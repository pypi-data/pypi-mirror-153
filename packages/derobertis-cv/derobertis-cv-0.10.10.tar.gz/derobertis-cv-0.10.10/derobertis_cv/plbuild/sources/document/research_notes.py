from typing import List

import pyexlatex as pl
import pyexlatex.table as lt
import pyexlatex.presentation as lp
import pyexlatex.graphics as lg
import pyexlatex.layouts as ll
import pyexlatex.resume as lr
from pyexlatex.models.page.number import PageReference
from pyexlatex.typing import PyexlatexItem

from derobertis_cv import plbuild
from derobertis_cv.plbuild.paths import images_path
from derobertis_cv.pldata.constants.contact import CONTACT_LINES, NAME
from derobertis_cv.pldata.papers import get_working_papers, get_works_in_progress

AUTHORS = ['Nick DeRobertis']

DOCUMENT_CLASS = pl.Document
OUTPUT_LOCATION = plbuild.paths.DOCUMENTS_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = None

title = 'Research Notes'


def get_content():
    research = get_working_papers() + get_works_in_progress()

    overview = pl.Section(
        [
            'The overarching focus in my research is financial markets, though my work falls in multiple '
            'different areas of the literature. I am primarily an empirical researcher focusing on asset pricing, '
            'microstructure, and behavioral finance, though I have also done some corporate finance and theory work.'
        ],
        title='Overview'
    )

    contents: List[PyexlatexItem] = [overview]
    for res in research:
        if res.notes_content:
            contents.append(pl.Section(res.notes_content, title=res.title))

    return contents

DOCUMENT_CLASS_KWARGS = dict(
    remove_section_numbering=True,
    title=title,
    page_modifier_str='margin=1in',
    apply_page_style_to_section_starts=True,
    custom_footers=[
        pl.LeftFooter(NAME),
        pl.CenterFooter(title),
        pl.RightFooter(
            ['Page', pl.ThisPageNumber(), '\\', 'of', PageReference('LastPage')]
        ),
        pl.FooterLine()
    ]
)
OUTPUT_NAME = title

