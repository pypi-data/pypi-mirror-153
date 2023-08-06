import json
import logging
import os
import tempfile
import itertools

import fakeredis
import pytest

import rasa.utils.io
from rasa.core import training, restore
from rasa.core.actions.action import ACTION_LISTEN_NAME
from rasa.core.domain import Domain
from rasa.core.events import (
    SlotSet,
    UserUttered,
    BotUttered,
    ActionExecuted,
    Restarted,
    ActionReverted,
    UserUtteranceReverted,
)
from rasa.core.tracker_store import (
    InMemoryTrackerStore,
    RedisTrackerStore,
    SQLTrackerStore,
)
from rasa.core.tracker_store import TrackerStore
from rasa.core.trackers import DialogueStateTracker, EventVerbosity
from tests.core.conftest import DEFAULT_STORIES_FILE, EXAMPLE_DOMAINS, TEST_DIALOGUES
from tests.core.utilities import (
    tracker_from_dialogue_file,
    read_dialogue_file,
    user_uttered,
    get_tracker,
)

domain = Domain.load("examples/moodbot/domain.yml")


class MockRedisTrackerStore(RedisTrackerStore):
    def __init__(self, domain):
        self.red = fakeredis.FakeStrictRedis()
        self.record_exp = None

        # added in redis==3.3.0, but not yet in fakeredis
        self.red.connection_pool.connection_class.health_check_interval = 0

        TrackerStore.__init__(self, domain)


def stores_to_be_tested():
    temp = tempfile.mkdtemp()
    return [
        MockRedisTrackerStore(domain),
        InMemoryTrackerStore(domain),
        # SQL-tracker test is broken.
        # SQLTrackerStore(domain, db=os.path.join(temp, "rasa.db")),
    ]


def stores_to_be_tested_ids():
    # SQL-tracker test is broken.
    # return ["redis-tracker", "in-memory-tracker", "SQL-tracker"]
    return ["redis-tracker", "in-memory-tracker"]


def test_tracker_duplicate():
    filename = "data/test_dialogues/moodbot.json"
    dialogue = read_dialogue_file(filename)
    tracker = DialogueStateTracker(dialogue.name, domain.slots)
    tracker.recreate_from_dialogue(dialogue)
    num_actions = len(
        [event for event in dialogue.events if isinstance(event, ActionExecuted)]
    )

    # There is always one duplicated tracker more than we have actions,
    # as the tracker also gets duplicated for the
    # action that would be next (but isn't part of the operations)
    assert len(list(tracker.generate_all_prior_trackers())) == num_actions + 1


@pytest.mark.parametrize("store", stores_to_be_tested(), ids=stores_to_be_tested_ids())
async def test_tracker_store_storage_and_retrieval(store):
    tracker = await store.get_or_create_tracker("some-id")
    # the retrieved tracker should be empty
    assert tracker.sender_id == "some-id"

    # Action listen should be in there
    assert list(tracker.events) == [ActionExecuted(ACTION_LISTEN_NAME)]

    # lets log a test message
    intent = {"name": "greet", "confidence": 1.0}
    tracker.update(UserUttered("/greet", intent, []))
    assert tracker.latest_message.intent.get("name") == "greet"
    await store.save(tracker)

    # retrieving the same tracker should result in the same tracker
    retrieved_tracker = await store.get_or_create_tracker("some-id")
    assert retrieved_tracker.sender_id == "some-id"
    assert len(retrieved_tracker.events) == 2
    assert retrieved_tracker.latest_message.intent.get("name") == "greet"

    # getting another tracker should result in an empty tracker again
    other_tracker = await store.get_or_create_tracker("some-other-id")
    assert other_tracker.sender_id == "some-other-id"
    assert len(other_tracker.events) == 1


