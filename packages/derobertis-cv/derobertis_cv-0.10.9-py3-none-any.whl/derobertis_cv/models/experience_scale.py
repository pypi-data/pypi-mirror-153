from abc import ABC, abstractmethod
from typing import Dict, TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from derobertis_cv.models.skill_experience import SkillExperience


class ExperienceAttributes(Protocol):
    hours: float


class SkillExperienceScale(ABC):

    @classmethod
    @abstractmethod
    def experience_to_level(cls, exp: ExperienceAttributes) -> int:
        ...

    @classmethod
    @abstractmethod
    def description_for_level(cls, level: int) -> str:
        ...


class HoursExperienceScale(SkillExperienceScale):
    cutoffs: Dict[int, float] = {
        2: 100,
        3: 500,
        4: 1000,
        5: 3000
    }

    @classmethod
    def experience_to_level(cls, exp: ExperienceAttributes) -> int:
        hours = exp.hours
        level = 0
        for level, cutoff in cls.cutoffs.items():
            if hours < cutoff:
                # Didn't meet this cutoff, assign last level
                return level - 1

        # Not less than any cutoffs, must be the last level
        return level

    @classmethod
    def description_for_level(cls, level: int) -> str:
        if level == 1:
            return f'20 - {cls.cutoffs[2]:,.0f}'
        if level < 5:
            return f'{cls.cutoffs[level]:,.0f} - {cls.cutoffs[level + 1]:,.0f}'
        if level == 5:
            return f'{cls.cutoffs[5]:,.0f}+'
        raise ValueError(f'invalid level {level}')