import logging
from pathlib import Path
from typing import Any, List, Union

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from classification_model import __version__ as _version
from classification_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config

logger = logging.getLogger(__name__)


def get_first_cabin(row: Any) -> Union[str, float]:
    try:
        return row.split()[0]
    except AttributeError:
        return np.nan


def pre_pipeline_preparation(*, dataframe: pd.DataFrame) -> pd.DataFrame:
    # replace question marks with NaN values
    data = dataframe.replace("?", np.nan)

    # retain only the first cabin if more than
    # 1 are available per passenger
    data[config.model_config.variable_to_get_first_letter] = data[
        config.model_config.variable_to_get_first_letter
    ].apply(get_first_cabin)

    # cast numerical variables as floats
    for feature in config.model_config.numerical_vars:
        data[feature] = data[feature].astype("float")

    data_feat = data[config.model_config.features].copy()
    data = pd.concat([data_feat, data[config.model_config.target]], axis=1)
    return data


def _load_raw_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    return dataframe


def load_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    transformed = pre_pipeline_preparation(dataframe=dataframe)

    return transformed


def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:

    # Prepare versioned save file name
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)


def load_pipeline(*, file_name: str) -> Pipeline:
    """Load a persisted pipeline."""

    file_path = TRAINED_MODEL_DIR / file_name
    return joblib.load(filename=file_path)


def remove_old_pipelines(*, files_to_keep: List[str]) -> None:

    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