@pytest.mark.skip(reason="Broken test.")
@pytest.mark.parametrize("store", stores_to_be_tested(), ids=stores_to_be_tested_ids())
@pytest.mark.parametrize("pair", zip(TEST_DIALOGUES, EXAMPLE_DOMAINS))
def test_tracker_store(store, pair):
    filename, domainpath = pair
    domain = Domain.load(domainpath)
    tracker = tracker_from_dialogue_file(filename, domain)
    store.save(tracker)
    restored = store.retrieve(tracker.sender_id)
    assert restored == tracker


async def test_tracker_write_to_story(tmpdir, moodbot_domain):
    tracker = tracker_from_dialogue_file(
        "data/test_dialogues/moodbot.json", moodbot_domain
    )
    p = tmpdir.join("export.md")
    tracker.export_stories_to_file(p.strpath)
    trackers = await training.load_data(
        p.strpath,
        moodbot_domain,
        use_story_concatenation=False,
        tracker_limit=1000,
        remove_duplicates=False,
    )
    assert len(trackers) == 1
    recovered = trackers[0]
    assert len(recovered.events) == 11
    assert recovered.events[4].type_name == "user"
    assert recovered.events[4].intent == {"confidence": 1.0, "name": "mood_unhappy"}


async def test_tracker_state_regression_without_bot_utterance(default_agent):
    sender_id = "test_tracker_state_regression_without_bot_utterance"
    for i in range(0, 2):
        await default_agent.handle_message("/greet", sender_id=sender_id)
    tracker = await default_agent.tracker_store.get_or_create_tracker(sender_id)

    # Ensures that the tracker has changed between the utterances
    # (and wasn't reset in between them)
    expected = "action_listen;greet;utter_greet;action_listen;greet;action_listen"
    assert (
        ";".join([e.as_story_string() for e in tracker.events if e.as_story_string()])
        == expected
    )


async def test_tracker_state_regression_with_bot_utterance(default_agent):
    sender_id = "test_tracker_state_regression_with_bot_utterance"
    for i in range(0, 2):
        await default_agent.handle_message("/greet", sender_id=sender_id)
    tracker = await default_agent.tracker_store.get_or_create_tracker(sender_id)

    expected = [
        "action_listen",
        "greet",
        "utter_greet",
        None,
        "action_listen",
        "greet",
        "action_listen",
    ]

    assert [e.as_story_string() for e in tracker.events] == expected


async def test_bot_utterance_comes_after_action_event(default_agent):
    sender_id = "test_bot_utterance_comes_after_action_event"

    await default_agent.handle_message("/greet", sender_id=sender_id)

    tracker = await default_agent.tracker_store.get_or_create_tracker(sender_id)

    # important is, that the 'bot' comes after the second 'action' and not
    # before
    expected = ["action", "user", "action", "bot", "action"]

    assert [e.type_name for e in tracker.events] == expected


def test_tracker_entity_retrieval(default_domain):
    tracker = DialogueStateTracker("default", default_domain.slots)
    # the retrieved tracker should be empty
    assert len(tracker.events) == 0
    assert list(tracker.get_latest_entity_values("entity_name")) == []

    intent = {"name": "greet", "confidence": 1.0}
    tracker.update(
        UserUttered(
            "/greet",
            intent,
            [
                {
                    "start": 1,
                    "end": 5,
                    "value": "greet",
                    "entity": "entity_name",
                    "extractor": "manual",
                }
            ],
        )
    )
    assert list(tracker.get_latest_entity_values("entity_name")) == ["greet"]
    assert list(tracker.get_latest_entity_values("unknown")) == []


def test_tracker_store_pci_disconnect(default_domain):
    tracker = DialogueStateTracker("default", default_domain.slots)
    # the retrieved tracker should be empty
    assert len(tracker.events) == 0
    assert list(tracker.get_latest_entity_values("entity_name")) == []

    intent = {"name": "disconnect", "confidence": 1.0}
    tracker.update(
        UserUttered(
            "/disconnect",
            intent,
            [],
            None,
            None,
            None,
            189547,
            {'should_redact': True}
        )
    )
    assert tracker.latest_message.intent.get("name") == "disconnect"


