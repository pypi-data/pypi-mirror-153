import pyexlatex as pl
import pyexlatex.table as lt
import pyexlatex.presentation as lp
import pyexlatex.graphics as lg
import pyexlatex.layouts as ll
import pyexlatex.resume as lr
from pyexlatex.models.control.setcounter import SetCounter

from derobertis_cv import plbuild
from derobertis_cv.plbuild.paths import images_path
from derobertis_cv.pldata.constants.contact import CONTACT_LINES
from derobertis_cv.pldata.courses.fin_model import get_fin_model_course
from derobertis_cv.pltemplates.syllabus import Syllabus

model = get_fin_model_course()

AUTHORS = [f'{model.course_id} - {model.title}']

DOCUMENT_CLASS = lr.Resume
OUTPUT_LOCATION = plbuild.paths.DOCUMENTS_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = None


def get_content():
    return [
        Syllabus(model=model)
    ]

DOCUMENT_CLASS_KWARGS = dict(
    pre_env_contents=[SetCounter('secnumdepth', 0)],  # remove section numbering
    contact_lines=[
        [model.current_period],
        [model.current_time],
    ]
)
OUTPUT_NAME = f'Financial Modeling Syllabus'

