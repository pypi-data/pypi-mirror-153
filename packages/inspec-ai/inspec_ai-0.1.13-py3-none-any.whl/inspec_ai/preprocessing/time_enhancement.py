from datetime import datetime
from typing import Dict, List, Union

import holidays
import numpy as np
import pandas as pd

from inspec_ai.preprocessing.predictive_features import get_predictive_features


DATES_NOT_A_PD_SERIES_ERROR = "The dates input should be a pandas series, not '{input_type}'."

DATES_NOT_A_DATETIME_DTYPE_ERROR = "The dates input have a datetime dtype, not '{input_dtype}'."

INVALID_PERIODICITY_ERROR = "The periodicity input should be either 'D', 'W' or 'M', not '{periodicity}'."

CUSTOM_DATES_NOT_DICT_ERROR = "The custom_dates input should be a dictionary, not '{input_type}'."

CUSTOM_DATES_VALUE_INVALID_TYPE_ERROR = (
    "The custom_dates input dict values should be either a list, a string with the 'YYYY-MM--DD' format or a datetime object, "
    "not '{custom_dates_value_type}'."
)

CUSTOM_DATES_LIST_VALUE_WITH_INVALID_ELEMENTS_ERROR = (
    "The elements of a list custom_dates input dict values should be either a string with the 'YYYY-MM--DD' format or a datetime object,"
    "not '{custom_dates_list_value_type}'."
)


def get_predictive_time_features(
    dates: pd.Series,
    y: Union[pd.Series, np.ndarray],
    periodicity="D",
    custom_dates: Dict[str, Union[List[Union[str, datetime]], str, datetime]] = None,
    alpha=0.1,
) -> pd.DataFrame:
    """Generates and selects the relevant time features for predicting the y series.

    The time features are automatically generated using the inspec_ai.preprocessing.time_enhancement function.
    The relevant features are then selected with a lasso regression model.

    Args:
        dates: Series of dates, should be a pandas Series with a datetime dtype.
        y: Numpy array or pandas Series. Predicted target values.
        periodicity: Periodicity of the series, should be either 'D' (daily), 'W' (weekly), or 'M' (monthly).
        custom_dates: A dictionary containing user defined important dates to add as one-hot encoded variables. Each key
            should be the name of an event and the value its date. The valid formats for the values are: list, datetime
            and str following the 'YYYY-MM-DD' format. The valid formats for the elements of a list value are: datetime and
            str with the 'YYYY-MM--DD' format.
        alpha: The L2 regularization parameter for the Lasso model. If 0, then all the features will be used.

    Returns: A pandas DataFrame containing the predictive time and seasonal features.

    """
    time_features = time_enhancement(dates, periodicity, custom_dates)
    _, predictive_time_features_coefs = get_predictive_features(time_features, y, alpha)

    predictive_columns = [col for col, coef in predictive_time_features_coefs.items() if abs(coef) > 0]

    return time_features[predictive_columns]


def time_enhancement(
    dates: pd.Series,
    periodicity="D",
    custom_dates: Dict[str, Union[List[Union[str, datetime]], str, datetime]] = None,
) -> pd.DataFrame:
    """Generates a dataframe with a set of one-hot encoded variables accounting for time and seasonal events based on a series of dates.

    Args:
        dates: Series of dates, should be a pandas Series with a datetime dtype.
        periodicity: Periodicity of the series, should be either 'D' (daily), 'W' (weekly), or 'M' (monthly).
        custom_dates: A dictionary containing user defined important dates to add as one-hot encoded variables. Each key
            should be the name of an event and the value its date. The valid formats for the values are: list, datetime
            and str following the 'YYYY-MM-DD' format. The valid formats for the elements of a list value are: datetime and
            str with the 'YYYY-MM--DD' format.

    Returns: A pandas DataFrame containing the time and seasonal features.
    """
    if not custom_dates:
        custom_dates = {}

    _validate_dates(dates)
    _validate_custom_dates(custom_dates)

    if periodicity == "D":
        return _time_enhancement_daily(dates, custom_dates)

    elif periodicity == "W":
        return _time_enhancement_weekly(dates)

    elif periodicity == "M":
        return _time_enhancement_monthly(dates)

    else:
        raise ValueError(INVALID_PERIODICITY_ERROR.format(periodicity=periodicity))


