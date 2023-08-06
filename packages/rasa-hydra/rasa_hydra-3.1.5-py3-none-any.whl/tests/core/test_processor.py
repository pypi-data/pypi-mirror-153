import aiohttp
import asyncio
import datetime
import uuid

import pytest
from aioresponses import aioresponses

from unittest.mock import patch

import rasa.utils.io
from rasa.core import jobs
from rasa.core.agent import Agent
from rasa.core.channels.channel import CollectingOutputChannel, UserMessage
from rasa.core.events import (
    ActionExecuted,
    BotUttered,
    ReminderCancelled,
    ReminderScheduled,
    Restarted,
    UserUttered,
)
from rasa.core.trackers import DialogueStateTracker
from rasa.core.slots import Slot
from rasa.core.processor import MessageProcessor
from rasa.core.interpreter import RasaNLUHttpInterpreter
from rasa.core.processor import MessageProcessor
from rasa.utils.endpoints import EndpointConfig
from tests.utilities import json_of_latest_request, latest_request

from tests.core.conftest import DEFAULT_DOMAIN_PATH_WITH_SLOTS
from rasa.core.domain import Domain

import logging

logger = logging.getLogger(__name__)


async def test_message_processor(
    default_channel: CollectingOutputChannel, default_processor: MessageProcessor
):
    await default_processor.handle_message(
        UserMessage('/greet{"name":"Core"}', default_channel)
    )
    assert {
        "recipient_id": "default",
        "text": "hey there Core!",
    } == default_channel.latest_output()


