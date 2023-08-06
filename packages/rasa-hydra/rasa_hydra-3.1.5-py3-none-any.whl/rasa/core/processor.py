import asyncio
import json
import warnings
import logging
import os
import copy
from types import LambdaType
from typing import Any, Dict, List, Optional, Text, Tuple
from rasa.core.utils import AvailableEndpoints
import aiohttp
import requests
from os import environ
import numpy as np
import time
import re
import string
from text2digits import text2digits
from metrics.constants import APP_NAV

t2d = text2digits.Text2Digits()

from metrics.constants import ACTION_PREDICT_EXECUTE_TIME
from rasa.core import jobs
from rasa.core.actions.action import Action, ACTION_DEFAULT_FALLBACK_NAME
from rasa.core.actions.action import ACTION_LISTEN_NAME, ActionExecutionRejection
from rasa.core.channels.channel import (
    CollectingOutputChannel,
    UserMessage,
    OutputChannel,
)
from rasa.core.constants import (
    ACTION_NAME_SENDER_ID_CONNECTOR_STR,
    USER_INTENT_RESTART,
    UTTER_PREFIX,
    USER_INTENT_BACK,
    USER_INTENT_OUT_OF_SCOPE,
    CDR_ENDPOINT,
    CDR_ACCOUNT_ID,
    CDR_ACCOUNT_TOKEN
)
from rasa.core.domain import Domain
from rasa.core.events import (
    ActionExecuted,
    ActionExecutionRejected,
    Event,
    ReminderCancelled,
    ReminderScheduled,
    SlotSet,
    UserUttered,
    BotUttered,
)
from rasa.core.interpreter import (
    INTENT_MESSAGE_PREFIX,
    NaturalLanguageInterpreter,
    RegexInterpreter,
)
from rasa.core.nlg import NaturalLanguageGenerator
from rasa.core.policies.asr_fallback import AsrFallbackPolicy
from rasa.core.policies.ensemble import PolicyEnsemble
from rasa.core.policies.form_nlu_fallback import FormFallbackPolicy
from rasa.core.tracker_store import TrackerStore
from rasa.core.trackers import DialogueStateTracker, EventVerbosity
from rasa.utils.endpoints import EndpointConfig
from rasa.utils.timer import timeit
from rasa.utils.redactor import Redactor
from rasa.constants import (
    ENV_MAX_NUMBER_OF_PREDICTIONS,
    ENV_MAX_PARTIALS_PROCESSED
)

logger = logging.getLogger(__name__)

MAX_NUMBER_OF_PREDICTIONS = ENV_MAX_NUMBER_OF_PREDICTIONS
MAX_PARTIALS_PROCESSED = ENV_MAX_PARTIALS_PROCESSED


redactor = Redactor()

if CDR_ENDPOINT == None or CDR_ACCOUNT_ID == None or CDR_ACCOUNT_TOKEN == None:
    logger.warning('CDR credentials do not exist, core is unable to submit App Nav events')

