import asyncio
import contextlib
import random
import warnings
import json
import logging
import os
import pickle
import typing
from datetime import datetime, timezone
from typing import Iterator, Optional, Text, Iterable, Union, Dict, Callable

import itertools
import copy
from boto3.dynamodb.conditions import Key

# noinspection PyPep8Naming
import time

import opentracing
from redis import ResponseError
from rediscluster import RedisCluster
from sqlalchemy import select, func, text, Table, MetaData, VARCHAR, bindparam

from metrics.constants import OUTGOING_REQUEST_LATENCY_SEC
from rasa.constants import ENV_AUTHENTICATION_STATE, ENV_DB_SCHEMA, ENV_LOG_LEVEL, ENV_REDIS_SOCKET_TIMEOUT, ENV_SKIP_FULL_COVERAGE_CHECK, ENV_SQL_MAX_OVERFLOW, ENV_SQL_POOL_SIZE, LOG_LEVEL
from rasa.core.actions.action import ACTION_LISTEN_NAME
from rasa.core.brokers.event_channel import EventChannel
from rasa.core.constants import DEFAULT_FALLBACK_ACTION
from rasa.core.conversation import Dialogue
from rasa.core.domain import Domain
from rasa.core.events import SlotSet
from rasa.core.trackers import ActionExecuted, DialogueStateTracker, EventVerbosity
from rasa.core.utils import replace_floats_with_decimals
from rasa.utils.common import class_from_module_path
from rasa.utils.timer import timeit
from rasa.utils.endpoints import EndpointConfig
from rasa.utils.redactor import Redactor

if typing.TYPE_CHECKING:
    from sqlalchemy.engine.url import URL
    from sqlalchemy.engine.base import Engine
    from sqlalchemy.orm import Session
    import boto3

logger = logging.getLogger(__name__)

