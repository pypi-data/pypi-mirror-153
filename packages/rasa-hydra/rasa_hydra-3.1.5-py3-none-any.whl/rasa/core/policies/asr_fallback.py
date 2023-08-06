import json
import logging
import os
from typing import Any, List, Text

from rasa.core.actions.action import ACTION_LISTEN_NAME

from rasa.core import utils
import rasa.utils.io
from rasa.core.domain import Domain
from rasa.core.policies.policy import Policy
from rasa.core.trackers import DialogueStateTracker
FALLBACK_SCORE = 1.5

logger = logging.getLogger(__name__)


class AsrFallbackPolicy(Policy):
    """Policy which predicts fallback actions.

    A fallback can be triggered by a low confidence score on a
    NLU prediction or by a low confidence score on an action
    prediction. """

    @staticmethod
    def _standard_featurizer():
        return None

    def __init__(self,
                 priority: int = 6,
                 nlu_threshold: float = 0.3,
                 core_threshold: float = 0.3,
                 fallback_action_name: Text = "action_asr_fallback"
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

        super(AsrFallbackPolicy, self).__init__(priority=priority)

        self.nlu_threshold = nlu_threshold
        self.core_threshold = core_threshold
        self.fallback_action_name = fallback_action_name

    def train(self,
              training_trackers: List[DialogueStateTracker],
              domain: Domain,
              **kwargs: Any
              ) -> None:
        """Does nothing. This policy is deterministic."""

        pass

    def should_fallback(self,
                        nlu_confidence: float,
                        last_action_name: Text
                        ) -> bool:
        """It should predict fallback action only if
        a. predicted NLU confidence is lower than ``nlu_threshold`` &&
        b. last action is NOT fallback action
        """
        return (nlu_confidence < self.nlu_threshold and
                last_action_name != self.fallback_action_name)

    def fallback_scores(self, domain, fallback_score=FALLBACK_SCORE):
        """Prediction scores used if a fallback is necessary."""

        result = [0.0] * domain.num_actions
        idx = domain.index_for_action(self.fallback_action_name)
        result[idx] = fallback_score
        return result

    def predict_action_probabilities(self,
                                     tracker: DialogueStateTracker,
                                     domain: Domain) -> List[float]:
        """Predicts a fallback action if NLU confidence is low
            or no other policy has a high-confidence prediction"""

        nlu_data = tracker.latest_message.parse_data

        # if NLU interpreter does not provide confidence score,
        # it is set to 1.0 here in order
        # to not override standard behaviour
        asr_confidence = float(1.0)
        try:
            asr_confidence = float(nlu_data["asrConfidence"])
        except KeyError:
            pass


        if tracker.latest_action_name == self.fallback_action_name:
            result = [0.0] * domain.num_actions
            idx = domain.index_for_action(ACTION_LISTEN_NAME)
            result[idx] = FALLBACK_SCORE

        elif self.should_fallback(asr_confidence, tracker.latest_action_name):
            logger.debug("NLU confidence {} is lower "
                         "than NLU threshold {}. "
                         "Predicting fallback action: {}"
                         "".format(asr_confidence, self.nlu_threshold,
                                   self.fallback_action_name))
            # we set this to 1.1 to make sure fallback overrides
            # the memoization policy
            result = self.fallback_scores(domain)
        else:
            # NLU confidence threshold is met, so
            # predict fallback action with confidence `core_threshold`
            # if this is the highest confidence in the ensemble,
            # the fallback action will be executed.
            result = self.fallback_scores(domain, self.core_threshold)

        return result

    def persist(self, path: Text) -> None:
        """Persists the policy to storage."""
        config_file = os.path.join(path, 'fallback_policy.json')
        meta = {
            "nlu_threshold": self.nlu_threshold,
            "core_threshold": self.core_threshold,
            "fallback_action_name": self.fallback_action_name
        }
        rasa.utils.io.create_directory_for_file(config_file)
        rasa.utils.io.dump_obj_as_json_to_file(config_file, meta)

    @classmethod
    def load(cls, path: Text) -> 'AsrFallbackPolicy':
        meta = {}
        if os.path.exists(path):
            meta_path = os.path.join(path, "fallback_policy.json")
            if os.path.isfile(meta_path):
                meta = json.loads(rasa.utils.io.read_file(meta_path))

        return cls(**meta)