class MessageProcessor:
    def __init__(
            self,
            interpreter: NaturalLanguageInterpreter,
            policy_ensemble: PolicyEnsemble,
            domain: Domain,
            tracker_store: TrackerStore,
            generator: NaturalLanguageGenerator,
            action_endpoint: Optional[EndpointConfig] = None,
            max_number_of_predictions: int = MAX_NUMBER_OF_PREDICTIONS,
            message_preprocessor: Optional[LambdaType] = None,
            on_circuit_break: Optional[LambdaType] = None,
    ):
        self.interpreter = interpreter
        self.nlg = generator
        self.policy_ensemble = policy_ensemble
        self.domain = domain
        self.tracker_store = tracker_store
        self.max_number_of_predictions = max_number_of_predictions
        self.message_preprocessor = message_preprocessor
        self.on_circuit_break = on_circuit_break
        self.action_endpoint = action_endpoint

    async def handle_message(
            self, message: UserMessage
    ) -> Optional[List[Dict[Text, Any]]]:
        """Handle a single message with this processor."""

        # preprocess message if necessary
        tracker = await self.log_message(message, should_save_tracker=False)
        if not tracker:
            return None

        if not self.policy_ensemble or not self.domain:
            # save tracker state to continue conversation from this state
            await self._save_tracker(tracker)
            warnings.warn(
                "No policy ensemble or domain set. Skipping action prediction "
                "and execution."
            )
            return None

        start = time.perf_counter()
        await self._predict_and_execute_next_action(message, tracker)
        duration = time.perf_counter() - start
        ACTION_PREDICT_EXECUTE_TIME.observe(duration)
        # save tracker state to continue conversation from this state
        await self._save_tracker(tracker)

        if isinstance(message.output_channel, CollectingOutputChannel):
            return message.output_channel.messages
        else:
            return None

    async def predict_next(self, sender_id: Text) -> Optional[Dict[Text, Any]]:

        # we have a Tracker instance for each user
        # which maintains conversation state
        tracker = await self._get_tracker(sender_id)
        if not tracker:
            logger.warning(
                f"Failed to retrieve or create tracker for sender '{sender_id}'."
            )
            return None

        if not self.policy_ensemble or not self.domain:
            # save tracker state to continue conversation from this state
            warnings.warn(
                "No policy ensemble or domain set. Skipping action prediction "
            )
            return None

        probabilities, policy = self._get_next_action_probabilities(tracker)
        # save tracker state to continue conversation from this state
        await self._save_tracker(tracker)
        scores = [
            {"action": a, "score": p}
            for a, p in zip(self.domain.action_names, probabilities)
        ]
        return {
            "scores": scores,
            "policy": policy,
            "confidence": np.max(probabilities),
            "tracker": tracker.current_state(EventVerbosity.AFTER_RESTART),
        }

    async def log_message(
            self, message: UserMessage, should_save_tracker: bool = True
    ) -> Optional[DialogueStateTracker]:
        """Log `message` on tracker belonging to the message's conversation_id.

        Optionally save the tracker if `should_save_tracker` is `True`. Tracker saving
        can be skipped if the tracker returned by this method is used for further
        processing and saved at a later stage.
        """

        # preprocess message if necessary
        if self.message_preprocessor is not None:
            message.text = self.message_preprocessor(message.text)
        # we have a Tracker instance for each user
        # which maintains conversation state
        tracker = await self._get_tracker(message.sender_id)
        if tracker:
            await self._handle_message_with_tracker(message, tracker)

            if should_save_tracker:
                # save tracker state to continue conversation from this state
                await self._save_tracker(tracker)
        else:
            logger.warning(
                "Failed to retrieve or create tracker for sender "
                f"'{message.sender_id}'."
            )
        return tracker

    async def execute_action(
        self,
        sender_id: Text,
        action_name: Text,
        output_channel: OutputChannel,
        nlg: NaturalLanguageGenerator,
        policy: Text,
        confidence: float,
    ) -> Optional[DialogueStateTracker]:

        # we have a Tracker instance for each user
        # which maintains conversation state
        tracker = await self._get_tracker(sender_id)
        if tracker:
            action = self._get_action(action_name)
            await self._run_action(
                action, tracker, output_channel, nlg, policy, confidence
            )

            # save tracker state to continue conversation from this state
            await self._save_tracker(tracker)
        else:
            logger.warning(
                f"Failed to retrieve or create tracker for sender '{sender_id}'."
            )
        return tracker

    def predict_next_action(
        self, tracker: DialogueStateTracker
    ) -> Tuple[Action, Text, float]:
        """Predicts the next action the bot should take after seeing x.

        This should be overwritten by more advanced policies to use
        ML to predict the action. Returns the index of the next action."""

        action_confidences, policy = self._get_next_action_probabilities(tracker)

        max_confidence_index = int(np.argmax(action_confidences))
        action = self.domain.action_for_index(
            max_confidence_index, self.action_endpoint
        )
        logger.info(
            "[{}] - Predicted next action '{}' with confidence {:.2f}.".format(
                tracker.sender_id, action.name(), action_confidences[max_confidence_index]
            )
        )
        return action, policy, action_confidences[max_confidence_index]

    @staticmethod
    def _is_reminder(e: Event, name: Text) -> bool:
        return isinstance(e, ReminderScheduled) and e.name == name

    @staticmethod
    def _is_reminder_still_valid(
            tracker: DialogueStateTracker, reminder_event: ReminderScheduled
    ) -> bool:
        """Check if the conversation has been restarted after reminder."""

        for e in reversed(tracker.applied_events()):
            if MessageProcessor._is_reminder(e, reminder_event.name):
                return True
        return False  # not found in applied events --> has been restarted

    @staticmethod
    def _has_message_after_reminder(
            tracker: DialogueStateTracker, reminder_event: ReminderScheduled
    ) -> bool:
        """Check if the user sent a message after the reminder."""

        for e in reversed(tracker.events):
            if MessageProcessor._is_reminder(e, reminder_event.name):
                return False
            elif isinstance(e, UserUttered) and e.text:
                return True
        return True  # tracker has probably been restarted

    async def handle_reminder(
        self,
        reminder_event: ReminderScheduled,
        sender_id: Text,
        output_channel: OutputChannel,
        nlg: NaturalLanguageGenerator,
    ) -> None:
        """Handle a reminder that is triggered asynchronously."""

        tracker = await self._get_tracker(sender_id)

        if not tracker:
            logger.warning(
                f"Failed to retrieve or create tracker for sender '{sender_id}'."
            )
            return None

        if (
            reminder_event.kill_on_user_message
            and self._has_message_after_reminder(tracker, reminder_event)
            or not self._is_reminder_still_valid(tracker, reminder_event)
        ):
            logger.debug(
                "Canceled reminder because it is outdated. "
                "(event: {} id: {})".format(
                    reminder_event.action_name, reminder_event.name
                )
            )
        else:
            # necessary for proper featurization, otherwise the previous
            # unrelated message would influence featurization
            tracker.update(UserUttered.empty())
            action = self._get_action(reminder_event.action_name)
            should_continue = await self._run_action(
                action, tracker, output_channel, nlg
            )
            if should_continue:
                user_msg = UserMessage(None, output_channel, sender_id)
                await self._predict_and_execute_next_action(user_msg, tracker)
            # save tracker state to continue conversation from this state
            await self._save_tracker(tracker)

    @staticmethod
    def _log_slots(tracker):
        # Log currently set slots
        slot_values = "\n".join(
            [f"\t{s.name}: {s.value}" for s in tracker.slots.values()]
        )
        if slot_values.strip():
            logger.debug("[{}] - Current slot values: \n{}".format(tracker.sender_id, slot_values))

    def _is_nlu_threshold_passed(self, nlu_data, tracker):
        if self.policy_ensemble is None or tracker.active_form or tracker.get_slot("handoff_active"):
            return True

        form_fallback_policy = self.policy_ensemble.look_up_policy(FormFallbackPolicy)
        nlu_confidence = nlu_data.get("intent", {}).get("confidence", 0)

        if form_fallback_policy:
            return nlu_confidence >= form_fallback_policy.nlu_threshold
        else:
            return False

    def get_nlu_threshold(self):
        """
        Return the NLU confidence threshold. (It only looks for the nlu_threshold from the policy
        called FormFallbackPolicy. It will not work if users are using something else that is not called
        FormFallbackPolicy.
        """
        if self.policy_ensemble:
            policies = self.policy_ensemble.policies
            for p in reversed(policies):
                if "FormFallbackPolicy" in p.__str__():
                    return p.nlu_threshold

            return 0.3
        else:
            logger.warning(f"Unable to get nlu threshold. Default to 0.")
            return 0.0

    def get_asr_threshold(self, tracker: DialogueStateTracker):
        """
        Return the ASR confidence threshold. Use a default value of 0.4 if a grammar file is used.
        Otherwise, use the value from the AsrFallbackPolicy.
        """

        last_bot_utter_template = tracker.latest_bot_utterance.metadata.get("template_name")
        if last_bot_utter_template:
            bot_responses = self.domain.templates.get(last_bot_utter_template, [])
            for bot_response in bot_responses:
                if bot_response.get("custom") and bot_response.get("custom", {}).get('grammar_file'):
                    return bot_response.get("custom").get('confidence_threshold', 0.4)

        asr_fallback_policy = self.policy_ensemble.look_up_policy(AsrFallbackPolicy) if self.policy_ensemble else None
        if asr_fallback_policy:
            return asr_fallback_policy.nlu_threshold or 0.3
        else:
            return 0.0

    def get_group(self, tracker: DialogueStateTracker):
        last_bot_utter_template = tracker.latest_bot_utterance.metadata.get("template_name")
        if last_bot_utter_template:
            bot_responses = self.domain.templates.get(last_bot_utter_template, [])
            for bot_response in bot_responses:
                if bot_response.get("custom") and bot_response.get("custom").get("group"):
                    return bot_response.get("custom").get("group")
                elif bot_response.get("button") and bot_response.get("button").get("group"):
                    return bot_response.get("button").get("group")

    def _log_unseen_features(self, parse_data: Dict[Text, Any]) -> None:
        """Check if the NLU interpreter picks up intents or entities that aren't recognized."""

        domain_is_not_empty = self.domain and not self.domain.is_empty()

        default_intents = [
            USER_INTENT_RESTART,
            USER_INTENT_BACK,
            USER_INTENT_OUT_OF_SCOPE,
        ]

        intent = parse_data["intent"]["name"]
        if intent:
            intent_is_recognized = (
                domain_is_not_empty and intent in self.domain.intents
            ) or intent in default_intents
            if not intent_is_recognized:
                warnings.warn(
                    f"Interpreter parsed an intent '{intent}' "
                    "that is not defined in the domain."
                )

        entities = parse_data["entities"] or []
        for element in entities:
            entity = element["entity"]
            if entity and domain_is_not_empty and entity not in self.domain.entities:
                warnings.warn(
                    f"Interpreter parsed an entity '{entity}' "
                    "that is not defined in the domain."
                )

    def _get_action(self, action_name):
        return self.domain.action_for_name(action_name, self.action_endpoint)


    async def _parse_message(self, message, tracker: DialogueStateTracker = None):
        # for testing - you can short-cut the NLU part with a message
        # in the format /intent{"entity1": val1, "entity2": val2}
        # parse_data is a dict of intent & entities
        if message.text.startswith(INTENT_MESSAGE_PREFIX):
            parse_data = await RegexInterpreter().parse(
                message.text, message.message_id, tracker
            )
        else:
            parse_data = await self.interpreter.parse(
                message.text, message.message_id, tracker
            )

        red_parse_data = redactor.redact_event(parse_data)
        red_parse_data['text'] = self.convert_messge_to_digits(message.text)
        red_parse_data = {'parse_data': red_parse_data}
        bot_msg_data = {}
        if tracker and tracker.latest_bot_utterance:
            bot_msg_data = tracker.latest_bot_utterance.as_dict()
        should_redact = bot_msg_data.get('privacy_mode', False)
        if should_redact: 
            red_parse_data = redactor.redact_event_complete(red_parse_data)
        else:
            red_parse_data = redactor.redact_event(red_parse_data)

        logger.info(
            "[{}] - Received user message '{}' with intent '{}' "
            "and entities '{}'".format(
                message.sender_id, red_parse_data['parse_data']['text'], red_parse_data['parse_data']["intent"], red_parse_data['parse_data']["entities"]
            ))
        logger.debug("[{}] - Received parse_data '{}'".format(message.sender_id, red_parse_data))
        confidence_threshold = self.get_nlu_threshold()
        if type(message.metadata) is not dict:
            if type(message.metadata) is str:
                logger.warning("metadata of type 'str' changing to empty dictionary")
            message.metadata = {}
        message_type = message.metadata.get("message_type")
        intent_name = parse_data["intent"]["name"]
        partials = message.metadata.get("partials", [])
        original_text = self.convert_messge_to_digits(message.text)
        message.metadata["original_text"] = original_text
        if message_type == "SPOKEN" and len(partials) > 0 and (
                parse_data["intent"]["confidence"] < confidence_threshold or
                (intent_name == "action_handle_error" and message.text) or
                (intent_name == "out_of_scope" and message.text) or
                not intent_name or
                re.match('action_\w{0,50}_fallback', intent_name) or
                re.match('action_\w{0,50}_followup', intent_name)):
            logger.debug("Entering partials strategy with parse_data: {}".format(red_parse_data))

            partials = partials[::-1]  # reverse list
            if len(partials) > MAX_PARTIALS_PROCESSED:
                partials = partials[:MAX_PARTIALS_PROCESSED]

            logger.info(
                "[{}] - Beginning partials strategy with '{}' as partials".format(message.sender_id,
                                                                                  self.convert_messge_to_digits(str(partials))))
            for partial in partials:
                partials_parse_data = await self.interpreter.parse(partial, message.message_id, tracker)
                if partials_parse_data["intent"]["name"] and partials_parse_data["intent"]["confidence"] > confidence_threshold and (
                        partials_parse_data["intent"]["name"] != "action_handle_error" or
                        partials_parse_data["intent"]["name"] != "out_of_scope"):
                    
                    red_parse_data_partials = redactor.redact_event_complete(partials_parse_data)
                    #red_parse_data_partials['text'], red_parse_data_partials["intent"], red_parse_data["entities"]
                    # logger.info(
                    #     "[{}] - Received user message '{}' with intent '{}' "
                    #     "and entities '{}' from partial".format(
                    #         message.sender_id, red_parse_data_partials['text'], red_parse_data_partials["intent"], red_parse_data_partials["entities"]
                    #     ))
                    #self._log_unseen_features(parse_data)
                    return partials_parse_data

        self._log_unseen_features(parse_data)
        return parse_data

    def get_last_bot_msg(self, tracker: DialogueStateTracker):
        for event in reversed(tracker.events):
            if (event.__class__.__name__ == "BotUttered" and event.data and event.data['custom'] and event.data['custom']['type'] != 'send_sip_info'):
                return event
        return None

    def create_metadata(
            self, message: UserMessage, tracker: DialogueStateTracker
    ) -> Dict:
        requested_slot = tracker.get_slot("requested_slot")
        handoff_active = tracker.get_slot("handoff_active")

        metadata = message.metadata or {}
        if metadata and metadata.get("replyType"):
            metadata["type"] = metadata.get("replyType")
        else:
            metadata["type"] = "text"

        if metadata and metadata.get("error_message"):
            metadata["error"] = True

        if metadata and metadata.get("error"):
            metadata["error"] = True
            tracker.total_errors += 1

        if tracker.active_form.get("name"):
            metadata["active_form"] = tracker.active_form.get("name")

        if handoff_active:
            metadata["handoff_active"] = handoff_active

        if requested_slot:
            metadata["requested_slot"] = requested_slot

            if requested_slot.startswith("confidential"):
                metadata["is_pii"] = True

            if requested_slot == "confidential_pass":
                metadata["type"] = "password"
            elif requested_slot == "id":
                metadata["type"] = "username"

        if tracker.latest_bot_utterance and tracker.latest_bot_utterance.metadata and "template_name" in tracker.latest_bot_utterance.metadata:
            metadata["template_name"] = tracker.latest_bot_utterance.metadata.get("template_name")

        last_bot_msg = self.get_last_bot_msg(tracker)
        if last_bot_msg:
            if last_bot_msg.metadata and "template_name" in last_bot_msg.metadata:
                metadata["template_name"] = last_bot_msg.metadata.get("template_name")

            if last_bot_msg.data and "custom" in last_bot_msg.data:
                custom = last_bot_msg.data["custom"]
                if "grammar_file" in custom:
                    metadata["grammar_file"] = custom["grammar_file"]

        metadata["asr_threshold"] = self.get_asr_threshold(tracker)
        metadata["nlu_threshold"] = self.get_nlu_threshold()
        metadata["group"] = self.get_group(tracker)

        return metadata

    def log_user_msg(self, message, metadata, tracker: DialogueStateTracker):
        if metadata.get('is_pii'):
            logger.info(f"[{tracker.sender_id}] - User msg: [FILTERED]")
        else:
            logger.info(f"[{tracker.sender_id}] - User msg: {message}")

    # COH requirement for redacting pci data that may be given for the wrong prompt
    def convert_messge_to_digits(self, message):
        pci_msg = message
        if '/greet' not in pci_msg and '/disconnect' not in pci_msg and '/restart' not in pci_msg:
            if len(pci_msg) > 0 and pci_msg[-1] in string.punctuation and (pci_msg[-1] not in ['#', '*']):
                pci_msg = pci_msg[:-1]
            pci_msg = ' ' + pci_msg + ' '
            pci_msg = pci_msg.replace(',', ' ').replace(' for ', ' four ').replace(' to ', ' two ').replace(' too ', ' two ').replace(' won ', ' one ').replace(' hate ', ' eight ').replace(' ate ', ' eight ')
            pci_msg = pci_msg[1:-1]
            pci_msg_digits = t2d.convert(pci_msg)
            if len(re.findall("\d{12,}", pci_msg_digits)) > 0:
                pci_msg_digits = re.sub(r'(?<=\d)+ (?=\d)+', '', pci_msg_digits)
                return pci_msg_digits
            else:
                pci_msg = re.sub(r'(?<=\d)+ (?=\d)+', '', pci_msg)  # strips any white space between digits
                return pci_msg
        return message

    def convert_pci_entities(self, message):
        pci_msg = message
        num_list = []
        for i in pci_msg:
            if i['entity'] == 'number':
                num_list.append(i)
            elif len(num_list) <= 11:
                num_list = []

        for e in pci_msg:
            e['value'] = re.sub(r"(?<!\d)(\d{12,})(?!\d)", '****************', str(e['value']))
        if len(num_list) > 11:
            for e in pci_msg:
                if e['entity'] == 'number' and filter(lambda x: x['start'] == (e['start'] and x['end'] == e['end']),
                                                      num_list):
                    e['value'] = "****"
                    e['text'] = "****"
        return pci_msg

    async def _handle_message_with_tracker(
            self, message: UserMessage, tracker: DialogueStateTracker
    ) -> None:

        if message.parse_data:
            parse_data = message.parse_data
        else:
            parse_data = await self._parse_message(message, tracker)

        if parse_data['text']:
            parse_data['text'] = self.convert_messge_to_digits(parse_data['text'])
            
        if parse_data.get('metadata') and parse_data.get('metadata').get('original_text'):
            parse_data['metadata']['original_text'] = self.convert_messge_to_digits(parse_data['text'])

        if parse_data.get('metadata') and parse_data.get('metadata').get('partials'):
            new_partial = []
            for partial in parse_data.get('metadata').get('partials'):
                  new_partial.append(convert_messge_to_digits(partial))
            parse_data['metadata']['partials'] = new_partial
            
        bot_msg_data = tracker.latest_bot_utterance.as_dict()
        should_redact = bot_msg_data.get('privacy_mode')
        redacted_text = self.convert_messge_to_digits(message.text)
        original_text = message.metadata.get('original_text')
        partials = message.metadata.get('partials')
        redacted_entities = copy.deepcopy(parse_data['entities'])  # NOTE: They will not be redacted at this point but this is needed for tracker-consumers
        message.metadata['should_redact'] = bool(should_redact)
        if should_redact:
            redacted_text = UserUttered.redact_msg(redacted_text)
            if parse_data['text']:
                parse_data['text'] = UserUttered.redact_msg(self.convert_messge_to_digits(parse_data['text']))
            if original_text:
                converted_original_text = self.convert_messge_to_digits(original_text)
                message.metadata['original_text'] = UserUttered.redact_msg(converted_original_text)
            if partials and len(partials) > 0:
                converted_partials = []
                for partial in partials:
                    if partial and len(partial) > 0:
                        converted_partial = self.convert_messge_to_digits(partial)
                        converted_partials.append(UserUttered.redact_msg(converted_partial))
                message.metadata['partials'] = converted_partials

        missed_intent = not self._is_nlu_threshold_passed(parse_data, tracker)
        message.metadata = self.create_metadata(message, tracker)
        #self.log_user_msg(redacted_text, message.metadata, tracker)

        # don't ever directly mutate the tracker
        # - instead pass its events to log
        user_uttered = UserUttered(
                message.text,
                parse_data["intent"],
                parse_data["entities"],
                parse_data,
                asrConfidence=message.asr_confidence,
                recordingId=message.recording_id,
                input_channel=message.input_channel,
                message_id=message.message_id,
                missed_intent=missed_intent,
                metadata=message.metadata,
                text_redacted=redacted_text,
                entities_redacted=redacted_entities
            )

        
        tracker.update(
            user_uttered,
            self.domain,
        )

        if parse_data["entities"]:
            self._log_slots(tracker)

        self.log_appNav(tracker.sender_id, user_uttered, tracker.latest_bot_utterance)
        
        logger.debug(
            "[{}] - Logged UserUtterance - "
            "tracker now has {} events".format(tracker.sender_id, len(tracker.events))
        )

    @staticmethod
    def _should_handle_message(tracker: DialogueStateTracker):
        return (
                not tracker.is_paused()
                or tracker.latest_message.intent.get("name") == USER_INTENT_RESTART
        )

   
    async def send_app_nav_async(self, conversation_id, app_nav):
        payload = {
            'appNavs': [app_nav]
        }
        async with aiohttp.ClientSession() as session:
            
            try:
                fc_auth = aiohttp.BasicAuth(CDR_ACCOUNT_ID, CDR_ACCOUNT_TOKEN)
                endpoint = f"{CDR_ENDPOINT}/Accounts/{CDR_ACCOUNT_ID}/Calls/{conversation_id}/AppNavs"
                async with session.request(method='POST',url=endpoint,json=payload,verify_ssl=False,auth=fc_auth) as response:
                    logger.warning('[{}] - cdr submission: {}'.format(conversation_id, response.status))
            except aiohttp.ClientConnectorError as e:
                logger.warning('[{}] - cdr connection error: {}'.format(conversation_id, str(e)))
            except Exception as e:
                logger.warning('[{}] - cdr submission failed: {}'.format(conversation_id, str(e)))
    
    


    def log_appNav(self, sender_id: str, message: UserUttered, bot_utterance: BotUttered ):

        try:
            if (message.text == '/disconnect' and bot_utterance.data.get('custom', {}).get('grammars', None) == None ):
                app_nav = {
                    'key': '{}_disconnect'.format(message._metadata['template_name']),
                    'value': 'disconnect'
                }
                logger.info('[{}] - APP NAV: {}'.format(sender_id, app_nav))
                asyncio.create_task(self.send_app_nav_async(sender_id, app_nav))
                APP_NAV.labels(message._metadata['template_name'], 'disconnect', None).inc()

            elif message._metadata and message._metadata.get('message_type', None) == 'SPOKEN':
                transcriber = message._metadata.get('transcriber', 'NA')
                if message.metadata.get('reporting_error_type', None):
                    app_nav = {
                    'key': '{}_{}_nlu_{}'.format(transcriber, message._metadata['template_name'], message._metadata['reporting_error_type']),
                    'value': 'NO_INTENT'
                    }
                    logger.info('[{}] - APP NAV: {}'.format(sender_id, app_nav))
                    asyncio.create_task(self.send_app_nav_async(sender_id,app_nav))
                    APP_NAV.labels(message._metadata['template_name'], message._metadata['reporting_error_type'], transcriber ).inc()
                    
                elif message.missed_intent and message.intent['confidence'] < message._metadata['nlu_threshold']:
                    app_nav = {
                    'key': '{}_{}_nlu_no_match'.format(transcriber, message._metadata['template_name']),
                    'value': 'NO_INTENT'
                    }
                    logger.info('[{}] - APP NAV: {}'.format(sender_id, app_nav))
                    asyncio.create_task(self.send_app_nav_async(sender_id,app_nav))
                    APP_NAV.labels(message._metadata['template_name'], 'no_match', transcriber ).inc()
                    
                elif message.intent and message.intent['name'] == USER_INTENT_OUT_OF_SCOPE:
                    app_nav = {
                        'key': '{}_{}_nlu_no_match'.format(transcriber, message._metadata['template_name'] ),
                        'value': 'NO_INTENT'
                    }
                    logger.info('[{}] - APP NAV: {}'.format(sender_id, app_nav))
                    asyncio.create_task(self.send_app_nav_async(sender_id,app_nav))
                    APP_NAV.labels(message._metadata['template_name'], 'no_match', transcriber ).inc()
                    
                elif message.intent['confidence'] > message._metadata['nlu_threshold']:
                    app_nav = {
                    'key': '{}_{}_nlu_match'.format(transcriber, message._metadata['template_name'] ),
                    'value': message.intent['name']
                    }
                    logger.info('[{}] - APP NAV: {}'.format(sender_id, app_nav))
                    asyncio.create_task(self.send_app_nav_async(sender_id,app_nav))
                    APP_NAV.labels(message._metadata['template_name'], 'match', transcriber ).inc()
                else:
                    logger.debug("[{}] - APP NAV: Error logging app_nav: {}".format(sender_id, message))

        except Exception as e:
            logger.debug("APP NAV: Error logging app nav")

    # @timeit
    async def _predict_and_execute_next_action(
            self, message: UserMessage, tracker: DialogueStateTracker
    ):
        # keep taking actions decided by the policy until it chooses to 'listen'
        should_predict_another_action = True
        num_predicted_actions = 0

        def is_action_limit_reached():
            return (
                    num_predicted_actions == self.max_number_of_predictions
                    and should_predict_another_action
            )

        # action loop. predicts actions until we hit action listen
        while (
                should_predict_another_action
                and self._should_handle_message(tracker)
                and num_predicted_actions < self.max_number_of_predictions
        ):
            # this actually just calls the policy's method by the same name
            action, policy, confidence = self.predict_next_action(tracker)

            should_predict_another_action = await self._run_action(
                action, tracker, message.output_channel, self.nlg, policy, confidence
            )
            num_predicted_actions += 1
            if action and action.name() in ["action_handle_error", ACTION_DEFAULT_FALLBACK_NAME]:
                tracker.total_errors += 1

        if is_action_limit_reached():
            # circuit breaker was tripped
            logger.warning(
                "Circuit breaker tripped. Stopped predicting "
                f"more actions for sender '{tracker.sender_id}'."
            )
            if self.on_circuit_break:
                # call a registered callback
                self.on_circuit_break(tracker, message.output_channel, self.nlg)

    # noinspection PyUnusedLocal
    @staticmethod
    def should_predict_another_action(action_name, events):
        is_listen_action = action_name == ACTION_LISTEN_NAME
        return not is_listen_action

    @staticmethod
    # @timeit
    async def _send_bot_messages(
            events: List[Event],
            tracker: DialogueStateTracker,
            output_channel: OutputChannel,
    ) -> None:
        """Send all the bot messages that are logged in the events array."""
        for e in events:
            if not isinstance(e, BotUttered):
                continue

            if tracker.get_slot("handoff_active") and not tracker.get_slot("initializing_handoff"):
                e.type_name = "liveAgent"
            e.metadata["handoff_active"] = tracker.get_slot("handoff_active")
            await output_channel.send_response(tracker.sender_id, e.message())

    async def _schedule_reminders(
            self,
            events: List[Event],
            tracker: DialogueStateTracker,
            output_channel: OutputChannel,
            nlg: NaturalLanguageGenerator,
    ) -> None:
        """Uses the scheduler to time a job to trigger the passed reminder.

        Reminders with the same `id` property will overwrite one another
        (i.e. only one of them will eventually run)."""
        for e in events:
            if not isinstance(e, ReminderScheduled):
                continue

            (await jobs.scheduler()).add_job(
                self.handle_reminder,
                "date",
                run_date=e.trigger_date_time,
                args=[e, tracker.sender_id, output_channel, nlg],
                id=e.name,
                replace_existing=True,
                name=(
                        str(e.action_name)
                        + ACTION_NAME_SENDER_ID_CONNECTOR_STR
                        + tracker.sender_id
                ),
            )

    @staticmethod
    async def _cancel_reminders(
            events: List[Event], tracker: DialogueStateTracker
    ) -> None:
        """Cancel reminders by action_name"""
        # All Reminders with the same action name will be cancelled
        for e in events:
            if isinstance(e, ReminderCancelled):
                name_to_check = (
                        str(e.action_name)
                        + ACTION_NAME_SENDER_ID_CONNECTOR_STR
                        + tracker.sender_id
                )
                scheduler = await jobs.scheduler()
                for j in scheduler.get_jobs():
                    if j.name == name_to_check:
                        scheduler.remove_job(j.id)

    # @timeit
    async def _run_action(
            self, action, tracker, output_channel, nlg, policy=None, confidence=None
    ):
        # events and return values are used to update
        # the tracker state after an action has been taken
        try:
            events = await action.run(output_channel, nlg, tracker, self.domain)
        except ActionExecutionRejection:
            events = [ActionExecutionRejected(action.name(), policy, confidence)]
            tracker.update(events[0])
            return self.should_predict_another_action(action.name(), events)
        except Exception as e:
            logger.error(
                "[{}] - Encountered an exception while running action '{}'. "
                "Bot will continue, but the actions events are lost. "
                "Please check the logs of your action server for "
                "more information.".format(tracker.sender_id, action.name())
                , exc_info=True)
            # logger.error(e, exc_info=True)
            events = []

        self._log_action_on_tracker(tracker, action.name(), events, policy, confidence)
        if action.name() != ACTION_LISTEN_NAME and not action.name().startswith(
                UTTER_PREFIX
        ):
            self._log_slots(tracker)

        await asyncio.gather(
            self._send_bot_messages(events, tracker, output_channel),
            self._schedule_reminders(events, tracker, output_channel, nlg),
            self._cancel_reminders(events, tracker)
        )

        return self.should_predict_another_action(action.name(), events)

    def _warn_about_new_slots(self, tracker, action_name, events):
        # these are the events from that action we have seen during training

        if action_name not in self.policy_ensemble.action_fingerprints:
            return

        fp = self.policy_ensemble.action_fingerprints[action_name]
        slots_seen_during_train = fp.get("slots", set())
        for e in events:
            if isinstance(e, SlotSet) and e.key not in slots_seen_during_train:
                s = tracker.slots.get(e.key)
                if s and s.has_features():
                    if e.key == "requested_slot" and tracker.active_form:
                        pass
                    else:
                        warnings.warn(
                            f"Action '{action_name}' set a slot type '{e.key}' that "
                            f"it never set during the training. This "
                            f"can throw of the prediction. Make sure to "
                            f"include training examples in your stories "
                            f"for the different types of slots this "
                            f"action can return. Remember: you need to "
                            f"set the slots manually in the stories by "
                            f"adding '- slot{{\"{e.key}\": {e.value}}}' "
                            f"after the action."
                        )

    def _log_action_on_tracker(self, tracker, action_name, events, policy, confidence):
        # Ensures that the code still works even if a lazy programmer missed
        # to type `return []` at the end of an action or the run method
        # returns `None` for some other reason.
        if events is None:
            events = []

        logger.debug(
            "Action '{}' ended with events '{}'".format(
                action_name, [f"{e}" for e in events]
            )
        )

        self._warn_about_new_slots(tracker, action_name, events)

        if action_name is not None:
            # log the action and its produced events
            tracker.update(ActionExecuted(action_name, policy, confidence))

        for e in events:
            # this makes sure the events are ordered by timestamp -
            # since the event objects are created somewhere else,
            # the timestamp would indicate a time before the time
            # of the action executed
            e.timestamp = time.time()
            tracker.update(e, self.domain)

    async def _get_tracker(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        sender_id = sender_id or UserMessage.DEFAULT_SENDER_ID
        return await self.tracker_store.get_or_create_tracker(sender_id)

    async def _save_tracker(self, tracker: DialogueStateTracker) -> None:
        await self.tracker_store.save(tracker)

    def _prob_array_for_action(
            self, action_name: Text
    ) -> Tuple[Optional[List[float]], None]:
        idx = self.domain.index_for_action(action_name)
        if idx is not None:
            result = [0.0] * self.domain.num_actions
            result[idx] = 1.0
            return result, None
        else:
            return None, None

    def _get_next_action_probabilities(
            self, tracker: DialogueStateTracker
    ) -> Tuple[Optional[List[float]], Optional[Text]]:
        """Collect predictions from ensemble and return action and predictions.
        """

        followup_action = tracker.followup_action
        if followup_action:
            tracker.clear_followup_action()
            result = self._prob_array_for_action(followup_action)
            if result:
                return result
            else:
                logger.error(
                    "[{}] - Trying to run unknown follow up action '{}'!"
                    "Instead of running that, we will ignore the action "
                    "and predict the next action.".format(tracker.sender_id, followup_action)
                )

        return self.policy_ensemble.probabilities_using_best_policy(
            tracker, self.domain
        )
