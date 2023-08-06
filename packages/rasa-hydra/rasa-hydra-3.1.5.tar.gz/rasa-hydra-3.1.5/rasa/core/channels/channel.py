import asyncio
import inspect
import json
import logging
import time
import traceback
import uuid
from asyncio import Queue, CancelledError
from os import environ

import aiohttp
import requests

from metrics.constants import OUTGOING_REQUEST_LATENCY_SEC
from rasa.core.utils import AvailableEndpoints
from sanic import Sanic, Blueprint, response
from sanic.request import Request
from typing import Text, List, Dict, Any, Optional, Callable, Iterable, Awaitable

import rasa.utils.endpoints
from rasa.cli import utils as cli_utils
from rasa.constants import DOCS_BASE_URL, ENV_CHANNEL_ID, ENV_OMNI_API_URL
from rasa.core import utils
from sanic.response import HTTPResponse

try:
    from urlparse import urljoin  # pytype: disable=import-error
except ImportError:
    from urllib.parse import urljoin

logger = logging.getLogger(__name__)
OMNI_API_URL = ENV_OMNI_API_URL
CHANNEL_ID = ENV_CHANNEL_ID

class UserMessage:
    """Represents an incoming message.
     Includes the channel the responses should be sent to."""

    DEFAULT_SENDER_ID = "default"

    def __init__(
            self,
            text: Optional[Text] = None,
            output_channel: Optional["OutputChannel"] = None,
            sender_id: Optional[Text] = None,
            parse_data: Dict[Text, Any] = None,
            input_channel: Text = None,
            message_id: Text = None,
            asrConfidence: Dict[Text, Any] = None,
            recordingId: Dict[Text, Any] = None,
            metadata: Optional[Dict] = None,
    ) -> None:
        """Creates a ``UserMessage`` object.
        Args:
            text: the message text content.
            output_channel: the output channel which should be used to send
                bot responses back to the user.
            sender_id: the message owner ID.
            parse_data: rasa data about the message.
            input_channel: the name of the channel which received this message.
            message_id: ID of the message.
            metadata: additional metadata for this message.

        """
        self.text = text.strip() if text else text

        self.recording_id = recordingId
        self.asr_confidence = asrConfidence

        if message_id is not None:
            self.message_id = str(message_id)
        else:
            self.message_id = uuid.uuid4().hex

        if output_channel is not None:
            self.output_channel = output_channel
        else:
            self.output_channel = CollectingOutputChannel()

        if sender_id is not None:
            self.sender_id = str(sender_id)
        else:
            self.sender_id = self.DEFAULT_SENDER_ID

        self.input_channel = input_channel
        self.channel_id = metadata.get('channel_id') if metadata else None

        self.parse_data = parse_data
        self.metadata = metadata


def register(
    input_channels: List["InputChannel"], app: Sanic, route: Optional[Text]
) -> None:
    async def handler(*args, **kwargs):
        sender_id = args[0].sender_id
        
        agent_english = await app.agent[0].tracker_store._tracker_store.retrieve(sender_id)
        agent_spanish = await app.agent[1].tracker_store._tracker_store.retrieve(sender_id)
        lang = 0
        if agent_english and agent_english.slots and agent_english.slots['session_language']:
            lang_val = agent_english.slots['session_language'].value
            if lang_val == 'Spanish':
                lang = 1

        await app.agent[lang].handle_message(*args, **kwargs)

    for channel in input_channels:
        if route:
            p = urljoin(route, channel.url_prefix())
        else:
            p = None
        app.blueprint(channel.blueprint(handler), url_prefix=p)

    app.input_channels = input_channels