class TrackerStore:
    """Class to hold all of the TrackerStore classes"""

    def __init__(
            self, domain: Optional[Domain], event_broker: Optional[EventChannel] = None
    ) -> None:
        self.domain = domain
        self.event_broker = event_broker
        self.max_event_history = None
        self.redactor = Redactor()

    @staticmethod
    def find_tracker_store(
            domain: Domain,
            store: Optional[EndpointConfig] = None,
            event_broker: Optional[EventChannel] = None,
    ) -> "TrackerStore":
        """Returns the tracker_store type"""

        tracker_store = None
        if store is not None and store.type is not None:
            try:
                tracker_store = TrackerStore._create_tracker_store(
                    domain, store, event_broker
                )
            except Exception as e:
                logger.error(
                    f"Error when trying to connect to '{store.type}' "
                    f"tracker store. Using "
                    f"'{InMemoryTrackerStore.__name__}'' instead. "
                    f"The causing error was: {e}."
                )

        if not tracker_store:
            tracker_store = InMemoryTrackerStore(domain, event_broker)

        logger.debug("Connected to {}.".format(tracker_store.__class__.__name__))

        return tracker_store

    @staticmethod
    def _create_tracker_store(
            domain: Domain, store: EndpointConfig, event_broker: Optional[EventChannel]
    ) -> "TrackerStore":
        if store.type.lower() == "redis":
            tracker_store = RedisTrackerStore(
                domain=domain, host=store.url, event_broker=event_broker, **store.kwargs
            )
        elif store.type == "redis_cluster":
            tracker_store = RedisClusterTrackerStore(
                domain=domain, host=store.url, event_broker=event_broker, **store.kwargs
            )
        elif store.type.lower() == "mongod":
            tracker_store = MongoTrackerStore(
                domain=domain, host=store.url, event_broker=event_broker, **store.kwargs
            )
        elif store.type.lower() == "sql":
            tracker_store = SQLTrackerStore(
                domain=domain, host=store.url, event_broker=event_broker, **store.kwargs
            )
        elif store.type.lower() == "dynamo":
            tracker_store = DynamoTrackerStore(
                domain=domain, event_broker=event_broker, **store.kwargs
            )
        else:
            tracker_store = TrackerStore.load_tracker_from_module_string(
                domain, store, event_broker
            )

        return tracker_store

    @staticmethod
    def load_tracker_from_module_string(
            domain: Domain,
            store: EndpointConfig,
            event_broker: Optional[EventChannel] = None,
    ) -> "TrackerStore":
        """
        Initializes a custom tracker.

        Args:
            domain: defines the universe in which the assistant operates
            store: the specific tracker store
            event_broker: an event broker to publish events

        Returns:
            custom_tracker: a tracker store from a specified database
            InMemoryTrackerStore: only used if no other tracker store is configured
        """
        custom_tracker = None
        try:
            custom_tracker = class_from_module_path(store.type)
        except (AttributeError, ImportError):
            warnings.warn(
                f"Store type '{store.type}' not found. "
                "Using InMemoryTrackerStore instead"
            )

        if custom_tracker:
            return custom_tracker(
                domain=domain, url=store.url, event_broker=event_broker, **store.kwargs
            )
        else:
            return InMemoryTrackerStore(domain)

    async def get_or_create_tracker(
            self, sender_id: Text, max_event_history: Optional[int] = None
    ) -> "DialogueStateTracker":
        """Returns tracker or creates one if the retrieval returns None"""
        tracker = await self.retrieve(sender_id)
        if max_event_history:
            self.max_event_history = max_event_history
        if tracker is None:
            tracker = await self.create_tracker(sender_id)
        return tracker

    async def init_tracker(self, sender_id: Text) -> "DialogueStateTracker":
        """Returns a Dialogue State Tracker"""
        return DialogueStateTracker(
            sender_id,
            self.domain.slots if self.domain else None,
            max_event_history=self.max_event_history,
        )

    async def create_tracker(
            self, sender_id: Text, append_action_listen: bool = True
    ) -> DialogueStateTracker:
        """Creates a new tracker for the sender_id. The tracker is initially listening."""
        tracker = await self.init_tracker(sender_id)
        if tracker:
            if append_action_listen:
                tracker.update(ActionExecuted(ACTION_LISTEN_NAME))
            await self.save(tracker)
        return tracker

    def save(self, tracker, timeout=None, stream_only=False):
        raise NotImplementedError()

    def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        """Retrieve method that will be overriden by specific tracker"""
        raise NotImplementedError()

    async def _stream_steps(self, tracker: DialogueStateTracker) -> None:
        """Stream steps slot event to a message broker"""
        body = {"sender_id": tracker.sender_id}
        slot_evt = SlotSet('steps', tracker.total_steps)
        body.update(slot_evt.as_dict())
        await self.event_broker.publish(body)

    async def _stream_errors(self, tracker: DialogueStateTracker) -> None:
        """Stream total_errors slot event to a message broker"""
        body = {"sender_id": tracker.sender_id}
        slot_evt = SlotSet('total_errors', tracker.total_errors)
        body.update(slot_evt.as_dict())
        await self.event_broker.publish(body)

    @staticmethod
    def is_form_error(tracker: DialogueStateTracker, evt_dict: dict):
        """Check if there is a form error"""
        form_error = False
        if tracker.active_form:
            form_error = evt_dict.get("event") == "action_execution_rejected"
        return form_error

    @staticmethod
    def is_prediction_error(evt_dict: dict):
        """Check if there is an action prediction error"""
        return evt_dict.get("event") == "action" and (
                evt_dict.get("name") in ["action_handle_error", DEFAULT_FALLBACK_ACTION])

    async def stream_events(self, tracker: DialogueStateTracker) -> None:
        """Streams events to a message broker"""
        offset = await self.number_of_existing_events(tracker.sender_id)
        evts = tracker.events
        start = time.perf_counter()
        form_error = False
        prediction_error = False
        step_number = offset
        for evt in list(itertools.islice(evts, offset, len(evts))):
            body = {"sender_id": tracker.sender_id}
            evt_dict = evt.as_dict()
            metadata = evt_dict.get('metadata', {})
            event_type = evt_dict.get('event')
            evt_text = evt_dict.get('text', None)
            not_disconnect = evt_text != '/disconnect' and evt_text != '/restart'
            
            if len(metadata) > 0:
                should_redact = metadata.get('should_redact', False)
            else:
                should_redact = False
            if str(event_type).lower() == 'user' and not_disconnect:
                if should_redact:
                    evt_dict = self.redactor.redact_event_complete(evt_dict)
                else:
                    evt_dict = self.redactor.redact_event(evt_dict)
            body.update(evt_dict)
            body["step_number"] = step_number
            step_number += 1
            if TrackerStore.is_form_error(tracker, evt_dict):
                form_error = True
            elif TrackerStore.is_prediction_error(evt_dict):
                prediction_error = True
            if body.get("event") == "bot":
                if form_error:
                    body["metadata"]["form_error"] = True
                    form_error = False
                elif prediction_error:
                    body["metadata"]["prediction_error"] = True
                    prediction_error = False
            tracker.add_conversation_steps(evt)
            # This function is shared by other non-async producers, below condition limits async use to AIOKafka.
            if type(self.event_broker).__name__ == "AIOKafkaMiddleware":
                await self.event_broker.publish(body)
            else:
                self.event_broker.publish(body)

        if tracker.conversation_ended():
            await self._stream_steps(tracker)
            await self._stream_errors(tracker)
        duration = time.perf_counter() - start
        OUTGOING_REQUEST_LATENCY_SEC.labels('kafka_stream', "NA", "NA").observe(duration)

    def is_authenticate_state(self, tracker):
        curr_state = tracker.current_state()
        active_form = curr_state.get('active_form')
        return active_form.get('name') == ENV_AUTHENTICATION_STATE

    async def number_of_existing_events(self, sender_id: Text) -> int:
        """Return number of stored events for a given sender id."""
        old_tracker = await self.retrieve(sender_id)
        return len(old_tracker.events) if old_tracker else 0

    def keys(self) -> Iterable[Text]:
        """Returns the set of values for the tracker store's primary key"""
        raise NotImplementedError()

    @staticmethod
    def serialise_tracker(tracker: DialogueStateTracker) -> Text:
        """Serializes the tracker, returns representation of the tracker."""
        dialogue = tracker.as_dialogue()

        return json.dumps(dialogue.as_dict())

    @staticmethod
    def _deserialise_dialogue_from_pickle(
            sender_id: Text, serialised_tracker: bytes
    ) -> Dialogue:

        logger.warning(
            f"Found pickled tracker for "
            f"conversation ID '{sender_id}'. Deserialisation of pickled "
            f"trackers will be deprecated in version 2.0. Rasa will perform any "
            f"future save operations of this tracker using json serialisation."
        )
        return pickle.loads(serialised_tracker)

    async def deserialise_tracker(
            self, sender_id: Text, serialised_tracker: Union[Text, bytes]
    ) -> Optional[DialogueStateTracker]:
        """Deserializes the tracker and returns it."""

        tracker = await self.init_tracker(sender_id)
        if not tracker:
            return None

        try:
            dialogue = Dialogue.from_parameters(json.loads(serialised_tracker))
        except UnicodeDecodeError:
            dialogue = self._deserialise_dialogue_from_pickle(
                sender_id, serialised_tracker
            )

        tracker.recreate_from_dialogue(dialogue)

        return tracker

    def get_channel_timeout(self, channel: str):
        """
        Use 1 hour TTL for the voice channels and 2 hours for everything else.
        :param channel:
        :return: timeout in seconds
        """
        if channel and "voice" in channel.lower():
            return 3600
        else:
            return 7200

    async def is_healthy(self):
        return None


