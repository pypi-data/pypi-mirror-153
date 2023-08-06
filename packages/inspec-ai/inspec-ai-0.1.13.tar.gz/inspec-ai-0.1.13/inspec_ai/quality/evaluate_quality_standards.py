from datetime import datetime
import json
import math
from pathlib import Path
from typing import List, Optional, Tuple, Union
import warnings

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_absolute_percentage_error,
    precision_score,
    recall_score,
    roc_auc_score,
)

from inspec_ai.metrics.mase import mean_absolute_scaled_error
from inspec_ai.quality.constants import (
    NAME_KEY_IDENTIFIER,
    METRIC_KEY_IDENTIFIER,
    THRESHOLD_KEY_IDENTIFIER,
    CONDITION_KEY_IDENTIFIER,
    DIMENSION_KEY_IDENTIFIER,
    DIMENSION_VALUE_KEY_IDENTIFIER,
    DETAILED_RESULTS_KEY_IDENTIFIER,
    EVALUATIONS_RESULTS_KEY_IDENTIFIER,
    ERROR_COUNT_KEY_IDENTIFIER,
    FAIL_COUNT_KEY_IDENTIFIER,
    MESSAGE_KEY_IDENTIFIER,
    METRIC_VALUE_KEY_IDENTIFIER,
    PASS_COUNT_KEY_IDENTIFIER,
    STATUS_KEY_IDENTIFIER,
)
from inspec_ai.quality.enums import Condition, Metric, Status, EvaluationMode
from inspec_ai.quality.exceptions import ConfigError, ConditionEvaluationError, InternalEvaluationError
from inspec_ai.quality.utils import make_plain_english_inner_result, make_plain_english_result
from inspec_ai.quality.quality_standard import QualityStandard
from inspec_ai.quality.visualisation.visualisation import generate_main_html_report
from inspec_ai.utils.text_utils import Color, enumerate_elements_in_a_sentence, color_text_for_console
from inspec_ai.analytics import telemetry_service

ACCEPTED_TYPES_SINGLE_VALUES = (int, float, str, bool)
ACCEPTED_TYPES_MULTIPLE_VALUES = (list,)
ACCEPTED_DIMENSION_VALUE_TYPES_ENUMERATION = enumerate_elements_in_a_sentence(
    [i.__name__ for i in ACCEPTED_TYPES_SINGLE_VALUES + ACCEPTED_TYPES_MULTIPLE_VALUES]
)


@telemetry_service.track_function_executed("evaluate_quality_standards")
def evaluate_quality_standards(
    dimensions_df: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    config: List[QualityStandard],
    print_results_in_console: bool = True,
    verbose: bool = False,
    save_html_report: bool = False,
    save_as_json: bool = False,
    output_folder: Union[Path, str] = None,
) -> dict:

    """Determines if the predictions satisfy quality standards.

        Args:
            dimensions_df: A dataframe containing the columns with values (e.g. product category or product) that will be
                used for aggregating metrics when running tests.
            y_true: Numpy array or pandas Series. Ground truth (correct) target values.
            y_pred: Numpy array or pandas Series. Predicted target values.
            config: A list of quality standards.
            print_results_in_console: Whether to print evaluation results in console.
            verbose: Whether to print the detailed results when available.
            save_html_report: Whether to produce a html report.
            save_as_json: Whether to save the evaluation results as a json file.
            output_folder: Path to the output directory for the json and html reports.

    Returns: A dict containing the detailed results of the tests.
    """

    evaluations_results = []
    output_folder = Path(output_folder) if output_folder else Path(".")

    for quality_standard in config:
        try:
            _check_dimension_config(dimensions_df, quality_standard)
            evaluation_result = _evaluate_metric(dimensions_df, y_true, y_pred, quality_standard)
            evaluations_results.append(evaluation_result)

        except Exception as e:
            message = f"{type(e).__name__}: {e}"
            warnings.warn(message)
            evaluation_result = dict()
            evaluation_result[METRIC_KEY_IDENTIFIER] = quality_standard.metric
            evaluation_result[THRESHOLD_KEY_IDENTIFIER] = quality_standard.threshold
            evaluation_result[CONDITION_KEY_IDENTIFIER] = quality_standard.condition
            evaluation_result[DIMENSION_KEY_IDENTIFIER] = quality_standard.dimension
            evaluation_result[DIMENSION_VALUE_KEY_IDENTIFIER] = quality_standard.dimension_value
            evaluation_result[STATUS_KEY_IDENTIFIER] = Status.ERROR
            evaluation_result[MESSAGE_KEY_IDENTIFIER] = message

            if isinstance(e, InternalEvaluationError):
                evaluation_result[DETAILED_RESULTS_KEY_IDENTIFIER] = e.evaluation_result

            evaluations_results.append(evaluation_result)

    if save_as_json:
        output_path = output_folder / f"quality_standards_evaluation_{datetime.today().strftime('%Y_%m_%d_%H_%M_%S')}.json"
        with open(output_path, "w") as f:
            json.dump(evaluations_results, f)

    results = {EVALUATIONS_RESULTS_KEY_IDENTIFIER: evaluations_results}
    results.update(_count_statuses(evaluations_results))

    if print_results_in_console:
        _print_console_report(results, verbose)

    if save_html_report:
        generate_main_html_report(results, output_folder)

    return results


