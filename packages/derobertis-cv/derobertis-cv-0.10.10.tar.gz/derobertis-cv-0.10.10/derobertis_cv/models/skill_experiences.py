from dataclasses import dataclass
import datetime
from typing import Type, Sequence

from derobertis_cv.models.experience_scale import HoursExperienceScale, SkillExperienceScale
from derobertis_cv.models.i_skill_experience import ISkillExperience
from derobertis_cv.models.skill_experience import SkillExperience
from derobertis_cv.models.skill_experience_mixin import SkillExperienceMixin


@dataclass(unsafe_hash=True)
class SkillExperiences(SkillExperienceMixin, ISkillExperience):
    experiences: Sequence[SkillExperience]
    experience_scale: Type[SkillExperienceScale] = HoursExperienceScale

    def __post_init__(self):
        count_end_date = sum(
            1 if exp.end_date is not None else 0 for exp in self.experiences
        )
        if count_end_date < len(self.experiences) - 1:
            raise ValueError(
                "Can only have one experience with no end date (only one can go to present)"
            )

    @property
    def begin_date(self) -> datetime.date:  # type: ignore
        return min(exp.begin_date for exp in self.experiences)

    @property
    def effective_end_date(self) -> datetime.date:  # type: ignore
        return max(exp.effective_end_date for exp in self.experiences)

    @property
    def hours(self) -> float:  # type: ignore
        return sum(exp.hours for exp in self.experiences)