class InMemoryTrackerStore(TrackerStore):
    """Stores conversation history in memory"""

    def __init__(
            self, domain: Domain, event_broker: Optional[EventChannel] = None
    ) -> None:
        self.store = {}
        super().__init__(domain, event_broker)

    async def save(self, tracker: DialogueStateTracker, timeout=None, stream_only=False) -> None:
        if self.event_broker:
            await self.stream_events(tracker)
        serialised = InMemoryTrackerStore.serialise_tracker(tracker)
        self.store[tracker.sender_id] = serialised

    async def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        """
        Args:
            sender_id: the message owner ID

        Returns:
            DialogueStateTracker
        """
        if sender_id in self.store:
            logger.debug(f"Recreating tracker for id '{sender_id}'")
            return await self.deserialise_tracker(sender_id, self.store[sender_id])
        else:
            logger.debug(f"Creating a new tracker for id '{sender_id}'.")
            return None

    async def keys(self) -> Iterable[Text]:
        """Returns sender_ids of the Tracker Store in memory"""
        return self.store.keys()

class RedisTrackerStore(TrackerStore):
    """Stores conversation history in Redis"""

    def __init__(
            self,
            domain,
            host="localhost",
            port=6379,
            db=0,
            password: Optional[Text] = None,
            event_broker: Optional[EventChannel] = None,
            record_exp: Optional[float] = 7200,
            use_ssl: bool = False,
    ):

        import redis

        self.red = redis.StrictRedis(
            host=host, port=port, db=db, password=password, ssl=use_ssl
        )
        self.record_exp = record_exp
        super().__init__(domain, event_broker)

    async def save(self, tracker: DialogueStateTracker, timeout=None, stream_only=False):
        """Saves the current conversation state"""
        if self.event_broker:
            await self.stream_events(tracker)

        if stream_only:
            return

        timeout = self.get_channel_timeout(tracker.get_latest_input_channel())

        if not timeout and self.record_exp:
            timeout = self.record_exp

        serialised_tracker = self.serialise_tracker(tracker)
        self.red.set(tracker.sender_id, serialised_tracker, ex=timeout)

    async def retrieve(self, sender_id):
        """
        Args:
            sender_id: the message owner ID

        Returns:
            DialogueStateTracker
        """
        stored = self.red.get(sender_id)
        if stored is not None:
            return await self.deserialise_tracker(sender_id, stored)
        else:
            return None

    async def keys(self) -> Iterable[Text]:
        """Returns keys of the Redis Tracker Store"""
        return self.red.keys()


class DynamoTrackerStore(TrackerStore):
    """Stores conversation history in DynamoDB"""

    def __init__(
            self,
            domain: Domain,
            table_name: Text = "states",
            region: Text = "us-east-1",
            event_broker: Optional[EndpointConfig] = None,
    ):
        """
        Args:
            domain:
            table_name: The name of the DynamoDb table, does not need to be present a priori.
            event_broker:
        """
        import boto3

        self.client = boto3.client("dynamodb", region_name=region)
        self.region = region
        self.table_name = table_name
        self.db = self.get_or_create_table(table_name)
        super().__init__(domain, event_broker)

    def get_or_create_table(
            self, table_name: Text
    ) -> "boto3.resources.factory.dynamodb.Table":
        """Returns table or creates one if the table name is not in the table list"""
        import boto3

        dynamo = boto3.resource("dynamodb", region_name=self.region)
        if self.table_name not in self.client.list_tables()["TableNames"]:
            table = dynamo.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {"AttributeName": "sender_id", "KeyType": "HASH"},
                    {"AttributeName": "session_date", "KeyType": "RANGE"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "sender_id", "AttributeType": "S"},
                    {"AttributeName": "session_date", "AttributeType": "N"},
                ],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )

            # Wait until the table exists.
            table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
        return dynamo.Table(table_name)

    async def save(self, tracker, timeout=None, stream_only=False):
        """Saves the current conversation state"""
        if self.event_broker:
            await self.stream_events(tracker)
        self.db.put_item(Item=self.serialise_tracker(tracker))

    def serialise_tracker(self, tracker: "DialogueStateTracker") -> Dict:
        """Serializes the tracker, returns object with decimal types"""
        d = tracker.as_dialogue().as_dict()
        d.update(
            {
                "sender_id": tracker.sender_id,
                "session_date": int(datetime.now(tz=timezone.utc).timestamp()),
            }
        )
        return replace_floats_with_decimals(d)

    def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        """Create a tracker from all previously stored events."""

        # Retrieve dialogues for a sender_id in reverse chronological order based on
        # the session_date sort key
        dialogues = self.db.query(
            KeyConditionExpression=Key("sender_id").eq(sender_id),
            Limit=1,
            ScanIndexForward=False,
        )["Items"]
        if dialogues:
            return DialogueStateTracker.from_dict(
                sender_id, dialogues[0].get("events"), self.domain.slots
            )
        else:
            return None

    def keys(self) -> Iterable[Text]:
        """Returns sender_ids of the DynamoTrackerStore"""
        return [
            i["sender_id"]
            for i in self.db.scan(ProjectionExpression="sender_id")["Items"]
        ]


