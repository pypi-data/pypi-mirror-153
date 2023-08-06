import copy
import logging
import re
import json
from collections import defaultdict

from rasa.core.trackers import DialogueStateTracker
from typing import Text, Any, Dict, Optional, List

from rasa.core.nlg.generator import NaturalLanguageGenerator
from rasa.core.nlg.interpolator import interpolate_text, interpolate
from rasa.utils.timer import timeit

from rasa.core.events import SlotSet

logger = logging.getLogger(__name__)


class TemplatedNaturalLanguageGenerator(NaturalLanguageGenerator):
    """Natural language generator that generates messages based on templates.

    The templates can use variables to customize the utterances based on the
    state of the dialogue."""

    def __init__(self, templates: Dict[Text, List[Dict[Text, Any]]]) -> None:
        self.templates = templates

    def _templates_for_utter_action(self, utter_action, output_channel):
        """Return array of templates that fit the channel and action."""

        channel_templates = []
        default_templates = []

        for template in self.templates[utter_action]:
            if template.get("channel") == output_channel:
                channel_templates.append(template)
            elif not template.get("channel"):
                default_templates.append(template)

        # always prefer channel specific templates over default ones
        if channel_templates:
            return channel_templates
        else:
            return default_templates

    # noinspection PyUnusedLocal
    def _random_template_for(
        self, utter_action: Text, output_channel: Text
    ) -> Optional[Dict[Text, Any]]:
        """Select random template for the utter action from available ones.

        If channel-specific templates for the current output channel are given,
        only choose from channel-specific ones.
        """
        import numpy as np

        if utter_action in self.templates:
            suitable_templates = self._templates_for_utter_action(
                utter_action, output_channel
            )

            if suitable_templates:
                return np.random.choice(suitable_templates)
            else:
                return None
        else:
            return None

    # @timeit
    async def generate(
        self,
        template_name: Text,
        tracker: DialogueStateTracker,
        output_channel: Text,
        **kwargs: Any,
    ) -> Optional[Dict[Text, Any]]:
        """Generate a response for the requested template."""

        filled_slots = tracker.current_slot_values()
        template = self.generate_from_slots(
            template_name, filled_slots, output_channel, **kwargs
        )
        if not tracker.get_slot('private_call'):
            if template and template.get('custom', {}).get('privacy_mode', None):
                tracker.update(SlotSet('private_call', True))

        return template
            

    def generate_from_slots(
        self,
        template_name: Text,
        filled_slots: Dict[Text, Any],
        output_channel: Text,
        **kwargs: Any,
    ) -> Optional[Dict[Text, Any]]:
        """Generate a response for the requested template."""

        # Fetching a random template for the passed template name
        r = copy.deepcopy(self._random_template_for(template_name, output_channel))
        # Filling the slots in the template and returning the template
        if r is not None:
            return self._fill_template(r, filled_slots, **kwargs)
        else:
            return None

    def _fill_template(
        self,
        template: Dict[Text, Any],
        filled_slots: Optional[Dict[Text, Any]] = None,
        **kwargs: Any,
    ) -> Dict[Text, Any]:
        """"Combine slot values and key word arguments to fill templates."""

        # Getting the slot values in the template variables
        template_vars = self._template_variables(filled_slots, kwargs)

        keys_to_interpolate = [
            "text",
            "image",
            "custom",
            "button",
            "attachment",
            "quick_replies",
        ]
        # Filling the template variables in the template text
        if template_vars and "text" in template:
            try:
                # transforming template tags from
                # "{tag_name}" to "{0[tag_name]}"
                # as described here:
                # https://stackoverflow.com/questions/7934620/python-dots-in-the-name-of-variable-in-a-format-string#comment9695339_7934969
                # assuming that slot_name do not contain newline character here
                text = re.sub(r"{([^\n]+?)}", r"{0[\1]}", template["text"])
                template["text"] = text.format(template_vars)
            except KeyError as e:
                logger.exception(
                    "Failed to fill utterance template '{}'. "
                    "Tried to replace '{}' but could not find "
                    "a value for it. There is no slot with this "
                    "name nor did you pass the value explicitly "
                    "when calling the template. Return template "
                    "without filling the template. "
                    "".format(template, e.args[0])
                )
        if template_vars and "custom" in template:
            try:
                self.iterateNestedDict(template["custom"], template_vars)
                # transforming template tags from
                # "{tag_name}" to "{0[tag_name]}"
                # as described here:
                # https://stackoverflow.com/questions/7934620/python-dots-in-the-name-of-variable-in-a-format-string#comment9695339_7934969
                # assuming that slot_name do not contain newline character here
            except KeyError as e:
                logger.exception(
                    "Failed to fill utterance template '{}'. "
                    "Tried to replace '{}' but could not find "
                    "a value for it. There is no slot with this "
                    "name nor did you pass the value explicitly "
                    "when calling the template. Return template "
                    "without filling the template. "
                    "".format(template, e.args[0])
                )
        if template_vars:
            for key in keys_to_interpolate:
                if key in template:
                    template[key] = interpolate(template[key], template_vars)

        # Inject the language attribute into the template based on the current session_language
        if template.get('custom'):
            template['custom']['language'] = template_vars.get('session_language') or 'English'
            
        return template

    def iterateNestedDict(self, custom: Dict[Text, Any], template_vars: Dict[Text, Any]):
        for k, v in custom.items():
            if isinstance(v, dict):
                self.iterateNestedDict(v, template_vars)
            elif isinstance(v, list):
                self.iterateNestedList(v, template_vars)
            else:
                if k in ['text', 'isVisible', 'file']:
                    v = re.sub(r"{([^\n]+?)}", r"{0[\1]}", v)
                    v = v.format(template_vars)
                    custom[k] = v

    def iterateNestedList(self, custom: List, template_vars: Dict[Text, Any]):
        for i in custom:
            if isinstance(i, list):
                self.iterateNestedList(i, template_vars)
            elif isinstance(i, dict):
                self.iterateNestedDict(i, template_vars)

    @staticmethod
    def _template_variables(
        filled_slots: Dict[Text, Any], kwargs: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Combine slot values and key word arguments to fill templates."""

        if filled_slots is None:
            filled_slots = {}

        # Copying the filled slots in the template variables.
        template_vars = filled_slots.copy()
        template_vars.update(kwargs)
        return template_vars
