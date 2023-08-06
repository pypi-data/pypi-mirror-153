import base64
import json
from enum import Enum

try:
    from .sklearn import SKLearnModelManager
except ValueError:
    SKLearnModelManager = None
try:
    from .lightgbm import LightGBMModelManager
except ValueError:
    LightGBMModelManager = None
except ModuleNotFoundError:
    LightGBMModelManager = None
try:
    from .xgboost import XGBoostModelManager
except ValueError:
    XGBoostModelManager = None
except ModuleNotFoundError:
    XGBoostModelManager = None
from typing import Any


class ModelManagers(Enum):
    XGBOOST = XGBoostModelManager
    LIGHTGBM = LightGBMModelManager
    SKLEARN = SKLearnModelManager
    NOT_IMPORTED = None


class ModelDecodeError(Exception):
    pass


class ModelEncodeError(Exception):
    pass


def serialize(model, model_manager: ModelManagers) -> bytes:
    """
    Serializes a model given a model manager so that it can be stored and reloaded later.
    @param model: The model to serialize
    @param model_manager: model manager to encode the model with
    @return: str of encoded model
    """
    try:
        if model_manager.value is None:
            raise ModelEncodeError(f"Framework {model_manager.name} is not imported")
        model_b = model_manager.value.encode(model)
        model_str = base64.b64encode(model_b).decode("ascii")
        return json.dumps([model_manager.name, model_str]).encode("utf-8")
    except Exception as e:
        raise ModelEncodeError(f"Issue encoding model: {e}")


def deserialize(data: bytes) -> Any:
    """
    returns a Loaded model given data (previously serialized)
    @param data: serialized model
    @return: loaded model
    """
    try:
        data_str = data.decode("utf-8")
        key, model_str = json.loads(data_str)
    except json.JSONDecodeError as e:
        raise ModelDecodeError("Failed to decode model:", e)
    except ValueError:
        raise ModelDecodeError(
            f"Wrong Encoding, expected list of two elements: key,val, got: {json.loads(data_str)}"
        )

    try:
        model_manager = ModelManagers[key].value
        model_b = base64.b64decode(model_str)

    except KeyError as e:
        raise ModelDecodeError(f"Failed to retrieve model manager with key: {key}, err:{e}")
    except AttributeError as e:
        raise ModelDecodeError(f"Framework {ModelManagers[key].name} is not imported, err:{e}")
    except Exception as e:
        raise ModelDecodeError(f"Unknown issue, potential decode implementation error:{e}")
    try:
        return model_manager.decode(model_b)
    except Exception as e:
        raise ModelDecodeError(
            f"Error decoding model, Framework:{model_manager.__class__}, err:{e}"
        )