async def test_message_id_logging(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker

    message = UserMessage("If Meg was an egg would she still have a leg?")
    tracker = DialogueStateTracker("1", [])
    await default_processor._handle_message_with_tracker(message, tracker)
    logged_event = tracker.events[-1]

    assert logged_event.message_id == message.message_id
    assert logged_event.message_id is not None


async def test_parsing(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker
    message = UserMessage('/greet{"name": "boy"}')
    parsed = await default_processor._parse_message(message)
    assert parsed["intent"]["name"] == "greet"
    assert parsed["entities"][0]["entity"] == "name"


async def test_log_unseen_feature(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker
    message = UserMessage('/dislike{"test_entity": "RASA"}')
    parsed = await default_processor._parse_message(message)
    with pytest.warns(UserWarning) as record:
        default_processor._log_unseen_features(parsed)
    assert len(record) == 2
    assert (
        record[0].message.args[0]
        == "Interpreter parsed an intent 'dislike' that is not defined in the domain."
    )
    assert (
        record[1].message.args[0]
        == "Interpreter parsed an entity 'test_entity' that is not defined in the domain."
    )


async def test_default_intent_recognized(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker
    message = UserMessage("/restart")
    parsed = await default_processor._parse_message(message)
    with pytest.warns(None) as record:
        default_processor._log_unseen_features(parsed)
    assert len(record) == 0


async def test_http_parsing():
    message = UserMessage("lunch?")

    endpoint = EndpointConfig("https://interpreter.com")
    with aioresponses() as mocked:
        mocked.post("https://interpreter.com/model/parse", repeat=True, status=200)

        inter = RasaNLUHttpInterpreter(endpoint=endpoint)
        try:
            await MessageProcessor(inter, None, None, None, None)._parse_message(
                message
            )
        except KeyError:
            pass  # logger looks for intent and entities, so we except

        r = latest_request(mocked, "POST", "https://interpreter.com/model/parse")

        assert r


async def mocked_parse(self, text, message_id=None, tracker=None):
    """Mock parsing a text message and augment it with the slot
    value from the tracker's state."""

    return {
        "intent": {"name": "", "confidence": 0.0},
        "entities": [],
        "text": text,
        "requested_language": tracker.get_slot("requested_language"),
    }


async def test_parsing_with_tracker():
    tracker = DialogueStateTracker.from_dict("1", [], [Slot("requested_language")])

    # we'll expect this value 'en' to be part of the result from the interpreter
    tracker._set_slot("requested_language", "en")

    endpoint = EndpointConfig("https://interpreter.com")
    with aioresponses() as mocked:
        mocked.post("https://interpreter.com/parse", repeat=True, status=200)

        # mock the parse function with the one defined for this test
        with patch.object(RasaNLUHttpInterpreter, "parse", mocked_parse):
            interpreter = RasaNLUHttpInterpreter(endpoint=endpoint)
            agent = Agent(None, None, interpreter)
            result = await agent.parse_message_using_nlu_interpreter("lunch?", tracker)

            assert result["requested_language"] == "en"


async def test_reminder_scheduled(
    default_channel: CollectingOutputChannel, default_processor: MessageProcessor
):
    sender_id = uuid.uuid4().hex

    reminder = ReminderScheduled("utter_greet", datetime.datetime.now())
    tracker = await default_processor.tracker_store.get_or_create_tracker(sender_id)

    tracker.update(UserUttered("test"))
    tracker.update(ActionExecuted("action_reminder_reminder"))
    tracker.update(reminder)

    await default_processor.tracker_store.save(tracker)
    await default_processor.handle_reminder(
        reminder, sender_id, default_channel, default_processor.nlg
    )

    # retrieve the updated tracker
    t = await default_processor.tracker_store.retrieve(sender_id)
    assert t.events[-4] == UserUttered(None)
    assert t.events[-3] == ActionExecuted("utter_greet")
    assert t.events[-2] == BotUttered(
        "hey there None!",
        {
            "elements": None,
            "buttons": None,
            "quick_replies": None,
            "attachment": None,
            "image": None,
            "custom": None,
        },
        metadata={"template_name": "utter_greet"}
    )
    assert t.events[-1] == ActionExecuted("action_listen")

async def test_convert_messge_to_digits_1(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker

    message = UserMessage("one,one,one,one,one,one,one,one,one,one,one,one,one,one,one,one")
    tracker = DialogueStateTracker("1", [])
    await default_processor._handle_message_with_tracker(message, tracker)
    logged_event = tracker.events[-1]
    assert logged_event.entities_redacted is not None
    assert logged_event.text_redacted == "1111111111111111"

async def test_convert_messge_to_digits_2(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker

    message = UserMessage("1,2,3,4,5,6,7,8,9,0,9,8,7,6,5,4")
    tracker = DialogueStateTracker("1", [])
    await default_processor._handle_message_with_tracker(message, tracker)
    logged_event = tracker.events[-1]
    assert logged_event.entities_redacted is not None
    assert logged_event.text_redacted == "1234567890987654"

async def test_convert_messge_to_digits_3(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker

    message = UserMessage("make a one time payment")
    tracker = DialogueStateTracker("1", [])
    await default_processor._handle_message_with_tracker(message, tracker)
    logged_event = tracker.events[-1]
    assert logged_event.entities_redacted is not None
    assert logged_event.text_redacted == "make a one time payment"

async def test_convert_messge_to_digits_4(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker

    message = UserMessage("one,one,one,one,one one one,one,one,one,one,one,one,one,one,one.")
    tracker = DialogueStateTracker("1", [])
    await default_processor._handle_message_with_tracker(message, tracker)
    logged_event = tracker.events[-1]
    assert logged_event.entities_redacted is not None
    assert logged_event.text_redacted == "1111111111111111"

async def test_convert_messge_to_digits_5(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker

    message = UserMessage("one one one one one one one one one one")
    tracker = DialogueStateTracker("1", [])
    await default_processor._handle_message_with_tracker(message, tracker)
    logged_event = tracker.events[-1]
    assert logged_event.entities_redacted is not None
    assert logged_event.text_redacted == "one one one one one one one one one one"

async def test_convert_messge_to_digits_6(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker

    message = UserMessage("one one one one one one one one one one one one one")
    tracker = DialogueStateTracker("1", [])
    await default_processor._handle_message_with_tracker(message, tracker)
    logged_event = tracker.events[-1]
    assert logged_event.entities_redacted is not None
    assert logged_event.text_redacted == "1111111111111"

async def test_convert_messge_to_digits_7(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker

    message = UserMessage("my cc is one one one one one one one one one one one one one one one one")
    tracker = DialogueStateTracker("1", [])
    await default_processor._handle_message_with_tracker(message, tracker)
    logged_event = tracker.events[-1]
    assert logged_event.entities_redacted is not None
    assert logged_event.text_redacted == "my cc is 1111111111111111"

async def test_convert_messge_to_digits_8(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker

    message = UserMessage("my cc is won too hate for to ate one one one one one one one one one one")
    tracker = DialogueStateTracker("1", [])
    await default_processor._handle_message_with_tracker(message, tracker)
    logged_event = tracker.events[-1]
    assert logged_event.entities_redacted is not None
    assert logged_event.text_redacted == "my cc is 1284281111111111"

async def test_convert_messge_to_digits_9(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker

    message = UserMessage("for forward autopay auto pay won")
    tracker = DialogueStateTracker("1", [])
    await default_processor._handle_message_with_tracker(message, tracker)
    logged_event = tracker.events[-1]
    assert logged_event.entities_redacted is not None
    assert logged_event.text_redacted == "four forward autopay auto pay one"

async def test_convert_messge_to_digits_greet(default_processor: MessageProcessor):
    from rasa.core.trackers import DialogueStateTracker

    message = UserMessage("/greet{guid: 'BE45375', channelUserId: '+17897897898'}")
    tracker = DialogueStateTracker("1", [])
    await default_processor._handle_message_with_tracker(message, tracker)
    logged_event = tracker.events[-1]
    assert logged_event.entities_redacted is not None
    assert logged_event.text_redacted == "/greet{guid: 'BE45375', channelUserId: '+17897897898'}"

async def test_reminder_aborted(
    default_channel: CollectingOutputChannel, default_processor: MessageProcessor
):
    sender_id = uuid.uuid4().hex

    reminder = ReminderScheduled(
        "utter_greet", datetime.datetime.now(), kill_on_user_message=True
    )
    tracker = await default_processor.tracker_store.get_or_create_tracker(sender_id)

    tracker.update(reminder)
    tracker.update(UserUttered("test"))  # cancels the reminder

    await default_processor.tracker_store.save(tracker)
    await default_processor.handle_reminder(
        reminder, sender_id, default_channel, default_processor.nlg
    )

    # retrieve the updated tracker
    t = await default_processor.tracker_store.retrieve(sender_id)
    assert len(t.events) == 3  # nothing should have been executed


async def test_reminder_cancelled(
    default_channel: CollectingOutputChannel, default_processor: MessageProcessor
):
    sender_ids = [uuid.uuid4().hex, uuid.uuid4().hex]
    trackers = []
    for sender_id in sender_ids:
        tracker = await default_processor.tracker_store.get_or_create_tracker(sender_id)

        tracker.update(UserUttered("test"))
        tracker.update(ActionExecuted("action_reminder_reminder"))
        tracker.update(
            ReminderScheduled(
                "utter_greet", datetime.datetime.now(), kill_on_user_message=True
            )
        )
        trackers.append(tracker)

    # cancel reminder for the first user
    trackers[0].update(ReminderCancelled("utter_greet"))

    for tracker in trackers:
        await default_processor.tracker_store.save(tracker)
        await default_processor._schedule_reminders(
            tracker.events, tracker, default_channel, default_processor.nlg
        )
    # check that the jobs were added
    assert len((await jobs.scheduler()).get_jobs()) == 2

    for tracker in trackers:
        await default_processor._cancel_reminders(tracker.events, tracker)
    # check that only one job was removed
    assert len((await jobs.scheduler()).get_jobs()) == 1

    # execute the jobs
    await asyncio.sleep(5)

    tracker_0 = await default_processor.tracker_store.retrieve(sender_ids[0])
    # there should be no utter_greet action
    assert ActionExecuted("utter_greet") not in tracker_0.events

    tracker_1 = await default_processor.tracker_store.retrieve(sender_ids[1])
    # there should be utter_greet action
    assert ActionExecuted("utter_greet") in tracker_1.events


async def test_reminder_restart(
    default_channel: CollectingOutputChannel, default_processor: MessageProcessor
):
    sender_id = uuid.uuid4().hex

    reminder = ReminderScheduled(
        "utter_greet", datetime.datetime.now(), kill_on_user_message=False
    )
    tracker = await default_processor.tracker_store.get_or_create_tracker(sender_id)

    tracker.update(reminder)
    tracker.update(Restarted())  # cancels the reminder
    tracker.update(UserUttered("test"))

    await default_processor.tracker_store.save(tracker)
    await default_processor.handle_reminder(
        reminder, sender_id, default_channel, default_processor.nlg
    )

    # retrieve the updated tracker
    t = await default_processor.tracker_store.retrieve(sender_id)
    assert len(t.events) == 4  # nothing should have been executed