def test_tracker_update_slots_with_entity(default_domain):
    tracker = DialogueStateTracker("default", default_domain.slots)

    test_entity = default_domain.entities[0]
    expected_slot_value = "test user"

    intent = {"name": "greet", "confidence": 1.0}
    tracker.update(
        UserUttered(
            "/greet",
            intent,
            [
                {
                    "start": 1,
                    "end": 5,
                    "value": expected_slot_value,
                    "entity": test_entity,
                    "extractor": "manual",
                }
            ],
        ),
        default_domain,
    )

    assert tracker.get_slot(test_entity) == expected_slot_value


def test_restart_event(default_domain):
    tracker = DialogueStateTracker("default", default_domain.slots)
    # the retrieved tracker should be empty
    assert len(tracker.events) == 0

    intent = {"name": "greet", "confidence": 1.0}
    tracker.update(ActionExecuted(ACTION_LISTEN_NAME))
    tracker.update(UserUttered("/greet", intent, []))
    tracker.update(ActionExecuted("my_action"))
    tracker.update(ActionExecuted(ACTION_LISTEN_NAME))

    assert len(tracker.events) == 4
    assert tracker.latest_message.text == "/greet"
    assert len(list(tracker.generate_all_prior_trackers())) == 4

    tracker.update(Restarted())

    assert len(tracker.events) == 5
    assert tracker.followup_action is not None
    assert tracker.followup_action == ACTION_LISTEN_NAME
    assert tracker.latest_message.text is None
    assert len(list(tracker.generate_all_prior_trackers())) == 1

    dialogue = tracker.as_dialogue()

    recovered = DialogueStateTracker("default", default_domain.slots)
    recovered.recreate_from_dialogue(dialogue)

    assert recovered.current_state() == tracker.current_state()
    assert len(recovered.events) == 5
    assert recovered.latest_message.text is None
    assert len(list(recovered.generate_all_prior_trackers())) == 1


def test_revert_action_event(default_domain):
    tracker = DialogueStateTracker("default", default_domain.slots)
    # the retrieved tracker should be empty
    assert len(tracker.events) == 0

    intent = {"name": "greet", "confidence": 1.0}
    tracker.update(ActionExecuted(ACTION_LISTEN_NAME))
    tracker.update(UserUttered("/greet", intent, []))
    tracker.update(ActionExecuted("my_action"))
    tracker.update(ActionExecuted(ACTION_LISTEN_NAME))

    # Expecting count of 4:
    #   +3 executed actions
    #   +1 final state
    assert tracker.latest_action_name == ACTION_LISTEN_NAME
    assert len(list(tracker.generate_all_prior_trackers())) == 4

    tracker.update(ActionReverted())

    # Expecting count of 3:
    #   +3 executed actions
    #   +1 final state
    #   -1 reverted action
    assert tracker.latest_action_name == "my_action"
    assert len(list(tracker.generate_all_prior_trackers())) == 3

    dialogue = tracker.as_dialogue()

    recovered = DialogueStateTracker("default", default_domain.slots)
    recovered.recreate_from_dialogue(dialogue)

    assert recovered.current_state() == tracker.current_state()
    assert tracker.latest_action_name == "my_action"
    assert len(list(tracker.generate_all_prior_trackers())) == 3