class RedisClusterTrackerStore(TrackerStore):
    async def keys(self) -> Iterable[Text]:
        return self.red_cluster.keys()

    def __init__(
            self,
            domain,
            host="localhost",
            port=6379,
            event_broker=None,
            record_exp=3600,
            max_event_history=None,
            max_connections=32,
    ):
        from rediscluster import RedisCluster
        import threading

        self.startup_nodes = []
        for url in host.split(","):
            hostname = url.split(":")[0]
            port = int(url.split(":")[1])
            self.startup_nodes.append({"host": hostname, "port": port})

        logger.info(f"Redis cluster connection info - {self.startup_nodes}. Max connections: {int(max_connections)}")

        self.max_connections = max_connections
        self.delay = 5
        self.max_retries = 3
        self.socket_timeout = ENV_REDIS_SOCKET_TIMEOUT
        self.skip_full_coverage_check = ENV_SKIP_FULL_COVERAGE_CHECK
        self.health_check_retries = 0
        self.red_cluster = RedisCluster(
            startup_nodes=self.startup_nodes,
            max_connections=int(max_connections),
            retry_on_timeout=False,
            socket_connect_timeout=self.socket_timeout,
            socket_timeout=self.socket_timeout,
            reinitialize_steps=1
        )
        self.record_exp = record_exp
        super(RedisClusterTrackerStore, self).__init__(domain, event_broker)
        self.max_event_history = max_event_history
        self.health_status = True

        health_check_thread = threading.Thread(
            name='redis_health_check_thread',
            target=self.custom_ping,
            args=(),
            daemon=True
        )
        logger.info("Starting redis cluster health check thread...")
        health_check_thread.start()

    async def init_tracker(self, sender_id):
        return DialogueStateTracker(
            sender_id,
            self.domain.slots if self.domain else None,
            max_event_history=self.max_event_history,
        )

    async def recreate_connection(self):
        logger.info("Recreating connection to the Redis cluster...")
        try:
            self.red_cluster = RedisCluster(
                startup_nodes=self.startup_nodes,
                max_connections=int(self.max_connections),
                retry_on_timeout=False,
                socket_connect_timeout=self.socket_timeout,
                socket_timeout=self.socket_timeout,
                reinitialize_steps=1
            )
            return True
        except Exception as exp:
            logger.warning(f"Failed to recreate connection to the redis cluster. Error: {exp}")
            return False

    async def execute_commands(self, command: str, key=None, value=None, ex=None):
        current_retries = 0
        res = None
        while current_retries < self.max_retries:
            try:
                pipeline = self.red_cluster.pipeline()
                if command == "SET":
                    pipeline.set(key, value, ex=ex)
                elif command == "GET":
                    pipeline.get(key)
                elif command == "DELETE":
                    pipeline.delete(key)
                elif command == "PING":
                    pipeline.ping()
                else:
                    raise Exception(f"Unrecognized predefined redis execute commands. Given command: {command}")

                res = pipeline.execute()
                if res and isinstance(res, list) and len(res) > 0:
                    res = res[0]
                    if isinstance(res, ResponseError):
                        raise Exception(f"Unexpected redis response: {res}")

                self.health_status = True
                if current_retries > 0:
                    logger.info(f"Reconnected to the Redis cluster after {current_retries} retries.")

                break
            except Exception as exp:
                res = None
                current_retries += 1
                sleep_time = self.delay * current_retries
                logger.warning(
                    f'[REDIS_CLUSTER_ERROR] - Failed to execute Redis commands, retry in {sleep_time}s. Error: {exp}')
                time.sleep(sleep_time)
                res = await self.recreate_connection()

        if current_retries == self.max_retries:
            self.health_status = False
            logger.error(f"[REDIS_CLUSTER_ERROR] - Unable to execute Redis commands after {self.max_retries} retries.")

        return res

    async def save(self, tracker: DialogueStateTracker, timeout=None, stream_only=False):
        if self.event_broker:
            await self.stream_events(tracker)

        if stream_only:
            return

        timeout = self.get_channel_timeout(tracker.get_latest_input_channel())
        if not timeout and self.record_exp:
            timeout = self.record_exp

        serialised_tracker = self.serialise_tracker(tracker)
        start = time.perf_counter()
        await self.execute_commands("SET", tracker.sender_id, serialised_tracker, timeout)

        # self.red_cluster.set(f'sid_{tracker.sender_id}', '', ex=timeout)
        duration = time.perf_counter() - start
        OUTGOING_REQUEST_LATENCY_SEC.labels('redis_save', "NA", "NA").observe(duration)

    async def retrieve(self, sender_id):
        start = time.perf_counter()
        stored = await self.execute_commands("GET", sender_id)
        duration = time.perf_counter() - start
        OUTGOING_REQUEST_LATENCY_SEC.labels('redis_get', "NA", "NA").observe(duration)

        if stored is not None:
            return await self.deserialise_tracker(sender_id, stored)
        else:
            return None

    async def delete(self, sender_id):
        return await self.execute_commands("DELETE", sender_id)

    async def ping(self):
        return await self.execute_commands("PING")

    def custom_ping(self):
        while True:
            try:
                pipeline = self.red_cluster.pipeline()
                rand_int = random.randint(1, 10000)
                pipeline.set(f"PING_{rand_int}", "", ex=10)
                res = pipeline.execute()
                if len(res) > 0:
                    res = res[0]
                    if isinstance(res, ResponseError):
                        raise Exception(f"Unexpected redis response: {res}")

                self.health_status = True
                if self.health_check_retries > 0:
                    self.health_check_retries = 0
                    logger.info(f"Reconnected to the Redis cluster after {self.health_check_retries} retries.")

            except Exception as exp:
                self.health_check_retries += 1
                logger.warning(
                    f'[REDIS_CLUSTER_ERROR] - Failed to ping Redis, error count: {self.health_check_retries}. Error: {exp}')
                self.recreate_connection()

            time.sleep(10)
            if self.health_check_retries == self.max_retries:
                self.health_status = False
                logger.error(
                    f"[REDIS_CLUSTER_ERROR] - Unable to execute Redis commands after {self.max_retries} retries.")

    async def is_healthy(self):
        return self.health_status


