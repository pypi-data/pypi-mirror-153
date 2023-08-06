import pyexlatex as pl
import pyexlatex.table as lt
import pyexlatex.presentation as lp
import pyexlatex.graphics as lg
import pyexlatex.layouts as ll
import pyexlatex.resume as lr
from pyexlatex.models.page.number import PageReference

from derobertis_cv import plbuild
from derobertis_cv.plbuild.paths import images_path
from derobertis_cv.pldata.constants.contact import CONTACT_LINES, NAME, SITE_URL

AUTHORS = ['Nick DeRobertis']

DOCUMENT_CLASS = pl.Document
OUTPUT_LOCATION = plbuild.paths.DOCUMENTS_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = None

title = 'Selected Research Works'

def get_content():
    return [
pl.Raw(r'\setlength{\parindent}{0em}'),
f"""Please find attached the following samples of research work:""",
        pl.UnorderedList([
            'Valuation without Cash Flows (Job Market Paper)',
            'Government Equity Market Intervention and the '
            'Cross-Section of Stock Returns (with Andy Naranjo and Mahendrarajah Nimalendran)',
            'OSPIN: Informed Trading in Options and Stock Markets '
            '(with Yong Jin, Mahendrarajah Nimalendran, and Sugata Ray)',
        ]),
"""
I have selected these working papers to give a diverse sample of my late-stage work. Valuation without Cash Flows 
is solo-authored and shows my knowledge of empirical asset pricing and cryptocurrencies. Government Equity Market 
Intervention and the Cross-Section of Stock Returns reveals my ability to evaluate government policies and their 
intended and unintended effects, as well as competency in machine learning. OSPIN: Informed Trading in Options 
and Stock Markets is a microstructure paper revolving around a theoretical model which we evaluate 
with Monte Carlo simulations and empirical tests.
"""
    ]



DOCUMENT_CLASS_KWARGS = dict(
    remove_section_numbering=True,
    title=title,
    page_modifier_str='margin=1in',
    font_size=12,
    apply_page_style_to_section_starts=True,
    custom_footers=[
        pl.LeftFooter(NAME),
        pl.CenterFooter(''),
        pl.RightFooter(title),
        pl.FooterLine()
    ]
)
OUTPUT_NAME = title