def test_revert_user_utterance_event(default_domain):
    tracker = DialogueStateTracker("default", default_domain.slots)
    # the retrieved tracker should be empty
    assert len(tracker.events) == 0

    intent1 = {"name": "greet", "confidence": 1.0}
    tracker.update(ActionExecuted(ACTION_LISTEN_NAME))
    tracker.update(UserUttered("/greet", intent1, []))
    tracker.update(ActionExecuted("my_action_1"))
    tracker.update(ActionExecuted(ACTION_LISTEN_NAME))

    intent2 = {"name": "goodbye", "confidence": 1.0}
    tracker.update(UserUttered("/goodbye", intent2, []))
    tracker.update(ActionExecuted("my_action_2"))
    tracker.update(ActionExecuted(ACTION_LISTEN_NAME))

    # Expecting count of 6:
    #   +5 executed actions
    #   +1 final state
    assert tracker.latest_action_name == ACTION_LISTEN_NAME
    assert len(list(tracker.generate_all_prior_trackers())) == 6

    tracker.update(UserUtteranceReverted())

    # Expecting count of 3:
    #   +5 executed actions
    #   +1 final state
    #   -2 rewound actions associated with the /goodbye
    #   -1 rewound action from the listen right before /goodbye
    assert tracker.latest_action_name == "my_action_1"
    assert len(list(tracker.generate_all_prior_trackers())) == 3

    dialogue = tracker.as_dialogue()

    recovered = DialogueStateTracker("default", default_domain.slots)
    recovered.recreate_from_dialogue(dialogue)

    assert recovered.current_state() == tracker.current_state()
    assert tracker.latest_action_name == "my_action_1"
    assert len(list(tracker.generate_all_prior_trackers())) == 3


def test_traveling_back_in_time(default_domain):
    tracker = DialogueStateTracker("default", default_domain.slots)
    # the retrieved tracker should be empty
    assert len(tracker.events) == 0

    intent = {"name": "greet", "confidence": 1.0}
    tracker.update(ActionExecuted(ACTION_LISTEN_NAME))
    tracker.update(UserUttered("/greet", intent, []))

    import time

    time.sleep(1)
    time_for_timemachine = time.time()
    time.sleep(1)

    tracker.update(ActionExecuted("my_action"))
    tracker.update(ActionExecuted(ACTION_LISTEN_NAME))

    # Expecting count of 4:
    #   +3 executed actions
    #   +1 final state
    assert tracker.latest_action_name == ACTION_LISTEN_NAME
    assert len(tracker.events) == 4
    assert len(list(tracker.generate_all_prior_trackers())) == 4

    tracker = tracker.travel_back_in_time(time_for_timemachine)

    # Expecting count of 2:
    #   +1 executed actions
    #   +1 final state
    assert tracker.latest_action_name == ACTION_LISTEN_NAME
    assert len(tracker.events) == 2
    assert len(list(tracker.generate_all_prior_trackers())) == 2


async def test_dump_and_restore_as_json(default_agent, tmpdir_factory):
    trackers = await default_agent.load_data(DEFAULT_STORIES_FILE)

    for tracker in trackers:
        out_path = tmpdir_factory.mktemp("tracker").join("dumped_tracker.json")

        dumped = tracker.current_state(EventVerbosity.AFTER_RESTART)
        rasa.utils.io.dump_obj_as_json_to_file(out_path.strpath, dumped)

        restored_tracker = restore.load_tracker_from_json(
            out_path.strpath, default_agent.domain
        )

        assert restored_tracker == tracker


@pytest.mark.skip(reason="Broken test.")
def test_read_json_dump(default_agent):
    tracker_dump = "data/test_trackers/tracker_moodbot.json"
    tracker_json = json.loads(rasa.utils.io.read_file(tracker_dump))

    restored_tracker = restore.load_tracker_from_json(
        tracker_dump, default_agent.domain
    )

    assert len(restored_tracker.events) == 7
    assert restored_tracker.latest_action_name == "action_listen"
    assert not restored_tracker.is_paused()
    assert restored_tracker.sender_id == "mysender"
    assert restored_tracker.events[-1].timestamp == 1517821726.211042

    restored_state = restored_tracker.current_state(EventVerbosity.AFTER_RESTART)
    assert restored_state == tracker_json


def test_current_state_after_restart(default_agent):
    tracker_dump = "data/test_trackers/tracker_moodbot.json"
    tracker_json = json.loads(rasa.utils.io.read_file(tracker_dump))

    tracker_json["events"].insert(3, {"event": "restart"})

    tracker = DialogueStateTracker.from_dict(
        tracker_json.get("sender_id"),
        tracker_json.get("events", []),
        default_agent.domain.slots,
    )

    events_after_restart = [e.as_dict() for e in list(tracker.events)[4:]]

    state = tracker.current_state(EventVerbosity.AFTER_RESTART)
    assert state.get("events") == events_after_restart