class MongoTrackerStore(TrackerStore):
    """
    Stores conversation history in Mongo

    Property methods:
        conversations: returns the current conversation
    """

    def __init__(
            self,
            domain: Domain,
            host: Optional[Text] = "mongodb://localhost:27017",
            db: Optional[Text] = "rasa",
            username: Optional[Text] = None,
            password: Optional[Text] = None,
            auth_source: Optional[Text] = "admin",
            collection: Optional[Text] = "conversations",
            event_broker: Optional[EventChannel] = None,
    ):
        from pymongo.database import Database
        from pymongo import MongoClient

        self.client = MongoClient(
            host,
            username=username,
            password=password,
            authSource=auth_source,
            # delay connect until process forking is done
            connect=False,
        )

        self.db = Database(self.client, db)
        self.collection = collection
        super().__init__(domain, event_broker)

        self._ensure_indices()

    @property
    def conversations(self):
        """Returns the current conversation"""
        return self.db[self.collection]

    def _ensure_indices(self):
        """Create an index on the sender_id"""
        self.conversations.create_index("sender_id")

    async def save(self, tracker, timeout=None, stream_only=False):
        """Saves the current conversation state"""
        if self.event_broker:
            await self.stream_events(tracker)

        state = tracker.current_state(EventVerbosity.ALL)

        self.conversations.update_one(
            {"sender_id": tracker.sender_id}, {"$set": state}, upsert=True
        )

    def retrieve(self, sender_id):
        """
        Args:
            sender_id: the message owner ID

        Returns:
            `DialogueStateTracker`
        """
        stored = self.conversations.find_one({"sender_id": sender_id})

        # look for conversations which have used an `int` sender_id in the past
        # and update them.
        if stored is None and sender_id.isdigit():
            from pymongo import ReturnDocument

            stored = self.conversations.find_one_and_update(
                {"sender_id": int(sender_id)},
                {"$set": {"sender_id": str(sender_id)}},
                return_document=ReturnDocument.AFTER,
            )

        if stored is not None:
            return DialogueStateTracker.from_dict(
                sender_id, stored.get("events"), self.domain.slots
            )
        else:
            return None

    def keys(self) -> Iterable[Text]:
        """Returns sender_ids of the Mongo Tracker Store"""
        return [c["sender_id"] for c in self.conversations.find()]