def _count_statuses(evaluations_results: List[dict]) -> dict:
    statuses_counts = dict()

    statuses_counts[PASS_COUNT_KEY_IDENTIFIER] = 0
    statuses_counts[FAIL_COUNT_KEY_IDENTIFIER] = 0
    statuses_counts[ERROR_COUNT_KEY_IDENTIFIER] = 0

    for result in evaluations_results:
        if result[STATUS_KEY_IDENTIFIER] == Status.ERROR:
            statuses_counts[ERROR_COUNT_KEY_IDENTIFIER] += 1

        if result[STATUS_KEY_IDENTIFIER] == Status.PASSED:
            statuses_counts[PASS_COUNT_KEY_IDENTIFIER] += 1

        elif result[STATUS_KEY_IDENTIFIER] == Status.FAILED:
            statuses_counts[FAIL_COUNT_KEY_IDENTIFIER] += 1

    return statuses_counts


def _check_dimension_config(dimensions_df: pd.DataFrame, quality_standard: QualityStandard):
    if quality_standard.dimension:
        if quality_standard.dimension not in dimensions_df.columns:
            raise ConfigError(
                f"The specified dimension '{quality_standard.dimension}' is missing from the columns in the dimensions dataframe, cannot evaluate"
            )

        if quality_standard.dimension_value:
            if isinstance(quality_standard.dimension_value, ACCEPTED_TYPES_SINGLE_VALUES):
                if quality_standard.dimension_value not in dimensions_df[quality_standard.dimension].unique():
                    raise ConfigError(
                        f"The dimension value '{quality_standard.dimension_value}' is not present in the specified dimension "
                        f"'{quality_standard.dimension}', cannot evaluate"
                    )

            elif isinstance(quality_standard.dimension_value, ACCEPTED_TYPES_MULTIPLE_VALUES):
                if len(set(quality_standard.dimension_value).intersection(dimensions_df[quality_standard.dimension].unique())) == 0:
                    raise ConfigError(
                        f"All the specified dimension values are missing in the specified dimension '{quality_standard.dimension}', cannot evaluate"
                    )

            else:
                raise ConfigError(
                    f"Detected the 'dimension' and 'dimension_value' properties, but 'dimension_value' is "
                    f"{type(quality_standard.dimension_value).__name__} "
                    f"which is not among accepted types: {ACCEPTED_DIMENSION_VALUE_TYPES_ENUMERATION}"
                )
    else:
        if quality_standard.dimension_value:
            raise ConfigError("Detected the 'dimension_value' property, but missing 'dimension' property in configuration, cannot evaluate")


def _evaluate_metric(dimensions_df: pd.DataFrame, y_true: pd.Series, y_pred: pd.Series, quality_standard: QualityStandard) -> dict:
    eval_result = {
        METRIC_KEY_IDENTIFIER: quality_standard.metric,
        CONDITION_KEY_IDENTIFIER: quality_standard.condition,
        THRESHOLD_KEY_IDENTIFIER: quality_standard.threshold,
        NAME_KEY_IDENTIFIER: quality_standard.name
    }

    if quality_standard.evaluation_mode in [EvaluationMode.FOR_EACH_DIM_VALUE_IN_LIST, EvaluationMode.FOR_EACH_UNIQUE_DIM_VALUE]:
        if quality_standard.evaluation_mode == EvaluationMode.FOR_EACH_UNIQUE_DIM_VALUE:
            dimension_value = dimensions_df[quality_standard.dimension].unique().tolist()

        else:
            dimension_value = quality_standard.dimension_value

        eval_result[DETAILED_RESULTS_KEY_IDENTIFIER], eval_result[STATUS_KEY_IDENTIFIER] = _measure_metric_and_evaluate_internal_multiple(
            dimensions_df,
            y_true,
            y_pred,
            quality_standard.metric,
            quality_standard.condition,
            quality_standard.threshold,
            quality_standard.dimension,
            dimension_value,
        )

    else:
        dimension_value = quality_standard.dimension_value

        eval_result[METRIC_VALUE_KEY_IDENTIFIER], eval_result[STATUS_KEY_IDENTIFIER] = _measure_metric_and_evaluate_internal_single(
            dimensions_df,
            y_true,
            y_pred,
            quality_standard.metric,
            quality_standard.condition,
            quality_standard.threshold,
            quality_standard.dimension,
            dimension_value,
        )

    if quality_standard.dimension:
        eval_result[DIMENSION_KEY_IDENTIFIER] = quality_standard.dimension
    if dimension_value:
        eval_result[DIMENSION_VALUE_KEY_IDENTIFIER] = dimension_value

    return eval_result


