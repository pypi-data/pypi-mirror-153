import pickle  # nosec
from typing import Any, Dict

from .model_management import ModelManager


class SKLearnModelManager(ModelManager):
    @staticmethod
    def encode(model: Any) -> bytes:
        return pickle.dumps(model)  # nosec

    @staticmethod
    def decode(data: bytes) -> Any:
        """
        Loads a stored SKLearn model. As the model is stored with pickle and a certain version of SKLearn, there
        may be inconsistencies where different versions of SKLearn are used for pickling and unpickling.
        :param reference:
        :return:
        """
        return pickle.loads(data)  # nosec

    @staticmethod
    def get_params(model) -> Dict:
        """
        Extracts the parameters of the model.
        :param model: The model
        """

        return model.get_params()