class SQLTrackerStore(TrackerStore):
    """Store which can save and retrieve trackers from an SQL database."""

    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class SQLEvent(Base):
        """Represents an event in the SQL Tracker Store"""

        from sqlalchemy import Column, Integer, String, Float, Text

        __tablename__ = "events"

        id = Column(Integer, primary_key=True)
        sender_id = Column(String(255, convert_unicode='force'), nullable=False, index=True)
        type_name = Column(String(255, convert_unicode='force'), nullable=False)
        timestamp = Column(Float, nullable=False)
        intent_name = Column(String(255, convert_unicode='force'))
        action_name = Column(String(255, convert_unicode='force'))
        data = Column(Text(None, convert_unicode='force'), nullable=False)
        table = Table(
            __tablename__,
            MetaData(schema=ENV_DB_SCHEMA),
            Column('id', Integer, primary_key=True),
            Column('sender_id', String(255, convert_unicode='force'), nullable=False, index=True),
            Column('type_name', String(255, convert_unicode='force'), nullable=False),
            Column('timestamp', Float, nullable=False),
            Column('intent_name', String(255, convert_unicode='force')),
            Column('action_name', String(255, convert_unicode='force')),
            Column('data', Text(None, convert_unicode='force'), nullable=False)
        )

    def __init__(
            self,
            domain: Optional[Domain] = None,
            dialect: Text = "sqlite",
            host: Optional[Text] = None,
            port: Optional[int] = None,
            db: Text = "rasa.db",
            username: Text = None,
            password: Text = None,
            event_broker: Optional[EventChannel] = None,
            login_db: Optional[Text] = None,
            query: Optional[Dict] = None,
    ) -> None:
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import create_engine
        import sqlalchemy.exc

        engine_url = self.get_db_url(
            dialect, host, port, db, username, password, login_db, query
        )
        echo_query = ENV_LOG_LEVEL == "DEBUG"
        logger.debug(
            "Attempting to connect to database via '{}'.".format(repr(engine_url))
        )
        self.DB_SCHEMA = ENV_DB_SCHEMA
        self.event_time_range = 14400  # 4 hours

        # Database might take a while to come up
        while True:
            try:
                # pool_size and max_overflow can be set to control the number of
                # connections that are kept in the connection pool. Not available
                # for SQLite, and only  tested for postgresql. See
                # https://docs.sqlalchemy.org/en/13/core/pooling.html#sqlalchemy.pool.QueuePool
                if dialect == "postgresql":
                    self.engine = create_engine(
                        engine_url,
                        pool_size=ENV_SQL_POOL_SIZE,
                        max_overflow=ENV_SQL_MAX_OVERFLOW,
                    )
                elif dialect == 'pymssql':
                    self.engine = create_engine(f'mssql+pymssql://{username}:{password}@{host}/{db}?charset=utf8',
                                                pool_size=ENV_SQL_POOL_SIZE,
                                                max_overflow=ENV_SQL_MAX_OVERFLOW,
                                                echo=echo_query,
                                                isolation_level='AUTOCOMMIT')
                    logger.info(
                        f"Connected to the MSSQL tracker store: mssql+pymssql://{username}:{password}@{host}/{db}?charset=utf8")
                else:
                    self.engine = create_engine(engine_url)

                # if `login_db` has been provided, use current channel with
                # that database to create working database `db`
                if login_db:
                    self._create_database_and_update_engine(db, engine_url)

                try:
                    self.Base.metadata.create_all(self.engine)
                except (
                        sqlalchemy.exc.OperationalError,
                        sqlalchemy.exc.ProgrammingError,
                ) as e:
                    # Several Rasa services started in parallel may attempt to
                    # create tables at the same time. That is okay so long as
                    # the first services finishes the table creation.
                    logger.error(f"Could not create tables: {e}")

                self.sessionmaker = sessionmaker(bind=self.engine)
                break
            except (
                    sqlalchemy.exc.OperationalError,
                    sqlalchemy.exc.IntegrityError,
            ) as error:

                logger.warning(error)
                asyncio.sleep(5)

        logger.debug(f"Connection to SQL database '{db}' successful.")

        super().__init__(domain, event_broker)

    @staticmethod
    def get_db_url(
            dialect: Text = "sqlite",
            host: Optional[Text] = None,
            port: Optional[int] = None,
            db: Text = "rasa.db",
            username: Text = None,
            password: Text = None,
            login_db: Optional[Text] = None,
            query: Optional[Dict] = None,
    ) -> Union[Text, "URL"]:
        """Builds an SQLAlchemy `URL` object representing the parameters needed
        to connect to an SQL database.

        Args:
            dialect: SQL database type.
            host: Database network host.
            port: Database network port.
            db: Database name.
            username: User name to use when connecting to the database.
            password: Password for database user.
            login_db: Alternative database name to which initially connect, and create
                the database specified by `db` (PostgreSQL only).
            query: Dictionary of options to be passed to the dialect and/or the
                DBAPI upon connect.

        Returns:
            URL ready to be used with an SQLAlchemy `Engine` object.

        """
        from urllib.parse import urlsplit
        from sqlalchemy.engine.url import URL

        # Users might specify a url in the host
        parsed = urlsplit(host or "")
        if parsed.scheme:
            return host

        if host:
            # add fake scheme to properly parse components
            parsed = urlsplit("schema://" + host)

            # users might include the port in the url
            port = parsed.port or port
            host = parsed.hostname or host

        return URL(
            dialect,
            username,
            password,
            host,
            port,
            database=login_db if login_db else db,
            query=query,
        )

    def _create_database_and_update_engine(self, db: Text, engine_url: "URL"):
        """Create databse `db` and update engine to reflect the updated `engine_url`."""

        from sqlalchemy import create_engine

        self._create_database(self.engine, db)
        engine_url.database = db
        self.engine = create_engine(engine_url)

    @staticmethod
    def _create_database(engine: "Engine", db: Text):
        """Create database `db` on `engine` if it does not exist."""

        import psycopg2

        conn = engine.connect()

        cursor = conn.connection.cursor()
        cursor.execute("COMMIT")
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db}'")
        exists = cursor.fetchone()
        if not exists:
            try:
                cursor.execute(f"CREATE DATABASE {db}")
            except psycopg2.IntegrityError as e:
                logger.error(f"Could not create database '{db}': {e}")

        cursor.close()
        conn.close()

    @contextlib.contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.sessionmaker()
        try:
            yield session
        finally:
            session.close()

    async def is_healthy(self):
        start = time.perf_counter()
        try:
            with self.engine.connect() as connection:
                return connection.execute("SELECT 1")
        except Exception:
            logger.error("SQL Tracker store is not healthy", exc_info=True)
            return None
        finally:
            duration = time.perf_counter() - start
            OUTGOING_REQUEST_LATENCY_SEC.labels('sql_healthcheck', "NA", "NA").observe(duration)

    def keys(self) -> Iterable[Text]:
        """Returns sender_ids of the SQLTrackerStore"""
        with self.session_scope() as session:
            sender_ids = session.query(self.SQLEvent.sender_id).distinct().all()
            return [sender_id for (sender_id,) in sender_ids]

    # Comment out the original method for now
    # def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
    #     """Create a tracker from all previously stored events."""
    #
    #     with self.session_scope() as session:
    #         query = session.query(self.SQLEvent)
    #         result = (
    #             query.filter_by(sender_id=sender_id)
    #             .order_by(self.SQLEvent.timestamp)
    #             .all()
    #         )
    #
    #         events = [json.loads(event.data) for event in result]
    #
    #         if self.domain and len(events) > 0:
    #             logger.debug(f"Recreating tracker from sender id '{sender_id}'")
    #             return DialogueStateTracker.from_dict(
    #                 sender_id, events, self.domain.slots
    #             )
    #         else:
    #             logger.debug(
    #                 "Can't retrieve tracker matching "
    #                 "sender id '{}' from SQL storage. "
    #                 "Returning `None` instead.".format(sender_id)
    #             )
    #             return None
    #
    # def save(self, tracker: DialogueStateTracker, timeout=None, stream_only=False) -> None:
    #     """Update database with events from the current conversation."""
    #
    #     if self.event_broker:
    #         self.stream_events(tracker)
    #
    #     with self.session_scope() as session:
    #         # only store recent events
    #         events = self._additional_events(session, tracker)
    #
    #         for event in events:
    #             data = event.as_dict()
    #
    #             intent = data.get("parse_data", {}).get("intent", {}).get("name")
    #             action = data.get("name")
    #             timestamp = data.get("timestamp")
    #
    #             # noinspection PyArgumentList
    #             session.add(
    #                 self.SQLEvent(
    #                     sender_id=tracker.sender_id,
    #                     type_name=event.type_name,
    #                     timestamp=timestamp,
    #                     intent_name=intent,
    #                     action_name=action,
    #                     data=json.dumps(data),
    #                 )
    #             )
    #         session.commit()
    #
    #     logger.debug(
    #         "Tracker with sender_id '{}' "
    #         "stored to database".format(tracker.sender_id)
    #     )
    #
    # def _additional_events(
    #     self, session: "Session", tracker: DialogueStateTracker
    # ) -> Iterator:
    #     """Return events from the tracker which aren't currently stored."""
    #
    #     n_events = (
    #         session.query(self.SQLEvent.sender_id)
    #         .filter_by(sender_id=tracker.sender_id)
    #         .count()
    #         or 0
    #     )

    def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        """Create a tracker from all previously stored events. (Using sqlalchemy core instead of ORM.)"""
        start = time.perf_counter()
        with self.engine.connect().execution_options(autocommit=True) as connection:
            end_time = time.time()
            start_time = end_time - self.event_time_range  # 4 hours ago
            stmt = f"declare @sql nvarchar(MAX), @p0 varchar(255), @p1 float, @p2 float" \
                   f" set @sql = N'SELECT * FROM {self.DB_SCHEMA}.{self.SQLEvent.__tablename__} (NOLOCK) WHERE sender_id=@p0 AND timestamp BETWEEN @p1 AND @p2 ORDER BY timestamp'" \
                   f" set @p0='{sender_id}'" \
                   f" set @p1={start_time}" \
                   f" set @p2={end_time}" \
                   f" execute dbo.sp_executesql @sql, N'@p0 varchar(255),@p1 float, @p2 float',@p0,@p1,@p2"

            result = connection.execute(stmt).fetchall()
            duration = time.perf_counter() - start
            OUTGOING_REQUEST_LATENCY_SEC.labels('sql_retrieve', "NA", "NA").observe(duration)

            events = [json.loads(event.data) for event in result]

            if self.domain and len(events) > 0:
                logger.debug(f"Recreating tracker from sender id '{sender_id}'")
                return DialogueStateTracker.from_dict(
                    sender_id, events, self.domain.slots
                )
            else:
                logger.debug(
                    "Can't retrieve tracker matching "
                    "sender id '{}' from SQL storage. "
                    "Returning `None` instead.".format(sender_id)
                )
                return None

    async def save(self, tracker: DialogueStateTracker, timeout=None, stream_only=False) -> None:
        """Update database with events from the current conversation. (Using sqlalchemy core instead of ORM.)"""

        if self.event_broker:
            await self.stream_events(tracker)

        with self.engine.connect().execution_options(autocommit=True) as connection:
            # only store recent events
            events = self._additional_events(connection, tracker)
            events_list = []

            for event in events:
                data = event.as_dict()
                data["total_steps"] = tracker.total_steps
                data["total_errors"] = tracker.total_errors

                intent = data.get("parse_data", {}).get("intent", {}).get("name")
                action = data.get("name")
                timestamp = data.get("timestamp")
                event_data = {
                    "sender_id": tracker.sender_id,
                    "type_name": event.type_name,
                    "timestamp": timestamp,
                    "intent_name": intent,
                    "action_name": action,
                    "data": json.dumps(data),
                }
                events_list.append(event_data)
            if len(events_list) > 0:
                stmt = self.SQLEvent.table.insert().values(
                    sender_id=bindparam("sender_id"),
                    type_name=bindparam("type_name"),
                    timestamp=bindparam("timestamp"),
                    intent_name=bindparam("intent_name"),
                    action_name=bindparam("action_name"),
                    data=bindparam("data"),
                )
                start = time.perf_counter()
                connection.execute(stmt, events_list)
                duration = time.perf_counter() - start
                OUTGOING_REQUEST_LATENCY_SEC.labels('sql_save', "NA", "NA").observe(duration)

        logger.debug(
            "Tracker with sender_id '{}' "
            "stored to database".format(tracker.sender_id)
        )

    def _additional_events(
            self, connection: None, tracker: DialogueStateTracker
    ) -> Iterator:
        """Return events from the tracker which aren't currently stored. (Using sqlalchemy core instead of ORM.)"""
        end_time = time.time()
        start_time = end_time - self.event_time_range
        sql_start_time = time.perf_counter()
        stmt = f"SELECT COUNT(*) FROM {self.DB_SCHEMA}.{self.SQLEvent.__tablename__} (NOLOCK) WHERE sender_id='{tracker.sender_id}'" \
               f" AND timestamp BETWEEN {start_time} AND {end_time}"
        n_events = connection.execute(stmt).fetchone()
        duration = time.perf_counter() - sql_start_time
        OUTGOING_REQUEST_LATENCY_SEC.labels('sql_retrieve', "NA", "NA").observe(duration)
        if len(n_events) > 0:
            n_events = n_events[0]
        else:
            n_events = 0

        return itertools.islice(tracker.events, n_events, len(tracker.events))


