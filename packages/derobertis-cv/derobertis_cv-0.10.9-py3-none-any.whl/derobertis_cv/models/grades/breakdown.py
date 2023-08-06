from dataclasses import dataclass
from typing import Dict


@dataclass
class GradeBreakdownModel:
    categories: Dict[str, float]

    def __post_init__(self):
        if sum(self.categories.values()) != 1:
            raise ValueError('breakdown grade weights must sum to 1')