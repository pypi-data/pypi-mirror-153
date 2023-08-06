import abc
import datetime


class ISkillExperience(abc.ABC):
    @property
    @abc.abstractmethod
    def experience_length(self) -> datetime.timedelta:
        ...

    @property
    @abc.abstractmethod
    def hours(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def experience_length_str(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def weeks_elapsed(self) -> float:
        ...

    @property
    @abc.abstractmethod
    def months_elapsed(self) -> float:
        ...

    @property
    @abc.abstractmethod
    def experience_level(self) -> int:
        ...