class FailSafeTrackerStore(TrackerStore):
    """Wraps a tracker store so that we can fallback to a different tracker store in
    case of errors."""

    def __init__(
            self,
            tracker_store: TrackerStore,
            on_tracker_store_error: Optional[Callable[[Exception], None]] = None,
            fallback_tracker_store: Optional[TrackerStore] = None,
    ) -> None:
        """Create a `FailSafeTrackerStore`.

        Args:
            tracker_store: Primary tracker store.
            on_tracker_store_error: Callback which is called when there is an error
                in the primary tracker store.
        """

        self._fallback_tracker_store: Optional[TrackerStore] = fallback_tracker_store
        self._tracker_store = tracker_store
        self._on_tracker_store_error = on_tracker_store_error

        super().__init__(tracker_store.domain, tracker_store.event_broker)

    @property
    def domain(self) -> Optional[Domain]:
        return self._tracker_store.domain

    @domain.setter
    def domain(self, domain: Optional[Domain]) -> None:
        self._tracker_store.domain = domain

        if self._fallback_tracker_store:
            self._fallback_tracker_store.domain = domain

    @property
    def fallback_tracker_store(self) -> TrackerStore:
        if not self._fallback_tracker_store:
            self._fallback_tracker_store = InMemoryTrackerStore(
                self._tracker_store.domain, self._tracker_store.event_broker
            )

        return self._fallback_tracker_store

    def on_tracker_store_error(self, error: Exception) -> None:
        if self._on_tracker_store_error:
            self._on_tracker_store_error(error)
        else:
            logger.error(
                f"Error happened when trying to save conversation tracker to "
                f"'{self._tracker_store.__class__.__name__}'. Falling back to use "
                f"the '{InMemoryTrackerStore.__name__}'. Please "
                f"investigate the following error: {error}."
            )

    async def retrieve(self, sender_id: Text) -> Optional[DialogueStateTracker]:
        try:
            return await self._tracker_store.retrieve(sender_id)
        except Exception as e:
            self.on_tracker_store_error(e)
            return None

    async def keys(self) -> Iterable[Text]:
        try:
            return await self._tracker_store.keys()
        except Exception as e:
            self.on_tracker_store_error(e)
            return []

    async def save(self, tracker: DialogueStateTracker, timeout=None, stream_only=False) -> None:
        try:
            await self._tracker_store.save(tracker, stream_only=stream_only)
        except Exception as e:
            self.on_tracker_store_error(e)
            await self.fallback_tracker_store.save(tracker)

    async def is_healthy(self):
        return await self._tracker_store.is_healthy()