class InputChannel:
    _available_endpoints = None

    @classmethod
    def name(cls) -> Text:
        """Every input channel needs a name to identify it."""
        return cls.__name__

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "InputChannel":
        return cls()

    def url_prefix(self) -> Text:
        return self.name()

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[Any]]
    ) -> Blueprint:
        """Defines a Sanic blueprint.
        The blueprint will be attached to a running sanic server and handle
        incoming routes it registered for."""
        raise NotImplementedError("Component listener needs to provide blueprint.")

    @classmethod
    def raise_missing_credentials_exception(cls) -> None:
        raise Exception(
            "To use the {} input channel, you need to "
            "pass a credentials file using '--credentials'. "
            "The argument should be a file path pointing to "
            "a yml file containing the {} authentication "
            "information. Details in the docs: "
            "{}/user-guide/messaging-and-voice-channels/".format(
                cls.name(), cls.name(), DOCS_BASE_URL
            )
        )

    def is_socketio_channel(self):
        return False

    async def disconnect_session(self):
        pass

    @classmethod
    def set_available_endpoints(cls, endpoints: AvailableEndpoints):
        InputChannel._available_endpoints = endpoints

    def get_output_channel(self) -> Optional["OutputChannel"]:
        """Create ``OutputChannel`` based on information provided by the input channel.
        Implementing this function is not required. If this function returns a valid
        ``OutputChannel`` this can be used by Rasa to send bot responses to the user
        without the user initiating an interaction.
        Returns:
            ``OutputChannel`` instance or ``None`` in case creating an output channel
             only based on the information present in the ``InputChannel`` is not
             possible.
        """
        pass

    def get_channel_id(self, channel_name: str):
        start = time.perf_counter()
        resp_status = 500
        channel_id = None
        delay = 5
        max_retries = 3
        retries = 0

        # TO DO: replace env variable with direct sql retrieval of channel HYDRA handles
        # DEPRECATED CODE: makes connection to omni-api to retrieve channel ids
        # while retries < max_retries:
        #     try:
        #         with requests.post(
        #             url=f'{OMNI_API_URL}/getOrCreateChannelId',
        #             data={"channelName": channel_name},
        #             timeout=30,
        #             verify=False
        #         ) as res:
        #             resp_status = res.status_code
        #             resp = res.json()
        #             channel_id = resp.get("channelId", None)
        #             if not channel_id and channel_id != 0:
        #                 raise Exception(f"Unable to parse channel id from the response. Response: {resp}")
        #             else:
        #                 logger.info(f"Channel: {channel_name}, Channel ID: {channel_id}")
        #                 break
        #     except Exception:
        #         retries += 1
        #         logger.warning(f"Failed to get channel id. Retrying in {delay}s...", exc_info=True)
        #         time.sleep(delay)

        # if retries == max_retries:
        #     logger.error(f"Failed to get channel id after {max_retries} retries.")

        # duration = time.perf_counter() - start
        # OUTGOING_REQUEST_LATENCY_SEC.labels(f'{OMNI_API_URL}/getOrCreateChannelId', resp_status, "POST").observe(
        #     duration)
        return CHANNEL_ID

    async def startTracking(self, usg_msg, slots, channel, sid):
        # make IDP request here and append guid to message
        idp_endpoint = InputChannel._available_endpoints.idp

        if idp_endpoint is None:
            logger.warning(
                f'[{sid}] - The endpoint of IDP is not configured. Please make sure you add that to your endpoints.yml!')
            return usg_msg

        idp_url = idp_endpoint.url or "http://localhost:8080"
        tenant_id = idp_endpoint.kwargs.get('tenant_id', '')

        headers = {"Conversation-Id": sid, "Tenant-Id": tenant_id}
        params = {
            "CSI": slots.get("channelUserId"),
            "channel": channel
        }
        msg = usg_msg
        start = time.perf_counter()
        resp_status = 500
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=f'{idp_url}/startTracking',
                    params=params,
                    headers=headers,
                    timeout=30,
                ) as res:
                    resp_status = res.status
                    resp = await res.json()

                    # Reformat the initial string
                    if resp.get('guid'):
                        slots['guid'] = resp.get('guid')
                        msg = "/greet" + json.dumps(slots)
                        logger.info(f"[{sid}] - User tracked by IDP with GUID. Message: {msg}")
                    else:
                        logger.warning(f"[{sid}] - Unable to retrieve guid from IDP: {resp}")
        except Exception as exception:
            logger.warning(f"[{sid}] - Failed to get guid: {str(exception)}")
            slots['guid'] = str(uuid.uuid4())
            msg = "/greet" + json.dumps(slots)
            logger.info(f"[{sid}] - User assigned random GUID. Message: {msg}")

        duration = time.perf_counter() - start
        OUTGOING_REQUEST_LATENCY_SEC.labels(f'{idp_url}/startTracking', resp_status, "POST").observe(duration)

        return msg

    def get_metadata(self, request: Request) -> Optional[Dict[Text, Any]]:
        """Extracts additional information from the incoming request.

         Implementing this function is not required. However, it can be used to extract
         metadata from the request. The return value is passed on to the
         ``UserMessage`` object and stored in the conversation tracker.

        Args:
            request: incoming request with the message of the user

        Returns:
            Metadata which was extracted from the request.
        """
        pass


