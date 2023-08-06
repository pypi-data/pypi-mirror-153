import logging
from typing import List, Text

from rasa.core.actions.action import ACTION_LISTEN_NAME
from rasa.core.domain import Domain
from rasa.core.policies.fallback import FallbackPolicy
from rasa.core.trackers import DialogueStateTracker

FALLBACK_SCORE = 1.2
logger = logging.getLogger(__name__)

from rasa.core.events import (
    UserUttered, Form)


class FormFallbackPolicy(FallbackPolicy):
    """Policy which predicts fallback actions.

    A fallback can be triggered by a low confidence score on a
    NLU prediction or by a low confidence score on an action
    prediction. """

    def __init__(
            self,
            priority: int = 4,
            nlu_threshold: float = 0.3,
            ambiguity_threshold: float = 0.1,
            core_threshold: float = 0.3,
            fallback_action_name: Text = "action_default_fallback",
    ) -> None:
        """Create a new Fallback policy.

        Args:
            core_threshold: if NLU confidence threshold is met,
                predict fallback action with confidence `core_threshold`.
                If this is the highest confidence in the ensemble,
                the fallback action will be executed.
            nlu_threshold: minimum threshold for NLU confidence.
                If intent prediction confidence is lower than this,
                predict fallback action with confidence 1.0.
            fallback_action_name: name of the action to execute as a fallback
        """
        super(FormFallbackPolicy, self).__init__(priority=priority)

        self.nlu_threshold = nlu_threshold
        self.ambiguity_threshold = ambiguity_threshold
        self.core_threshold = core_threshold
        self.fallback_action_name = fallback_action_name

    def should_fallback(self,
                        nlu_confidence: float,
                        last_action_name: Text) -> bool:
        """It should predict fallback action only if
        a. predicted NLU confidence is lower than ``nlu_threshold`` &&
        b. last action is NOT fallback action
        """
        return (nlu_confidence < self.nlu_threshold and
                last_action_name != self.fallback_action_name)

    def get_confidence(self, events):
        active_form = None
        for event in events:
            if isinstance(event, UserUttered):
                if active_form not in ('authentication_form', 'feedback_form'):
                    form_latest_message = event
            elif isinstance(event, Form):
                active_form = event.name

        nlu_data = form_latest_message.parse_data
        return nlu_data["intent"].get("confidence", 1.0)

    def predict_action_probabilities(self,
                                     tracker: DialogueStateTracker,
                                     domain: Domain) -> List[float]:
        """Predicts a fallback action if NLU confidence is low
            or no other policy has a high-confidence prediction"""

        end_states = ['utter_transfer', 'utter_ok_else', 'utter_bye']
        nlu_data = tracker.latest_message.parse_data

        # if NLU interpreter does not provide confidence score,
        # it is set to 1.0 here in order
        # to not override standard behaviour
        nlu_confidence = nlu_data.get("intent", {}).get("confidence", 1.0)

        if tracker.latest_action_name == self.fallback_action_name:
            result = [0.0] * domain.num_actions
            if tracker.get_slot('errors') > 2:
                idx = domain.index_for_action('utter_transfer')
                result[idx] = 1.3
            else:
                idx = domain.index_for_action(ACTION_LISTEN_NAME)
                result[idx] = 1.3

        if tracker.latest_action_name in end_states:
            result = self.fallback_scores(domain, self.core_threshold)

        elif self.should_nlu_fallback(nlu_data, tracker.latest_action_name):
            logger.debug(
                "NLU confidence {} is lower "
                "than NLU threshold {:.2f}. "
                "".format(nlu_confidence, self.nlu_threshold)
            )
            result = self.fallback_scores(domain)
        else:
            # NLU confidence threshold is met, so
            # predict fallback action with confidence `core_threshold`
            # if this is the highest confidence in the ensemble,
            # the fallback action will be executed.
            logger.debug(
                "NLU confidence threshold met, confidence of "
                "fallback action set to core threshold ({}).".format(
                    self.core_threshold
                )
            )
            result = self.fallback_scores(domain, self.core_threshold)

        return result
