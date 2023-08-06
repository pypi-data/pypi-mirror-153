from typing import Any, Dict

import pyexlatex as pl

from derobertis_cv.models.grades.breakdown import GradeBreakdownModel
from derobertis_cv.models.grades.main import GradingModel
from derobertis_cv.models.grades.scale import GradingScaleModel


def get_grading_model(**config: Dict[str, Any]) -> GradingModel:
    default_breakdown = GradeBreakdownModel({
        'Lab Exercises': 0.2,
        'Projects': 0.8
    })
    default_grading_scale = GradingScaleModel({
        'A': (93, 100),
        'A-': (90, 92),
        'B+': (87, 89),
        'B': (83, 86),
        'B-': (80, 82),
        'C+': (77, 79),
        'C': (73, 76),
        'C-': (70, 72),
        'D+': (67, 69),
        'D': (63, 66),
        'D-': (60, 62),
        'F': (0, 59),
    })
    default_extra_info = [
        pl.SubSection(
            [
                """
I will strictly follow standard rounding rules to two decimal places, so 92.450% is the minimum grade for an
A. 92.449% is considered an A-.
                """.strip()
            ],
            title='Rounding'
        ),
        pl.SubSection(
            [
                """
I will strive for a B average in the class. If this requires boosting grades with a curve, this will be done after
all the projects are submitted. I will not reduce grades with a curve even if grades are higher than a B average.
                """.strip()
            ],
            title='Curve'
        )
    ]

    data = dict(
        breakdown=default_breakdown,
        scale=default_grading_scale,
        extra_info=default_extra_info,
    )
    data.update(config)

    model = GradingModel(**data)  # type: ignore
    return model