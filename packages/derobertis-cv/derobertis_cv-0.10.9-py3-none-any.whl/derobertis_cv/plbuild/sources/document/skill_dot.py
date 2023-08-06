from typing import Any, Dict

import pyexlatex as pl

from derobertis_cv import plbuild
from derobertis_cv.plbuild.paths import images_path
from derobertis_cv.pltemplates.skills.skill_dot import SkillDot

DOCUMENT_CLASS = pl.Standalone
OUTPUT_LOCATION = plbuild.paths.DOCUMENTS_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = None

num_levels = 5

def get_content():
    return [
        *[SkillDot(level, max_level=num_levels) for level in range(1, num_levels + 1)],
    ]

DOCUMENT_CLASS_KWARGS: Dict[str, Any] = dict(

)
OUTPUT_NAME = f'Skill Dot'

