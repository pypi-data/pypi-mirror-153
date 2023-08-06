from dataclasses import dataclass
from typing import Optional, Sequence

from pyexlatex import resume as lr

from derobertis_cv.models.category import CategoryModel


@dataclass
class AwardModel(CategoryModel):
    received: Optional[str] = None
    extra_info: Optional[str] = None
    award_parts: Optional[Sequence[str]] = None

    def to_pyexlatex_award(self) -> lr.Award:
        return lr.Award(self.title, received=self.received, extra_info=self.extra_info)
