from ..core import load_object
from .get_model_manager import deserialize


def load_model_state(model_state_path: str):
    """
     # TODO: Convert part of this to a seclea utils?
     loads and deserializes model state into the model used in ML.
    :param model_state:
    :return:
    """
    model_b = load_object(model_state_path)
    return deserialize(model_b)
