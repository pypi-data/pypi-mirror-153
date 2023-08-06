from abc import ABC, abstractmethod


class SkillLevelScaler(ABC):

    @classmethod
    @abstractmethod
    def level_to_scaled_level(cls, level: int) -> int:
        ...


class FiveToThreeScaler(SkillLevelScaler):

    @classmethod
    def level_to_scaled_level(cls, level: int) -> int:
        if level in (1, 2):
            return 1
        if level == 3:
            return 2
        if level in (4, 5):
            return 3
        raise ValueError(f'invalid level {level}')