def _time_enhancement_daily(dates: pd.Series, custom_dates: Dict[str, Union[List[Union[str, datetime]], str, datetime]]) -> pd.DataFrame:
    """Time enhancement for daily periodicity."""

    time_features = [
        _make_week_dummies(dates),
        _make_month_dummies(dates),
        _make_day_of_week_dummies(dates),
        _make_holiday_dummies(dates, prov="QC"),
        _make_trigonometric_features(dates),
    ]

    if custom_dates:
        time_features.append(_make_custom_dates_dummies(dates, custom_dates))

    return pd.concat(time_features, axis=1)


def _time_enhancement_weekly(dates: pd.Series) -> pd.DataFrame:
    """Time enhancement for weekly periodicity."""
    time_features = [
        _make_week_dummies(dates),
        _make_month_dummies(dates),
        _make_trigonometric_features(dates),
    ]

    return pd.concat(time_features, axis=1)


def _time_enhancement_monthly(dates: pd.Series) -> pd.DataFrame:
    """Time enhancement for monthly periodicity."""
    time_features = [_make_month_dummies(dates), _make_trigonometric_features(dates)]

    return pd.concat(time_features, axis=1)


def _make_month_dummies(dates: pd.Series) -> pd.DataFrame:
    return pd.get_dummies(dates.dt.month_name())


def _make_week_dummies(dates: pd.Series) -> pd.DataFrame:
    return pd.get_dummies(dates.dt.week, prefix="Week")


def _make_day_of_week_dummies(dates: pd.Series) -> pd.DataFrame:
    return pd.get_dummies(dates.dt.day_name())


def _make_holiday_dummies(dates: pd.Series, prov="QC") -> pd.DataFrame:
    holiday_series = dates.apply(_get_canadian_holiday, prov=prov)
    holiday_dummies_df = pd.get_dummies(holiday_series, prefix="holiday")

    return holiday_dummies_df.drop(columns="holiday_None", errors="ignore")


def _make_trigonometric_features(dates: pd.Series) -> pd.DataFrame:
    share_of_year_completed = dates.dt.day_of_year / (365 + dates.dt.is_leap_year)
    angle = (share_of_year_completed * 2 * np.pi).values
    return pd.DataFrame({"sine": np.sin(angle), "cosine": np.cos(angle)})


def _make_custom_dates_dummies(
    dates: pd.Series,
    custom_dates: Dict[str, Union[List[Union[str, datetime]], str, datetime]],
) -> pd.DataFrame:
    dummies = {}

    for event_name, day_or_list_of_days in custom_dates.items():

        if isinstance(day_or_list_of_days, list):
            days = day_or_list_of_days
            datetime_dates = [_to_datetime(day).date() for day in days]
            dummies[event_name] = dates.dt.date.isin(datetime_dates).astype(int)

        else:
            day = day_or_list_of_days
            dummies[event_name] = (dates.dt.date == _to_datetime(day).date()).astype(int)

    return pd.DataFrame(dummies)


def _to_datetime(date: Union[str, datetime]) -> datetime:
    if isinstance(date, str):
        return datetime.strptime(date, "%Y-%m-%d")

    return date


def _get_canadian_holiday(date: str, prov="QC") -> str:
    holidays_dict_like = holidays.Canada(prov=prov)

    try:
        return holidays_dict_like[date].replace(" (Observed)", "")

    except KeyError:
        return "None"


def _validate_dates(dates: pd.Series):
    if not isinstance(dates, pd.Series):
        raise ValueError(DATES_NOT_A_PD_SERIES_ERROR.format(input_type=type(dates)))

    if "datetime" not in str(dates.dtype):
        raise ValueError(DATES_NOT_A_DATETIME_DTYPE_ERROR.format(input_dtype=dates.dtype))


def _validate_custom_dates(custom_dates: Dict[str, Union[List[Union[str, datetime]], str, datetime]]):
    if isinstance(custom_dates, dict):

        for custom_dates_value in custom_dates.values():

            if isinstance(custom_dates_value, list):
                for date in custom_dates_value:
                    if not isinstance(date, str) and not isinstance(date, datetime):
                        raise ValueError(CUSTOM_DATES_LIST_VALUE_WITH_INVALID_ELEMENTS_ERROR.format(custom_dates_list_value_type=type(date)))

            else:
                if not isinstance(custom_dates_value, str) and not isinstance(custom_dates_value, datetime):
                    raise ValueError(
                        CUSTOM_DATES_VALUE_INVALID_TYPE_ERROR.format(
                            custom_dates_value_type=type(custom_dates_value),
                        )
                    )

    else:
        raise ValueError(CUSTOM_DATES_NOT_DICT_ERROR.format(input_type=type(custom_dates)))