class OutputChannel:
    """Output channel base class.
    Provides sane implementation of the send methods
    for text only output channels."""

    @classmethod
    def name(cls) -> Text:
        """Every output channel needs a name to identify it."""
        return cls.__name__

    async def send_response(self, recipient_id: Text, message: Dict[Text, Any]) -> None:
        """Send a message to the client."""

        if message.get("quick_replies"):
            await self.send_quick_replies(
                recipient_id,
                message.pop("text"),
                message.pop("quick_replies"),
                **message,
            )
        elif message.get("buttons"):
            await self.send_text_with_buttons(
                recipient_id, message.pop("text"), message.pop("buttons"), **message
            )
        elif message.get("text"):
            await self.send_text_message(recipient_id, message.pop("text"), **message)

        if message.get("custom"):
            await self.send_custom_json(recipient_id, message.pop("custom"), **message)

        # if there is an image we handle it separately as an attachment
        if message.get("image"):
            await self.send_image_url(recipient_id, message.pop("image"), **message)

        if message.get("video"):
            await self.send_video_url(recipient_id, message.pop("video"), **message)

        if message.get("attachment"):
            await self.send_attachment(
                recipient_id, message.pop("attachment"), **message
            )

        if message.get("elements"):
            await self.send_elements(recipient_id, message.pop("elements"), **message)

    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        """Send a message through this channel."""

        raise NotImplementedError(
            "Output channel needs to implement a send message for simple texts."
        )

    async def send_image_url(
        self, recipient_id: Text, image: Text, **kwargs: Any
    ) -> None:
        """Sends an image. Default will just post the url as a string."""

        await self.send_text_message(recipient_id, "Image: {}".format(image), **kwargs)
    
    async def send_video_url(
            self, recipient_id: Text, video: Text, **kwargs: Any
    ) -> None:
        """Sends a video. Default will jsut post the url as a string."""

        await self.send_text_message(recipient_id, "Video: {}".format(video), **kwargs)

    async def send_attachment(
        self, recipient_id: Text, attachment: Text, **kwargs: Any
    ) -> None:
        """Sends an attachment. Default will just post as a string."""

        await self.send_text_message(recipient_id, f"Attachment: {attachment}")

    async def send_text_with_buttons(
        self,
        recipient_id: Text,
        text: Text,
        buttons: List[Dict[Text, Any]],
        **kwargs: Any,
    ) -> None:
        """Sends buttons to the output.
        Default implementation will just post the buttons as a string."""

        await self.send_text_message(recipient_id, text)
        for idx, button in enumerate(buttons):
            button_msg = cli_utils.button_to_string(button, idx)
            await self.send_text_message(recipient_id, button_msg)

    async def send_quick_replies(
        self,
        recipient_id: Text,
        text: Text,
        quick_replies: List[Dict[Text, Any]],
        **kwargs: Any,
    ) -> None:
        """Sends quick replies to the output.
        Default implementation will just send as buttons."""

        await self.send_text_with_buttons(recipient_id, text, quick_replies)

    async def send_elements(
        self, recipient_id: Text, elements: Iterable[Dict[Text, Any]], **kwargs: Any
    ) -> None:
        """Sends elements to the output.
        Default implementation will just post the elements as a string."""

        for element in elements:
            element_msg = "{title} : {subtitle}".format(
                title=element.get("title", ""), subtitle=element.get("subtitle", "")
            )
            await self.send_text_with_buttons(
                recipient_id, element_msg, element.get("buttons", [])
            )

    async def send_custom_json(
        self, recipient_id: Text, json_message: Dict[Text, Any], **kwargs: Any
    ) -> None:
        """Sends json dict to the output channel.
        Default implementation will just post the json contents as a string."""

        await self.send_text_message(recipient_id, json.dumps(json_message))


class CollectingOutputChannel(OutputChannel):
    """Output channel that collects send messages in a list
    (doesn't send them anywhere, just collects them)."""

    def __init__(self) -> None:
        self.messages = []

    @classmethod
    def name(cls) -> Text:
        return "collector"

    @staticmethod
    def _message(
        recipient_id: Text,
        text: Text = None,
        image: Text = None,
        video: Text = None,
        buttons: List[Dict[Text, Any]] = None,
        attachment: Text = None,
        custom: Dict[Text, Any] = None,
    ) -> Dict:
        """Create a message object that will be stored."""

        obj = {
            "recipient_id": recipient_id,
            "text": text,
            "image": image,
            "buttons": buttons,
            "attachment": attachment,
            "custom": custom,
        }

        # filter out any values that are `None`
        return utils.remove_none_values(obj)

    def latest_output(self) -> Optional[Dict[Text, Any]]:
        if self.messages:
            return self.messages[-1]
        else:
            return None

    async def _persist_message(self, message: Dict[Text, Any]) -> None:
        self.messages.append(message)  # pytype: disable=bad-return-type

    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        for message_part in text.split("\n\n"):
            await self._persist_message(self._message(recipient_id, text=message_part))

    async def send_image_url(
        self, recipient_id: Text, image: Text, **kwargs: Any
    ) -> None:
        """Sends an image. Default will just post the url as a string."""

        await self._persist_message(self._message(recipient_id, image=image))

    async def send_video_url(
            self, recipient_id: Text, video: Text, **kwargs: Any
    ) -> None:
        """Sends a video. Default will jsut post the url as a string."""

        await self._persist_message(self._message(recipient_id, video=video))

    async def send_attachment(
        self, recipient_id: Text, attachment: Text, **kwargs: Any
    ) -> None:
        """Sends an attachment. Default will just post as a string."""

        await self._persist_message(self._message(recipient_id, attachment=attachment))

    async def send_text_with_buttons(
        self,
        recipient_id: Text,
        text: Text,
        buttons: List[Dict[Text, Any]],
        **kwargs: Any,
    ) -> None:
        await self._persist_message(
            self._message(recipient_id, text=text, buttons=buttons)
        )

    async def send_custom_json(
        self, recipient_id: Text, json_message: Dict[Text, Any], **kwargs: Any
    ) -> None:
        await self._persist_message(self._message(recipient_id, custom=json_message))


