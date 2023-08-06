from dataclasses import dataclass
import datetime
from typing import Union, Type, Optional

import pandas as pd

from derobertis_cv.models.experience_scale import (
    SkillExperienceScale,
    HoursExperienceScale,
)
from derobertis_cv.models.i_skill_experience import ISkillExperience
from derobertis_cv.models.skill_experience_mixin import SkillExperienceMixin


@dataclass(unsafe_hash=True)
class SkillExperience(SkillExperienceMixin, ISkillExperience):
    begin_date_inp: Union[str, datetime.date]
    hours_per_week: float = 0
    one_time_hours: float = 0
    end_date_inp: Optional[Union[str, datetime.date]] = None
    experience_scale: Type[SkillExperienceScale] = HoursExperienceScale

    def __post_init__(self):
        self.begin_date = _date_str_to_date(self.begin_date_inp)
        if self.end_date_inp is not None:
            self.end_date = _date_str_to_date(self.end_date_inp)
            self.effective_end_date = self.end_date
        else:
            self.end_date = None
            self.effective_end_date = datetime.date.today()

    @property
    def hours(self) -> float:  # type: ignore
        num_hours = self.one_time_hours
        num_hours += self.weeks_elapsed * self.hours_per_week
        return num_hours


def _date_str_to_date(date_str: str) -> datetime.date:
    dt: datetime.datetime = pd.to_datetime(date_str).to_pydatetime()
    return dt.date()
