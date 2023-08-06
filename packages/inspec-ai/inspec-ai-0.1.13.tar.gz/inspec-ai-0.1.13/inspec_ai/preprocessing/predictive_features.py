from typing import Tuple, Union

import numpy as np
import pandas as pd

from sklearn.linear_model import Lasso

from inspec_ai.analytics import telemetry_service


@telemetry_service.track_function_executed("get_predictive_features")
def get_predictive_features(
    x_train: Union[pd.DataFrame, np.ndarray],
    y_train: Union[pd.DataFrame, pd.Series, np.ndarray],
    alpha: float = 0.1,
) -> Tuple[Union[pd.DataFrame, np.ndarray], dict]:
    """Gets the predictive features of a dataset based on the coefficients returned by a Lasso model used as a baseline.

    Args:
        x_train: Numpy array or pandas Series. Training dataset.
        y_train: Numpy array or pandas Series. Predicted target values.
        alpha: The L2 regularization parameter for the Lasso model. If 0, then all the features will be used.

    Returns:
        The dataset with only the optimal features.
        The dictionary containing the coefficients used to establish the optimal features

    """
    _validate_inputs(x_train, y_train)

    model = Lasso(alpha=alpha)
    model.fit(x_train, y_train)
    lasso_coef = model.coef_

    optimal_features, coef_dict = _format_output(x_train, lasso_coef)

    return optimal_features, coef_dict


def _format_output(x_train, lasso_coef):

    if isinstance(x_train, pd.DataFrame):
        optimal_features = x_train.loc[:, lasso_coef != 0]
        coef_dict = {x_train.columns[index]: coef for index, coef in enumerate(lasso_coef)}

    else:
        optimal_features = x_train[:, (lasso_coef != 0)]
        coef_dict = dict(enumerate(lasso_coef))

    return optimal_features, coef_dict


def _validate_inputs(x_train: Union[pd.DataFrame, np.ndarray], y_train: Union[pd.DataFrame, np.ndarray]) -> None:
    if not isinstance(x_train, (pd.DataFrame, np.ndarray)):
        raise ValueError(f"x_train must be a pandas Dataframe or a numpy array, not {type(x_train)}")

    if not isinstance(y_train, (pd.DataFrame, pd.Series, np.ndarray)):
        raise ValueError(f"y_train must be a pandas Dataframe, a pandas Series or a numpy array, not {type(y_train)}")

    if len(x_train) != len(y_train):
        raise ValueError("The provided inputs must contain the same number of elements: x_train and y_train.")
