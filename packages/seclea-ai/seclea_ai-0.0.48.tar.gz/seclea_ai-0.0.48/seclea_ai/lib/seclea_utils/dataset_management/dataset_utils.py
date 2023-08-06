import os
import uuid
from enum import Enum
from io import StringIO
from pathlib import Path
from typing import Any

import boto3
import dill as pickle  # nosec
import numpy as np
import pandas as pd
from PIL import Image

from ..core import CompressionFactory, load_object, save_object

S3_BUCKET_NAME = "S3_BUCKET_NAME"


def save_dataset(dataset, path, name):
    Path(path).mkdir(parents=True, exist_ok=True)
    dataset_path = os.path.join(path, name + "tmp.csv")
    dataset.to_csv(dataset_path, index=True)
    comp_path = os.path.join(path, name)
    rb = open(dataset_path, "rb")
    comp_path = save_object(rb, comp_path, compression=CompressionFactory.ZSTD)
    return comp_path


def load_dataset(dataset_path: str, index_col=None):
    """
     # TODO: Extend to different types of datasets
    :param model_dataset:
    :return:
    """

    dataset_str = load_object(dataset_path, as_bytes=False)
    dataset_stream = StringIO(dataset_str)
    df = pd.read_csv(dataset_stream, index_col=index_col)
    return df


def dataset_hash(dataset, project: int) -> str:
    return str(hash(pd.util.hash_pandas_object(dataset).sum() + project))


def get_dataset_project_hash(dataset, project) -> str:
    return str(hash(bytes(dataset)) + hash(project))


def get_dataset_hash(dataset) -> str:
    return str(hash(bytes(dataset)))


def get_project_hash(project) -> str:
    return str(hash(project))


class DatasetWorker:
    PANDAS = "pandas"
    DILL = "dill"
    NUMPY = "numpy"
    FEATHER = "feather"
    PILLOW = "pillow"
    ZIPFILE = "zipfile"
    TARFILE = "tarfile"

    class Mode(Enum):
        S3 = 1
        LOCAL = 2

    mode = Mode.LOCAL

    def get_lib(self, file_type: str):
        FILE_OPENER = {
            # Single files
            self.PANDAS: ["csv", "txt", "parquet"],
            self.DILL: ["pickle"],
            self.NUMPY: ["npy"],
            self.FEATHER: ["feather"],
            self.PILLOW: ["jpg", "png"],
            # Archives
            self.ZIPFILE: ["gzip", "bzip", "7zip"],
            self.TARFILE: ["tar_gz", "tar_bz"],
            None: [  # We will work with those types in future
                # Single files
                "dhf5",
                "netcdf",
                "json",
                "orc",
                "avro",
                "pdf",
                "nii",
                "dicom",
            ],
        }

        for lib, file_types in FILE_OPENER.items():
            if file_type in file_types:
                return lib
        raise Exception(f"We didn't work with {file_type} file type")

    def open_pandas(self, file_path, file_type):
        if file_type == "parquet":
            return pd.read_parquet(file_path, engine="pyarrow")
        else:
            return pd.read_csv(file_path)

    def open_dill(self, file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)  # nosec

    def open_numpy(self, file_path):
        return np.load(file_path)

    def open_feather(self, file_path):
        return pd.read_feather(file_path)

    def open_pillow(self, file_path):
        return Image.open(file_path)

    def load_dataset(self, file_path: str):
        file_type = file_path.split(".")[-1]
        lib = self.get_lib(file_type=file_type)
        return self.open_dataset(lib=lib, file_path=file_path)

    def save_on_s3(self, file_path):
        file_name = file_path.split("/")[-1]
        file_path_on_s3 = f"data/{file_name}"

        client = boto3.client("s3")
        client.put_object(
            Body=open(file_path, "rb"),
            Bucket=S3_BUCKET_NAME,
            Key=file_path_on_s3,
        )

        return file_path_on_s3

    def save_pandas(self, dataset: Any, file_path: str, file_type: str):
        if file_type == "parquet":
            dataset.to_parquet("dataset.parquet.gzip", compression="gzip")
        else:
            dataset.to_csv(file_path)

    def save_dill(self, dataset: Any, file_path: str):
        with open(file_path, "wb") as outp:
            pickle.dump(dataset, outp, pickle.HIGHEST_PROTOCOL)

    def save_numpy(self, dataset: Any, file_path: str):
        np.savetxt(file_path, dataset, delimiter=",")

    def save_feather(self, dataset: Any, file_path: str):
        dataFrame = pd.DataFrame(data=dataset)
        dataFrame.to_feather(file_path)

    def save_pillow(self, dataset: Any, file_path: str):
        dataset.save(file_path)

    def open_dataset(self, lib: str, file_path: str):
        file_type = file_path.split(".")[0]
        if lib == self.PANDAS:
            return self.open_pandas(file_path=file_path, file_type=file_type)
        elif lib == self.DILL:
            return self.open_dill(file_path=file_path)
        elif lib == self.NUMPY:
            return self.open_numpy(file_path=file_path)
        elif lib == self.FEATHER:
            return self.open_feather(file_path=file_path)
        elif lib == self.PILLOW:
            return self.open_pillow(file_path=file_path)

    def save_dataset(self, dataset: Any, file_type: str, path: str) -> str:
        lib = self.get_lib(file_type=file_type)
        file_path = f"{path}_{uuid.uuid4()}.{file_type}"

        if lib == self.PANDAS:
            self.save_pandas(dataset=dataset, file_path=file_path, file_type=file_type)
        elif lib == self.DILL:
            self.save_dill(dataset=dataset, file_path=file_path)
        elif lib == self.NUMPY:
            self.save_numpy(dataset=dataset, file_path=file_path)
        elif lib == self.FEATHER:
            self.save_feather(dataset=dataset, file_path=file_path)
        elif lib == self.PILLOW:
            self.save_pillow(dataset=dataset, file_path=file_path)

        if self.mode == self.Mode.S3:
            return self.save_on_s3(file_path=file_path)
        return file_path