def test_current_state_all_events(default_agent):
    tracker_dump = "data/test_trackers/tracker_moodbot.json"
    tracker_json = json.loads(rasa.utils.io.read_file(tracker_dump))

    tracker_json["events"].insert(3, {"event": "restart"})

    tracker = DialogueStateTracker.from_dict(
        tracker_json.get("sender_id"),
        tracker_json.get("events", []),
        default_agent.domain.slots,
    )

    evts = [e.as_dict() for e in tracker.events]

    state = tracker.current_state(EventVerbosity.ALL)
    assert state.get("events") == evts


def test_current_state_no_events(default_agent):
    tracker_dump = "data/test_trackers/tracker_moodbot.json"
    tracker_json = json.loads(rasa.utils.io.read_file(tracker_dump))

    tracker = DialogueStateTracker.from_dict(
        tracker_json.get("sender_id"),
        tracker_json.get("events", []),
        default_agent.domain.slots,
    )

    state = tracker.current_state(EventVerbosity.NONE)
    assert state.get("events") is None


def test_current_state_applied_events(default_agent):
    tracker_dump = "data/test_trackers/tracker_moodbot.json"
    tracker_json = json.loads(rasa.utils.io.read_file(tracker_dump))

    # add some events that result in other events not being applied anymore
    tracker_json["events"].insert(1, {"event": "restart"})
    tracker_json["events"].insert(7, {"event": "rewind"})
    tracker_json["events"].insert(8, {"event": "undo"})

    tracker = DialogueStateTracker.from_dict(
        tracker_json.get("sender_id"),
        tracker_json.get("events", []),
        default_agent.domain.slots,
    )

    evts = [e.as_dict() for e in tracker.events]
    applied_events = [evts[2], evts[9]]

    state = tracker.current_state(EventVerbosity.APPLIED)
    assert state.get("events") == applied_events


async def test_tracker_dump_e2e_story(default_agent):
    sender_id = "test_tracker_dump_e2e_story"

    await default_agent.handle_message("/greet", sender_id=sender_id)
    await default_agent.handle_message("/goodbye", sender_id=sender_id)
    tracker = await default_agent.tracker_store.get_or_create_tracker(sender_id)

    story = tracker.export_stories(e2e=True)
    assert story.strip().split("\n") == [
        "## test_tracker_dump_e2e_story",
        "* greet: /greet",
        "    - utter_greet",
        "* goodbye: /goodbye",
    ]


def test_get_last_event_for():
    events = [ActionExecuted("one"), user_uttered("two", 1)]

    tracker = get_tracker(events)

    assert tracker.get_last_event_for(ActionExecuted).action_name == "one"


def test_get_last_event_with_reverted():
    events = [ActionExecuted("one"), ActionReverted(), user_uttered("two", 1)]

    tracker = get_tracker(events)

    assert tracker.get_last_event_for(ActionExecuted) is None


def test_get_last_event_for_with_skip():
    events = [ActionExecuted("one"), user_uttered("two", 1), ActionExecuted("three")]

    tracker = get_tracker(events)

    assert tracker.get_last_event_for(ActionExecuted, skip=1).action_name == "one"


def test_get_last_event_for_with_exclude():
    events = [ActionExecuted("one"), user_uttered("two", 1), ActionExecuted("three")]

    tracker = get_tracker(events)

    assert (
        tracker.get_last_event_for(
            ActionExecuted, action_names_to_exclude=["three"]
        ).action_name
        == "one"
    )


def test_last_executed_has():
    events = [
        ActionExecuted("one"),
        user_uttered("two", 1),
        ActionExecuted(ACTION_LISTEN_NAME),
    ]

    tracker = get_tracker(events)

    assert tracker.last_executed_action_has("one") is True


