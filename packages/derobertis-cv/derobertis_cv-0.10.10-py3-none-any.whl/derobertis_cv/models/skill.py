from dataclasses import dataclass, field
from typing import Optional, Sequence, Callable, Union, cast, Type

from weakreflist import WeakList

from derobertis_cv.models.cased import CasedModel
from derobertis_cv.models.i_skill_experience import ISkillExperience
from derobertis_cv.models.level_scale import SkillLevelScaler, FiveToThreeScaler
from derobertis_cv.models.nested import NestedModel
from derobertis_cv.models.skill_experience import SkillExperience
from derobertis_cv.pldata.cover_letters.models import SkillFocusPriority
from derobertis_cv.pltemplates.logo import HasLogo


@dataclass(unsafe_hash=True)
class SkillModel(CasedModel, NestedModel, HasLogo):
    title: str
    level: int
    flexible_case: bool = True
    logo_url: Optional[str] = None
    logo_svg_text: Optional[str] = None
    logo_base64: Optional[str] = None
    logo_fa_icon_class_str: Optional[str] = None
    case_lower_func: Callable[[str], str] = lambda x: x.lower()
    case_title_func: Callable[[str], str] = lambda x: x.title()
    case_capitalize_func: Callable[[str], str] = lambda x: x.capitalize()
    parents: Optional[Sequence['NestedModel']] = tuple()
    children: WeakList = field(default_factory=lambda: WeakList(), hash=False)
    primary_category: Optional[Union['SkillModel', str]] = None
    experience: Optional[ISkillExperience] = None
    priority: SkillFocusPriority = SkillFocusPriority(3)
    level_scaler: Type[SkillLevelScaler] = FiveToThreeScaler

    def __post_init__(self):
        if self.primary_category is not None and self.primary_category != 'self':
            self.parents = (*self.parents, self.primary_category)
        super().__init__()

    @property
    def category(self) -> 'SkillModel':
        if self.primary_category is not None:
            if self.primary_category == 'self':
                return self
            elif isinstance(self.primary_category, str):
                raise ValueError('only str passed for primary_category should be self')
            return self.primary_category
        if self.parents:
            return cast('SkillModel', self.parents[0])
        return self

    @property
    def experience_level(self) -> int:
        if self.experience is None:
            return self.level
        return self.experience.experience_level

    @property
    def scaled_level(self) -> int:
        return self.level_scaler.level_to_scaled_level(self.level)
