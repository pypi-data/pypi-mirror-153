from typing import Type

import pyexlatex as pl

from derobertis_cv.models.experience_scale import SkillExperienceScale, HoursExperienceScale
from derobertis_cv.pltemplates.skills.skill_dot import GrayscaleSkillDot as SkillDot, GRAY_DARK, GRAY_LIGHT

LEGEND_SPACER_SIZE = 0.2


class PyexlatexSkill(pl.Template):
    experience_scale: Type[SkillExperienceScale] = HoursExperienceScale
    legend = [
        pl.Center(
            [
                'Hours of Experience:',
                pl.HFill(),
                SkillDot(5),
                experience_scale.description_for_level(5),
                pl.HSpace(LEGEND_SPACER_SIZE),
                '|',
                pl.HSpace(LEGEND_SPACER_SIZE),
                SkillDot(4),
                experience_scale.description_for_level(4),
                pl.HSpace(LEGEND_SPACER_SIZE),
                '|',
                pl.HSpace(LEGEND_SPACER_SIZE),
                SkillDot(3),
                experience_scale.description_for_level(3),
                pl.HSpace(LEGEND_SPACER_SIZE),
                '|',
                pl.HSpace(LEGEND_SPACER_SIZE),
                SkillDot(2),
                experience_scale.description_for_level(2),
                pl.HSpace(LEGEND_SPACER_SIZE),
                '|',
                pl.HSpace(LEGEND_SPACER_SIZE),
                SkillDot(1),
                experience_scale.description_for_level(1),
                pl.VSpace(-0.2),
            ]
        )

    ]

    def __init__(self, skill_name: str, level: int, color_level: int = 3):
        self.skill_name = skill_name
        self.level = level
        self.contents = [SkillDot(level, color_level=color_level), skill_name]
        super().__init__()
