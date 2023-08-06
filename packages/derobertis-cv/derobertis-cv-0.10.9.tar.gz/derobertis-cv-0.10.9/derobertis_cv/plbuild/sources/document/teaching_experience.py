import pyexlatex as pl
import pyexlatex.table as lt
import pyexlatex.presentation as lp
import pyexlatex.graphics as lg
import pyexlatex.layouts as ll
import pyexlatex.resume as lr
from pyexlatex.models.format.text.linespacing import LineSpacing
from pyexlatex.models.page.number import PageReference
from pyexlatex.texgen.packages.default import default_packages

from derobertis_cv import plbuild
from derobertis_cv.plbuild.paths import images_path
from derobertis_cv.pldata.constants.contact import CONTACT_LINES, NAME
from derobertis_cv.pldata.courses.fin_model import get_fin_model_course

AUTHORS = ['Nick DeRobertis']

DOCUMENT_CLASS = pl.Document
OUTPUT_LOCATION = plbuild.paths.DOCUMENTS_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = None

title = 'Teaching Experience Overview'

fin_model = get_fin_model_course()


def get_content():
    return [
        pl.VSpace(-1.5),
        pl.Section([
"""
I have taught three courses across two universities and six semesters in a wide variety of formats. 
I have received 4.8/5 evaluations and the Warrington College of Business Ph.D. Student Teaching Award.
I am currently teaching Financial Modeling, a senior capstone course at UF, which is not usually taught 
by Ph.D. students, but an exception was made due to my teaching and technical skills. 
All of my classes teach practical skills in addition to the concepts, and I draw on my experience 
as a portfolio analyst to relate concepts to the real world.
"""
        ], title='Overview'),
        pl.Section([
            pl.SubSection([
"""
This course covers the full financial modeling workflow using both Excel and Python. It covers how to 
build a model in general, all the way from concept and data collection to the result and
visualization, and how to complete the various steps in either Excel or Python.
""",
                pl.UnorderedList([
                    [pl.Bold('University:'), 'University of Florida'],
                    [pl.Bold('Topics:'), 'Python programming, Excel, personal finance, capital budgeting, DCF valuation, '
                                         'Monte Carlo simulations, sensitivity analysis, scenario analysis'],
                    [pl.Bold('Semesters Taught:'), 'Fall 2019, Spring 2020, Fall 2020'],
                    [pl.Bold('Formats:'), 'In-person, online live, online asynchronous, '
                          'and online distributed (Public free course and YouTube channel)'],
                    [pl.Bold('Course Website:'), pl.TextColor(
                        pl.Underline(
                            pl.Hyperlink(fin_model.website_url, fin_model.website_url)
                        ),
                        'blue'
                    ),],
                ])
            ], title='Financial Modeling'),
            pl.SubSection([
"""
A fixed income course focusing on debt analysis and debt portfolio management, also covering the 
use of derivatives for risk management in fixed income portfolios.
""",
                pl.UnorderedList([
                    [pl.Bold('University:'), 'University of Florida'],
                    [pl.Bold('Topics:'),
                     'TVM, bond pricing, YTM, interest rates, risk analysis, term structure, duration, '
                     'convexity, immunization, bond options, interest rate swaps, CDS'],
                    [pl.Bold('Semesters Taught:'), 'Fall 2016, Spring 2018'],
                    [pl.Bold('Formats:'), 'In-person'],
                ])
            ], title='Debt and Money Markets'),
            pl.SubSection([
                """
                A lab taught as part of a financial management course which focuses on using 
                Excel to solve case problems.
                """,
                pl.UnorderedList([
                    [pl.Bold('University:'), 'Virginia Commonwealth University'],
                    [pl.Bold('Topics:'),
                     'Cell references, formulas, piovot tables, iteration, macros, regressions'],
                    [pl.Bold('Semesters Taught:'), 'Spring 2014'],
                    [pl.Bold('Formats:'), 'In-person'],
                ])
            ], title='Excel Lab')
        ], title='Courses')
    ]

DOCUMENT_CLASS_KWARGS = dict(
    remove_section_numbering=True,
    title=title,
    page_modifier_str='margin=1in,tmargin=0.2in',
    font_size=11,
    apply_page_style_to_section_starts=True,
    custom_footers=[
        pl.LeftFooter(NAME),
        pl.CenterFooter(title),
        pl.RightFooter(
            ['Page', pl.ThisPageNumber(), '\\', 'of', PageReference('LastPage')]
        ),
        pl.FooterLine()
    ],
    packages=default_packages + [
        pl.Package('hyperref', modifier_str='hidelinks=true'),
        'setspace',
        'enumitem',
        LineSpacing(0.85),
        pl.Raw(r'\setlist[itemize]{itemsep=0.035in}'),
    ]
)
OUTPUT_NAME = title

