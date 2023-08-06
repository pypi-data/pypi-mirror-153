from feature_engine.encoding import OneHotEncoder, RareLabelEncoder
from feature_engine.imputation import (
    AddMissingIndicator,
    CategoricalImputer,
    MeanMedianImputer,
)
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from classification_model.config.core import config
from classification_model.processing.features import (
    ExtractLetterTransformer,
    ExtractSalutationTransformer,
)

titanic_pipe = Pipeline(
    [
        (
            "extract_salutation",
            ExtractSalutationTransformer(
                variables=[
                    config.model_config.variable_to_get_salutation,
                    config.model_config.variable_to_create,
                ]
            ),
        ),
        (
            "categorical_imputation",
            CategoricalImputer(
                imputation_method="missing",
                variables=config.model_config.categorical_vars,
            ),
        ),
        (
            "missing_indicator",
            AddMissingIndicator(variables=config.model_config.numerical_vars),
        ),
        (
            "median_imputation",
            MeanMedianImputer(
                imputation_method="median", variables=config.model_config.numerical_vars
            ),
        ),
        (
            "extract_letter",
            ExtractLetterTransformer(
                variables=config.model_config.variable_to_get_first_letter
            ),
        ),
        (
            "rare_label_encoder",
            RareLabelEncoder(
                tol=0.05, n_categories=1, variables=config.model_config.categorical_vars
            ),
        ),
        (
            "categorical_encoder",
            OneHotEncoder(
                drop_last=True, variables=config.model_config.categorical_vars
            ),
        ),
        ("scaler", MinMaxScaler()),
        (
            "Logit",
            LogisticRegression(
                C=config.model_config.penalty,
                random_state=config.model_config.random_state,
            ),
        ),
    ]
)
