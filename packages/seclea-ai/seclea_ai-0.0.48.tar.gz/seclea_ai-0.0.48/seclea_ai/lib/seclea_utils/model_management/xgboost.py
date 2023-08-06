from typing import Any, Dict

import xgboost as xgb

from ..core import CustomNamedTemporaryFile
from .model_management import ModelManager


class XGBoostModelManager(ModelManager):
    @staticmethod
    def encode(model: Any) -> bytes:
        # save to temp file then use manager to store.
        with CustomNamedTemporaryFile() as temp:
            # this could be from SKlearnAPI or LearningAPI which have significant differences
            model.save_model(temp.name)
            with open(temp.name, "rb") as read_temp:
                return read_temp.read()

    @staticmethod
    def decode(data: bytes) -> Any:
        """
        Loads a stored XGBoost model. Note this will always return a Booster (LearningAPI model) even if the original
        model was an SKLearn model. This will impact the methods available on the returned model.
        :param reference:
        :return: XGBoost.Booster model.
        """
        # need to know what kind of model -
        with CustomNamedTemporaryFile() as temp:
            temp.write(data)
            temp.flush()
            model = (
                xgb.Booster()
            )  # TODO need to be careful about customer usage - ie. do they use the best iteration for their model or not....
            model.load_model(temp.name)
        return model

    @staticmethod
    def get_params(model) -> Dict:
        """
        Extracts the parameters of the model.
        :param model: The model
        """

        return model.save_config()
