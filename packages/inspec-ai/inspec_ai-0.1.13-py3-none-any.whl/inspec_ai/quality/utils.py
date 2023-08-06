from inspec_ai.quality.constants import (
    CONDITION_KEY_IDENTIFIER,
    DIMENSION_VALUE_KEY_IDENTIFIER,
    METRIC_KEY_IDENTIFIER,
    METRIC_VALUE_KEY_IDENTIFIER,
    MESSAGE_KEY_IDENTIFIER,
    THRESHOLD_KEY_IDENTIFIER,
)
from inspec_ai.utils.text_utils import enumerate_elements_in_a_sentence


def make_plain_english_result(evaluation_result: dict) -> str:
    return (
        f"{evaluation_result[METRIC_KEY_IDENTIFIER].upper()} "
        f"{evaluation_result[CONDITION_KEY_IDENTIFIER].convert_to_plain_english()} "
        f"{evaluation_result[THRESHOLD_KEY_IDENTIFIER]}"
        f"{_format_plain_english_dimension_value(evaluation_result)}"
    )


def make_plain_english_inner_result(inner_evaluation_result: dict) -> str:
    metric_value = inner_evaluation_result[METRIC_VALUE_KEY_IDENTIFIER]

    return (
        f"{inner_evaluation_result[DIMENSION_VALUE_KEY_IDENTIFIER]}"
        f"{' (' + str((round(metric_value, 4))) + ')' if metric_value is not None else ': '}"
        f"{str(inner_evaluation_result[MESSAGE_KEY_IDENTIFIER]) if MESSAGE_KEY_IDENTIFIER in inner_evaluation_result.keys() else ''}"
    )


def _format_plain_english_dimension_value(evaluation_result: dict) -> str:
    if "dimension_value" in evaluation_result.keys():
        dim_values = evaluation_result[DIMENSION_VALUE_KEY_IDENTIFIER]
        dim_values = _make_str_or_list_of_str(dim_values)
        if isinstance(dim_values, list):
            return f" for {enumerate_elements_in_a_sentence(dim_values)}"
        else:
            return f" for {dim_values}"

    return ""


def _make_str_or_list_of_str(thing):
    if isinstance(thing, str):
        return thing

    elif isinstance(thing, list):
        return [_make_str_or_list_of_str(i) for i in thing]

    return str(thing)