def _measure_metric(
    dimensions_df: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    metric: Metric,
    dimension: Optional[Union[str, int, float, bool]] = None,
    dimension_value: Optional[Union[list, str, int, float, bool]] = None,
) -> float:
    y_tmp = y_true
    predictions_tmp = y_pred

    if dimension is not None and dimension_value is not None:
        # if a dimension is specified, slice y to only evaluate the metric for the chosen dimension value
        y_tmp = y_true[dimensions_df[dimension] == dimension_value]
        predictions_tmp = y_pred[dimensions_df[dimension] == dimension_value]

    if metric == Metric.MAE.value:
        return mean_absolute_error(y_tmp, predictions_tmp)

    if metric == Metric.MASE.value:
        return mean_absolute_scaled_error(y_tmp, predictions_tmp)

    if metric == Metric.MAPE.value:
        return mean_absolute_percentage_error(y_tmp, predictions_tmp)

    if metric == Metric.AUC.value:
        return roc_auc_score(y_tmp, predictions_tmp)

    if metric == Metric.F1.value:
        return f1_score(y_tmp, predictions_tmp)

    if metric == Metric.PRECISION.value:
        return precision_score(y_tmp, predictions_tmp)

    if metric == Metric.RECALL.value:
        return recall_score(y_tmp, predictions_tmp)

    else:
        return accuracy_score(y_tmp, predictions_tmp)


def _evaluate_internal(metric_value: Union[float, int], condition: Condition, threshold: Union[float, int]) -> bool:

    # lt = lower than
    if condition == Condition.LOWER:
        return metric_value < threshold

    # gt = greater than
    elif condition == Condition.GREATER:
        return metric_value > threshold

    # lte = lower than or equals
    elif condition == Condition.LOWER_EQUALS:
        return metric_value <= threshold

    # gte = greater than or equals
    elif condition == Condition.GREATER_EQUALS:
        return metric_value >= threshold

    # default is eq = equals
    else:
        return metric_value == threshold


def _measure_metric_and_evaluate_internal_single(
    dimensions_df: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    metric: Metric,
    condition: Condition,
    threshold: Union[float, int],
    dimension: Optional[Union[str, int, float, bool]],
    dimension_value: Optional[Union[str, int, float, bool]],
) -> Tuple[float, str]:

    metric_value = _measure_metric(dimensions_df, y_true, y_pred, metric, dimension, dimension_value)
    evaluation_success = _evaluate_internal(metric_value, condition, threshold)

    if math.isnan(metric_value):
        raise ConditionEvaluationError(f"The {metric} was evaluated to NaN.")

    status = Status.PASSED if evaluation_success else Status.FAILED

    return metric_value, status


def _check_config_for_multiple_dimension_values(dimensions_df, dimension, dimension_value):
    if dimension_value not in dimensions_df[dimension].unique().tolist():
        raise ConfigError(f"the dimension value '{dimension_value}' is missing in the dimension '{dimension}'")


