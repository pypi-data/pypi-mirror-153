from typing import Optional, Type, Union
from inspec_ai.quality.enums import Condition, Metric, EvaluationMode
from inspec_ai.quality.exceptions import ConfigError
from inspec_ai.utils.text_utils import enumerate_elements_in_a_sentence
from inspec_ai.utils.utils import _StrEnum


class QualityStandard:
    """Quality standard for the evaluate_quality_standards function.

    Attributes:
        metric: The error measure to evaluate the model on. Can be 'mae', 'mase', 'mape', 'auc', 'f1', 'precision', 'recall', or 'accuracy'.
            The init method accepts a string, but sets the attribute as an enum.
        threshold: The limit (numerical) value that the metric should be.
            Whether the metric should be equal, lower or higher than the threshold is defined by the condition attribute.
        condition: An indicator whether the error should be equal ('eq'), greater ('ht'), greater or equal ('gte'), lower ('lt'),
            or lower or equal ('lte') to the threshold. The init method accepts a string, but sets the attribute as an enum.
        dimension: Indicates a dimension column for which the error measure should be evaluated. If the dimension_value attribute is None,
            then the evaluation mode will be set to 'for each unique dimension value', i.e. the quality standard should be evaluated for each group.
            If the dimension_value is defined, then the quality standard will only be evaluated for that dimension value, or that group of dimension values.
            If the dimension is set to None, then the quality standard should be evaluated for the whole dataset.
        dimension_value: Indicates a dimension value or a group or dimension values for which the quality standard should be evaluated.
            he dimension_value should only be set if the dimension attribute is also set (not None).
        name: Optional quality standard name.
        evaluation_mode: Indicates whether the quality standard should be evaluated for the whole dataset ("global"), for each dimension in the dataset,
            for one dimension, or for each dimension in a list
    """

    def __init__(
        self,
        metric: str,
        threshold: Union[int, float],
        condition: str,
        dimension: Optional[Union[str, int, float, bool]] = None,
        dimension_value: Optional[Union[list, str, int, float, bool]] = None,
        name: Optional[str] = None,
    ):
        self._check_if_user_input_in_allowed_values(metric, Metric)
        self._check_if_user_input_in_allowed_values(condition, Condition)

        self.metric: Metric = Metric(metric)
        self.threshold = threshold
        self.condition: Condition = Condition(condition)
        self.dimension = dimension
        self.dimension_value = dimension_value
        self.name = name
        self.evaluation_mode: EvaluationMode = self._determine_evaluation_mode()

    def _determine_evaluation_mode(self):
        accepted_types_single_values = (int, float, str, bool)

        if self.dimension:
            if self.dimension_value:
                if isinstance(self.dimension_value, accepted_types_single_values):
                    return EvaluationMode.FOR_SINGLE_DIM_VALUE
                else:
                    return EvaluationMode.FOR_EACH_DIM_VALUE_IN_LIST
            else:
                return EvaluationMode.FOR_EACH_UNIQUE_DIM_VALUE
        return EvaluationMode.GLOBAL

    @staticmethod
    def _check_if_user_input_in_allowed_values(user_input: str, enum: Type[_StrEnum]):
        allowed_values = [str(value) for value in enum]

        if user_input not in allowed_values:
            raise ConfigError(
                f"Unknown '{enum.__name__.lower()}': '{user_input}'. "
                f"Please specify one of the following metrics: {enumerate_elements_in_a_sentence(allowed_values).replace('and', 'or')}"
            )
