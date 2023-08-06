import pyexlatex as pl
import pyexlatex.table as lt
import pyexlatex.presentation as lp
import pyexlatex.graphics as lg
import pyexlatex.layouts as ll
import pyexlatex.resume as lr
from pyexlatex.models.page.number import PageReference
from pyexlatex.texgen.packages.default import default_packages

from derobertis_cv import plbuild
from derobertis_cv.plbuild.paths import images_path
from derobertis_cv.pldata.constants.contact import CONTACT_LINES, NAME, SITE_URL
from derobertis_cv.pldata.courses.fin_model import get_fin_model_course

fin_model = get_fin_model_course()

AUTHORS = ['Nick DeRobertis']

DOCUMENT_CLASS = pl.Document
OUTPUT_LOCATION = plbuild.paths.DOCUMENTS_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = None

title = 'Teaching Portfolio'

def get_content():
    return [
pl.Raw(r'\setlength{\parindent}{0em}'),
f"""Please find attached the following evidence of teaching experience for the following courses:""",
        pl.UnorderedList([
            'Financial Modeling with Python and Excel (senior capstone)',
            pl.UnorderedList([
                [
                    'Course website:',
                    pl.TextColor(
                        pl.Underline(
                            pl.Hyperlink(fin_model.website_url, fin_model.website_url)
                        ),
                        'blue'
                    ),
                ],
                'Syllabus',
                'Course Schedule',
                'Evaluations (Fall 2019, Spring 2020, Fall 2020)',
                ['Note:', 'Taught across four different formats: in-person, online live, online asynchronous, '
                          'and online distributed (Public free course and YouTube channel)']
            ]),
            'Debt and Money Markets (fixed income course)',
            pl.UnorderedList([
                'Syllabus',
                'Evaluations (Fall 2016, Spring 2018)'
            ])
        ]),
        pl.VSpace(0.7),
        pl.Bold('Selected Teaching Interests'),
        pl.VSpace(0.4),
        ' ',
        """
        FinTech (cryptocurrencies, blockchain, machine learning/AI, decentralized finance, data science), 
        modeling, investments, derivatives, corporate finance, financial management
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
    ],
    packages=default_packages + [pl.Package('hyperref', modifier_str='hidelinks=true')]
)
OUTPUT_NAME = title

