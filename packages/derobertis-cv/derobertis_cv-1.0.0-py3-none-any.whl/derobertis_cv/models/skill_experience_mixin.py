import datetime
from typing import Type

from derobertis_cv.models.experience_scale import SkillExperienceScale


class SkillExperienceMixin:
    experience_scale: Type[SkillExperienceScale]
    hours: float
    effective_end_date: datetime.date
    begin_date: datetime.date

    @property
    def experience_length_str(self) -> str:
        months = self.months_elapsed
        if months < 1.5:
            return "1 month"
        if months < 10:
            return f"{months:.0f} months"
        years = months / 12
        if round(years, 0) == 1:
            return f"{years:.0f} year"
        return f"{years:.0f} years"

    @property
    def weeks_elapsed(self) -> float:
        seconds_elapsed = self.experience_length.total_seconds()
        return seconds_elapsed / (60 * 60 * 24 * 7)

    @property
    def months_elapsed(self) -> float:
        seconds_elapsed = self.experience_length.total_seconds()
        return seconds_elapsed / (60 * 60 * 24 * 30)

    @property
    def experience_level(self) -> int:
        return self.experience_scale.experience_to_level(self)

    @property
    def experience_length(self) -> datetime.timedelta:
        return self.effective_end_date - self.begin_date
