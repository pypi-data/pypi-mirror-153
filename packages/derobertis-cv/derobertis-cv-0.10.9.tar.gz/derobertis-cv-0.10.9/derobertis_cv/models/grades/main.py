from dataclasses import dataclass
from typing import Any

from derobertis_cv.models.grades.breakdown import GradeBreakdownModel
from derobertis_cv.models.grades.scale import GradingScaleModel


@dataclass
class GradingModel:
    breakdown: GradeBreakdownModel
    scale: GradingScaleModel
    extra_info: Any = None
