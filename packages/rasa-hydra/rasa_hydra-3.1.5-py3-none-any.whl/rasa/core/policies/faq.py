import base64
import json
import logging
import os
import zlib
from typing import Any, Dict, List, Optional, Text

from fuzzywuzzy import fuzz, process
from rasa.core import utils
import rasa.utils.io
from rasa.core.actions.action import ACTION_LISTEN_NAME
from rasa.core.domain import Domain
from rasa.core.events import ActionExecuted
from rasa.core.featurizers import (MaxHistoryTrackerFeaturizer,
                                   TrackerFeaturizer)
from rasa.core.policies.policy import Policy
from rasa.core.trackers import DialogueStateTracker
from tqdm import tqdm

logger = logging.getLogger(__name__)


class FaqPolicy(Policy):
    """The policy that remembers exact examples of
        `max_history` turns from training stories.

        Since `slots` that are set some time in the past are
        preserved in all future feature vectors until they are set
        to None, this policy implicitly remembers and most importantly
        recalls examples in the context of the current dialogue
        longer than `max_history`.

        This policy is not supposed to be the only policy in an ensemble,
        it is optimized for precision and not recall.
        It should get a 100% precision because it emits probabilities of 1.0
        along it's predictions, which makes every mistake fatal as
        no other policy can overrule it.

        If it is needed to recall turns from training dialogues where
        some slots might not be set during prediction time, and there are
        training stories for this, use AugmentedMemoizationPolicy.
    """

    ENABLE_FEATURE_STRING_COMPRESSION = True

    SUPPORTS_ONLINE_TRAINING = True

    USE_NLU_CONFIDENCE_AS_SCORE = False

    def _parse_my_file(self, filename):
        with open(filename) as f:
            for line in f:
                yield line

    def __init__(
        self,
        featurizer: Optional[TrackerFeaturizer] = None,
        questions: Optional[Dict] = None,
    ) -> None:
        self.questions = []
        logger.info("Init FAQ policy")
        for i in self._parse_my_file("faq_q.txt"):
            self.questions.append(i.rstrip("\n"))
        super(FaqPolicy, self).__init__(featurizer=featurizer)

    def train(
        self,
        training_trackers: List[DialogueStateTracker],
        domain: Domain,
        **kwargs: Any
    ) -> None:
        """Trains the policy on given training trackers."""

    def _normalize(self, value):
        norm = (value * 50 / 100) + 50
        return norm

    def _boost(self, x, y=80):
        return (x + y) / (1 + (x * y) / (100 * 100))

    def predict_action_probabilities(
        self, tracker: DialogueStateTracker, domain: Domain
    ) -> List[float]:
        """Predicts the next action the bot should take
            after seeing the tracker.

            Returns the list of probabilities for the next actions.
            If memorized action was found returns 1.0 for its index,
            else returns 0.0 for all actions."""
        result = [0.0] * domain.num_actions

        if tracker.latest_action_name == "action_faq":
            idx = domain.index_for_action(ACTION_LISTEN_NAME)
            result[idx] = 1
        else:
            query = tracker.latest_message.text
            match = process.extract(
                query, self.questions, limit=1, scorer=fuzz.token_sort_ratio
            )[0]

            idx = domain.index_for_action("action_faq")
            norm = self._boost(match[1])
            # print(norm)
            result[idx] = norm / 100
        return result

    def persist(self, path: Text) -> None:

        faq_file = os.path.join(path, "faq.json")
        self.featurizer.persist(path)

        data = {"questions": self.questions}
        rasa.utils.io.create_directory_for_file(config_file)
        rasa.utils.io.dump_obj_as_json_to_file(faq_file, data)

    @classmethod
    def load(cls, path: Text) -> "MemoizationPolicy":

        featurizer = TrackerFeaturizer.load(path)
        faq_file = os.path.join(path, "faq.json")
        if os.path.isfile(faq_file):
            data = json.loads(rasa.utils.io.read_file(faq_file))
            return cls(questions=data["questions"])
        else:
            logger.info(
                "Couldn't load faq for policy. "
                "File '{}' doesn't exist. Falling back to empty "
                "turn memory.".format(faq_file)
            )
            return cls()