def test_last_executed_has_not_name():
    events = [
        ActionExecuted("one"),
        user_uttered("two", 1),
        ActionExecuted(ACTION_LISTEN_NAME),
    ]

    tracker = get_tracker(events)

    assert tracker.last_executed_action_has("another") is False


def test_events_metadata():
    # It should be possible to attach arbitrary metadata to any event and then
    # retrieve it after getting the tracker dict representation.
    events = [
        ActionExecuted("one", metadata={"one": 1}),
        user_uttered("two", 1, metadata={"two": 2}),
        ActionExecuted(ACTION_LISTEN_NAME, metadata={"three": 3}),
    ]

    events = get_tracker(events).current_state(EventVerbosity.ALL)["events"]
    assert events[0]["metadata"] == {"one": 1}
    assert events[1]["metadata"] == {"two": 2}
    assert events[2]["metadata"] == {"three": 3}


@pytest.mark.skip(reason="Broken test.")
def test_tracker_app_events():
    app_events = {'capture_utterance', 'get_speech', 'send_sip_info', 'dtmf', 'hangup'}
    events = [
        UserUttered("/greet", {"name": "greet", "confidence": 1.0}, []),
        ActionExecuted("one", metadata={"custom": {"type": "capture_utterance"}})
    ]
    tracker = get_tracker(events)
    assert len(tracker.app_events) == 5
    assert tracker.app_events == app_events


