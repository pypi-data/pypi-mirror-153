import copy
from typing import Any, Dict

import lightgbm as lgb

from .model_management import ModelManager


class LightGBMModelManager(ModelManager):
    @staticmethod
    def encode(model: Any) -> bytes:
        # saves either the best or all iterations.. TODO think
        if isinstance(model, lgb.Booster):
            model_data = model.model_to_string().encode("utf-8")
        else:
            model_data = model.booster_.model_to_string().encode("utf-8")
        return model_data

    @staticmethod
    def decode(data: bytes) -> Any:
        """
        Loads a stored LightGBM model. Note this will always return a LightGBM Booster, even if the original model was
        an SKLearn model. This will impact the methods available on the returned model.
        :param data:
        :return: LightGBM.Booster model
        """
        model_str = data.decode()
        model = lgb.Booster(model_str=model_str)
        return model

    @staticmethod
    def get_params(model) -> Dict:
        """
        Extracts the parameters of the model.
        :param model: The model
        """

        return copy.deepcopy(model.params)
