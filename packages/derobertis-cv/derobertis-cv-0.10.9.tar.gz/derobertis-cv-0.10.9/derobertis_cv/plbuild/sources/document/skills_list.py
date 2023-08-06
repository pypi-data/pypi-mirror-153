import pyexlatex as pl
import pyexlatex.resume as lr

from derobertis_cv import plbuild
from derobertis_cv.plbuild.paths import images_path
from derobertis_cv.pldata.constants.contact import CONTACT_LINES
from derobertis_cv.pldata.cv import get_cv_packages, get_cv_pre_env_contents
from derobertis_cv.pldata.skills import CV_RENAME_SKILLS, CV_EXCLUDE_SKILLS, CV_SKILL_SECTION_ORDER, get_skills

AUTHORS = ['Nick DeRobertis']

DOCUMENT_CLASS = lr.Resume
OUTPUT_LOCATION = plbuild.paths.DOCUMENTS_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = None
DEFAULT_OUTPUT_FORMAT = 'html'


def get_content():
    skills = get_skills(exclude_skill_children=False, order=CV_SKILL_SECTION_ORDER)
    skill_names = [skills[0].to_title_case_str()] + [skill.to_lower_case_str() for skill in skills[1:]]
    joined = ', '.join(skill_names)
    contents = pl.Section(
        joined,
        title='Skills'
    )
    return contents

DOCUMENT_CLASS_KWARGS = dict(
    contact_lines=CONTACT_LINES,
    packages=get_cv_packages(),
    pre_env_contents=get_cv_pre_env_contents(),
)
OUTPUT_NAME = f'{AUTHORS[0]} Skills List'