def _measure_metric_and_evaluate_internal_multiple(
    dimensions_df: pd.DataFrame,
    y_true: pd.Series,
    y_pred: pd.Series,
    metric: Metric,
    condition: Condition,
    threshold: Union[float, int],
    dimension: Optional[Union[str, int, float, bool]],
    dimension_value: List[Union[str, int, float, bool]],
) -> Tuple[List[dict], str]:

    detailed_results = []

    for i in dimension_value:

        try:
            _check_config_for_multiple_dimension_values(dimensions_df, dimension, i)
            metric_value = _measure_metric(dimensions_df, y_true, y_pred, metric, dimension, i)
            evaluation_success = _evaluate_internal(metric_value, condition, threshold)
            status = Status.ERROR if math.isnan(metric_value) else Status.PASSED if evaluation_success else Status.FAILED
            message = ""

        except Exception as e:
            metric_value = None
            status = Status.ERROR
            message = f"{type(e).__name__}: {e}"

        detailed_results.append(
            {
                DIMENSION_VALUE_KEY_IDENTIFIER: i,
                METRIC_VALUE_KEY_IDENTIFIER: metric_value,
                STATUS_KEY_IDENTIFIER: status,
                MESSAGE_KEY_IDENTIFIER: message
            }
        )

    statuses_counts = _count_statuses(detailed_results)

    if statuses_counts[FAIL_COUNT_KEY_IDENTIFIER] > 0:
        global_status = Status.FAILED
    elif statuses_counts[ERROR_COUNT_KEY_IDENTIFIER] > 0:
        raise InternalEvaluationError(detailed_results, "Error(s) occurred when evaluating the quality standard for at least one group of dimension.")
    else:
        global_status = Status.PASSED

    return detailed_results, global_status


def _format_status_for_console_report(status: str) -> str:
    if status == Status.ERROR or status == Status.FAILED:
        return color_text_for_console(f"[{status}]", Color.RED)

    if status == Status.PASSED:
        return color_text_for_console(f"[{status}]", Color.GREEN)

    return f"[{status}]"


def _print_console_report(results: dict, verbose: bool):

    n_evaluations = len(results[EVALUATIONS_RESULTS_KEY_IDENTIFIER])
    completion_pct = round(100 * results[PASS_COUNT_KEY_IDENTIFIER] / n_evaluations, 2)

    print("QUALITY STANDARDS EVALUATION")

    print(
        f"Total - Pass: {color_text_for_console(str(results[PASS_COUNT_KEY_IDENTIFIER]), Color.GREEN)} "
        f"({str(completion_pct)}%); "
        f"Fail: {color_text_for_console(str(results[FAIL_COUNT_KEY_IDENTIFIER]), Color.RED)}; "
        f"Error: {str(results[ERROR_COUNT_KEY_IDENTIFIER])}"
    )

    print("===============================================================")

    for result in results[EVALUATIONS_RESULTS_KEY_IDENTIFIER]:

        if result[STATUS_KEY_IDENTIFIER] == Status.ERROR and DETAILED_RESULTS_KEY_IDENTIFIER not in result.keys():
            print(f"{_format_status_for_console_report(result[STATUS_KEY_IDENTIFIER])} - {result[MESSAGE_KEY_IDENTIFIER]}")
            print("===============================================================")

        else:
            print(
                f"{_format_status_for_console_report(result[STATUS_KEY_IDENTIFIER])} - "
                f"{result.get(NAME_KEY_IDENTIFIER) if result.get(NAME_KEY_IDENTIFIER) else make_plain_english_result(result)}"
                f"{' (' + str((round(result[METRIC_VALUE_KEY_IDENTIFIER], 4))) + ')' if METRIC_VALUE_KEY_IDENTIFIER in result.keys() else ''}"
            )

            if verbose:
                # print detailed result for evaluations over multiple dimension_values
                if DETAILED_RESULTS_KEY_IDENTIFIER in result.keys():

                    statuses_counts = _count_statuses(result[DETAILED_RESULTS_KEY_IDENTIFIER])

                    print("\n---------  DETAILED RESULTS  ----------------------------------")
                    print(
                        f"Total - Pass: {color_text_for_console(str(statuses_counts[PASS_COUNT_KEY_IDENTIFIER]), Color.GREEN)} "
                        f"({round(statuses_counts[PASS_COUNT_KEY_IDENTIFIER] / len(result[DETAILED_RESULTS_KEY_IDENTIFIER]) * 100, 1)}%); "
                        f"Fail: {color_text_for_console(str(statuses_counts[FAIL_COUNT_KEY_IDENTIFIER]), Color.RED)}; "
                        f"Error: {str(statuses_counts[ERROR_COUNT_KEY_IDENTIFIER])}"
                    )

                    for inner_result in result[DETAILED_RESULTS_KEY_IDENTIFIER]:
                        print(f"{_format_status_for_console_report(inner_result[STATUS_KEY_IDENTIFIER])} - {make_plain_english_inner_result(inner_result)}")

            print("===============================================================")
