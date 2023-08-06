from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class GradingScaleModel:
    grade_ranges: Dict[str, Tuple[float, float]]

    def __post_init__(self):
        if len(self.grade_ranges) == 0:
            raise ValueError('no grade ranges provided')
        last_bot = 101
        for grade_name, (bot, top) in self.grade_ranges.items():
            if top != last_bot - 1:
                raise ValueError(f'grade range for {grade_name} is not consecutive in {self}. '
                                 f'({top} should be {last_bot} - 1)')
            last_bot = bot
        if bot != 0:
            raise ValueError(f'lowest grade did not go to zero, instead went to {bot}')