class QueueOutputChannel(CollectingOutputChannel):
    """Output channel that collects send messages in a list
    (doesn't send them anywhere, just collects them)."""

    @classmethod
    def name(cls) -> Text:
        return "queue"

    # noinspection PyMissingConstructor
    def __init__(self, message_queue: Optional[Queue] = None) -> None:
        super().__init__()
        self.messages = Queue() if not message_queue else message_queue

    def latest_output(self):
        raise NotImplementedError("A queue doesn't allow to peek at messages.")

    async def _persist_message(self, message) -> None:
        await self.messages.put(message)  # pytype: disable=bad-return-type


class RestInput(InputChannel):
    """A custom http input channel.
    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa Core and
    retrieve responses from the agent."""

    @classmethod
    def name(cls) -> Text:
        return "rest"

    @staticmethod
    async def on_message_wrapper(
        on_new_message: Callable[[UserMessage], Awaitable[Any]],
        text: Text,
        queue: Queue,
        sender_id: Text,
        input_channel: Text,
        metadata: Optional[Dict[Text, Any]],
    ) -> None:
        collector = QueueOutputChannel(queue)

        message = UserMessage(
            text, collector, sender_id, input_channel=input_channel, metadata=metadata
        )
        await on_new_message(message)

        await queue.put("DONE")  # pytype: disable=bad-return-type

    async def _extract_sender(self, req: Request) -> Optional[Text]:
        return req.json.get("sender", None)

    # noinspection PyMethodMayBeStatic
    def _extract_message(self, req: Request) -> Optional[Text]:
        return req.json.get("message", None)

    def _extract_input_channel(self, req: Request) -> Text:
        return req.json.get("input_channel") or self.name()

    def stream_response(
        self,
        on_new_message: Callable[[UserMessage], Awaitable[None]],
        text: Text,
        sender_id: Text,
        input_channel: Text,
        metadata: Optional[Dict[Text, Any]],
    ) -> Callable[[Any], Awaitable[None]]:
        async def stream(resp: Any) -> None:
            q = Queue()
            task = asyncio.ensure_future(
                self.on_message_wrapper(
                    on_new_message, text, q, sender_id, input_channel, metadata
                )
            )
            result = None  # declare variable up front to avoid pytype error
            while True:
                result = await q.get()
                if result == "DONE":
                    break
                else:
                    await resp.write(json.dumps(result) + "\n")
            await task

        return stream  # pytype: disable=bad-return-type

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        # noinspection PyUnusedLocal
        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            sender_id = await self._extract_sender(request)
            text = self._extract_message(request)
            should_use_stream = rasa.utils.endpoints.bool_arg(
                request, "stream", default=False
            )
            input_channel = self._extract_input_channel(request)
            metadata = self.get_metadata(request)

            if should_use_stream:
                return response.stream(
                    self.stream_response(
                        on_new_message, text, sender_id, input_channel, metadata
                    ),
                    content_type="text/event-stream",
                )
            else:
                collector = CollectingOutputChannel()
                # noinspection PyBroadException
                try:
                    await on_new_message(
                        UserMessage(
                            text,
                            collector,
                            sender_id,
                            input_channel=input_channel,
                            metadata=metadata,
                        )
                    )
                except CancelledError:
                    logger.error(
                        "Message handling timed out for "
                        "user message '{}'.".format(text)
                    )
                except Exception:
                    logger.exception(
                        "An exception occured while handling "
                        "user message '{}'.".format(text)
                    )
                return response.json(collector.messages)

        return custom_webhook