def test_tracker_total_steps():
    events = [
        UserUttered('/greet{channelUserId: +11231231234,entry_point: non_device}', {'name': 'greet', 'confidence': 1.0},
                    [{'entity': 'channelUserId', 'start': 6, 'end': 65, 'value': '+11231231234'},
                     {'entity': 'entry_point', 'start': 6, 'end': 65, 'value': 'non_device'}]),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"audio": "EN_US/audioLogo.wav,EN_US/greeting.wav", "barge_in": False,
                                     "group": "greeting", "text": "AudioLogo EN_US/greeting.wav",
                                     "type": "capture_utterance"}},
                   {"template_name": "utter_greet", "files": "EN_US/greeting.wav", "handoff_active": None}),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"audio": "EN_US/select_language.wav", "barge_in": False, "grammars": [
                              {"contentId": "Language.grxml", "grammarFile": "Language.grxml", "grammarType": "URL"},
                              {"contentId": "Language_DTMF.grxml", "grammarFile": "Language_DTMF.grxml",
                               "grammarType": "URL"}], "group": "select_language", "max_digits": 1, "min_digits": 0,
                                     "recognitionTimeoutMs": 5000,
                                     "text": "Say English or press 1, or Spanish or press 2",
                                     "type": "capture_utterance"}},
                   {"template_name": "utter_ask_select_language", "audio_dir": "EN_US", "handoff_active": None}),
        UserUttered("", {'name': None, 'confidence': 0.0}, []),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"audio": "EN_US/temp_help_message.wav", "barge_in": False, "group": "hmihy",
                                     "max_digits": 1, "min_digits": 0, "text": "<pause 0.1>", "type": "capture_utterance"}},
                   {"template_name": "temp_help_message", "handoff_active": None}),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"audio": "EN_US/so_hmihy.wav", "barge_in": False, "group": "hmihy", "max_digits": 1,
                                     "min_digits": 0,
                                     "text": "So, how can we help you today? <pause 0.250> Say something like \"make the next payment on my account\" or \"what are your store hours?\"",
                                     "type": "capture_utterance"}}, {"template_name": "so_hmihy", "handoff_active": None}),
        UserUttered("", {'name': None, 'confidence': 0.0}, []),
        UserUttered("", {'name': 'out_of_scope', 'confidence': 1}, []),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"audio": "EN_US/hmihy_1_alt_1.wav", "group": "hmihy", "max_digits": 1, "min_digits": 0,
                                     "text": "Try say something like \"when is my bill due\" or \"buy more mobile data.\"",
                                     "type": "capture_utterance"}},
                   {"template_name": "hmihy_1_alt_1", "handoff_active": None, "prediction_error": True}),
        UserUttered("", {'name': None, 'confidence': 0.0}, []),
        UserUttered("", {'name': 'out_of_scope', 'confidence': 1}, []),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"audio": "EN_US/difficulty_understanding_press_keys.wav", "barge_in": False,
                                     "group": "hmihy_backoff",
                                     "text": "Sorry I don't seem to be getting it. Let's try this another way. Please respond by using the keys on your phone.",
                                     "type": "capture_utterance"}},
                   {"template_name": "difficulty_understanding_press_keys", "handoff_active": None,
                    "prediction_error": True}),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {
                              "audio": "EN_US/hmihy_backoff_payments.wav,EN_US/press_key_1.wav,EN_US/hmihy_backoff_settings.wav,EN_US/press_key_2.wav,EN_US/hmihy_backoff_voicemail.wav,EN_US/press_key_3.wav,EN_US/hmihy_backoff_lost_stolen.wav,EN_US/press_key_4.wav,EN_US/hmihy_backoff_features.wav,EN_US/press_key_5.wav,EN_US/hmihy_backoff_device_issues.wav,EN_US/press_key_6.wav",
                              "group": "hmihy_backoff", "max_digits": 1, "min_digits": 0,
                              "text": "For payments and autopay, press 1. To manage basic account settings, such as your PIN, and your language preference, press 2. For voicemail help, press 3. For lost or stolen device options press 4. [Remaining Options]",
                              "type": "dtmf"}}, {"template_name": "hmihy_backoff_with_features", "handoff_active": None}),
        UserUttered("get_one_time_pin", {'name': 'out_of_scope', 'confidence': 0.0}, []),
        UserUttered('1', {'name': 'sim_card', 'confidence': 0.1740902215242386}, [
            {'start': 0, 'end': 1, 'text': '1', 'value': 1, 'confidence': 1.0,
             'additional_info': {'value': 1, 'type': 'value'}, 'entity': 'number', 'extractor': 'DucklingHTTPExtractor'}]),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"audio": "EN_US/lets_log_in.wav", "group": "login",
                                     "text": "Let's just get you logged in.", "type": "capture_utterance"}},
                   {"template_name": "lets_log_in", "handoff_active": None}),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"audio": "EN_US/midcall_ask_ctn.wav", "grammars": [
                              {"contentId": "MidCall_Ask_CTN.grxml", "grammarFile": "MidCall_Ask_CTN.grxml",
                               "grammarType": "URL"},
                              {"contentId": "MidCall_Ask_CTN_DTMF.grxml", "grammarFile": "MidCall_Ask_CTN_DTMF.grxml",
                               "grammarType": "URL"}], "group": "mid_call_ask_ctn", "max_digits": 11, "min_digits": 0,
                                     "text": "What's the Cricket phone number you're calling about?",
                                     "type": "capture_utterance"}},
                   {"template_name": "utter_ask_mid_call_ask_ctn", "handoff_active": None}),
        UserUttered('5555555', {'name': 'sim_card', 'confidence': 0.1740902215242386}, [
            {'start': 0, 'end': 7, 'text': '5555555', 'value': 5555555, 'confidence': 1.0,
             'additional_info': {'value': 5555555, 'type': 'value'}, 'entity': 'number',
             'extractor': 'DucklingHTTPExtractor'}]),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"audio": "EN_US/midcall_ask_ctn_er1.wav", "grammars": [
                              {"contentId": "MidCall_Ask_CTN.grxml", "grammarFile": "MidCall_Ask_CTN.grxml",
                               "grammarType": "URL"},
                              {"contentId": "MidCall_Ask_CTN_DTMF.grxml", "grammarFile": "MidCall_Ask_CTN_DTMF.grxml",
                               "grammarType": "URL"}], "group": "mid_call_ask_ctn", "max_digits": 11, "min_digits": 0,
                                     "text": "Say or enter the 10-digit wireless number you're calling about",
                                     "type": "capture_utterance"}},
                   {"template_name": "utter_ask_mid_call_ask_ctn_1", "handoff_active": None, "prediction_error": True}),
        UserUttered("", {'name': None, 'confidence': 0.0}, []),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"audio": "EN_US/midcall_ask_ctn_er2.wav", "grammars": [
                              {"contentId": "MidCall_Ask_CTN.grxml", "grammarFile": "MidCall_Ask_CTN.grxml",
                               "grammarType": "URL"},
                              {"contentId": "MidCall_Ask_CTN_DTMF.grxml", "grammarFile": "MidCall_Ask_CTN_DTMF.grxml",
                               "grammarType": "URL"}], "group": "mid_call_ask_ctn", "max_digits": 11, "min_digits": 0,
                                     "text": "Let's try that again. Say, or enter the 10-digit Cricket wireless number. You can also say \"start over\" or press 9, or, \"representative\" or press 0.",
                                     "type": "capture_utterance"}},
                   {"template_name": "utter_ask_mid_call_ask_ctn_2", "handoff_active": None, "prediction_error": True}),
        UserUttered("", {'name': None, 'confidence': 0.0}, []),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"audio": "EN_US/final_err.wav", "group": "error_handling",
                                     "text": "Ok, hang on... Let me get one of our team members to help us out.",
                                     "type": "capture_utterance"}},
                   {"template_name": "utter_final_err", "handoff_active": None, "prediction_error": True}),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"audio": "EN_US/ccpa_disclosure.wav", "barge_in": False, "group": "transfer",
                                     "text": "California customers can request a report on the personal information Cricket has on them, ask us not to sell the information, and ask us to delete it, and find out about the categories of info we collect at cricket wireless dot com slash privacy FAQs",
                                     "type": "capture_utterance"}},
                   {"template_name": "ccpa_disclosure", "handoff_active": None}),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"audio": "EN_US/one_moment.wav,EN_US/recorded.wav", "barge_in": False,
                                     "group": "transfer_2",
                                     "text": "Just a sec. Oh, and by the way, the lawyers want me to tell you that your call might be monitored or recorded.",
                                     "type": "capture_utterance"}},
                   {"template_name": "recording_disclaimer", "handoff_active": None}),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"sip_body": "1231231234|English|None|", "sip_type": "application/racc-out-xh",
                                     "type": "send_sip_info"}},
                   {"template_name": "send_uui_data", "body": "1231231234|English|None|", "handoff_active": None}),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"sip_body": "rdnis:3213214321", "sip_type": "application/racc-vsubst",
                                     "type": "send_sip_info"}},
                   {"template_name": "init_sip_transfer", "rdnis": "3213214321", "handoff_active": None}),
        BotUttered(None, {"elements": None, "quick_replies": None, "buttons": None, "attachment": None, "image": None,
                          "custom": {"action_url": "/sipTransfer", "sip_body": "*8ENGLISH_DEFAULT_SIP#*2",
                                     "sip_type": "application/racc-call-control", "type": "send_sip_info"}},
                   {"template_name": "send_sip_transfer", "call_center": "ENGLISH_DEFAULT_SIP", "handoff_active": None}),
        UserUttered('/disconnect', {'name': 'disconnect', 'confidence': 1.0}, [])
    ]
    tracker = DialogueStateTracker.from_events("sender", events, [], 28)
    events = tracker.events
    for event in list(itertools.islice(events, len(events))):
        tracker.add_conversation_steps(event)
    assert tracker.total_steps == 23


@pytest.mark.parametrize("key, value", [("asfa", 1), ("htb", None)])
def test_tracker_without_slots(key, value, caplog):
    event = SlotSet(key, value)
    tracker = DialogueStateTracker.from_dict("any", [])
    assert key in tracker.slots
    with caplog.at_level(logging.INFO):
        event.apply_to(tracker)
        v = tracker.get_slot(key)
        assert v == value
    assert len(caplog.records) == 0
