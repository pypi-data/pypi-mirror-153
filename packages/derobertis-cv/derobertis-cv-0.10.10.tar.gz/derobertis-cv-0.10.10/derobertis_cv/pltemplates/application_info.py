from typing import Sequence, List, Dict, Optional

import math
import pyexlatex as pl
import pyexlatex.resume as lr
from pyexlatex.typing import PyexlatexItem

from derobertis_cv.models.skill import SkillModel
from derobertis_cv.pltemplates.skills.skill import PyexlatexSkill


class ApplicationInfoSection(lr.SpacedSection):
    def __init__(self, application_info: Dict[str, str], font_scale: Optional[float] = None):
        self.application_info = application_info
        self.font_scale = font_scale

        content: List[PyexlatexItem] = []
        if font_scale is not None:
            font_str = (
                    r'\setmainfont{Latin Modern Roman}[Scale =' +
                    str(font_scale) +
                    ',Ligatures = {Common, TeX}]'
            )
            font_resize = pl.Raw(font_str)
            content.append(font_resize)

        extra_info_items = [[pl.Bold(key + ':'), value] for key, value in application_info.items()]
        content.extend(extra_info_items)
        content.append(pl.VSpace(0.4))

        super().__init__(content, title="Application Information")
