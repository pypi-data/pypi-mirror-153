import pyexlatex as pl
import pyexlatex.table as lt
import pyexlatex.presentation as lp
import pyexlatex.graphics as lg
import pyexlatex.layouts as ll
import pyexlatex.resume as lr
from pyexlatex.models.page.number import PageReference

from derobertis_cv import plbuild
from derobertis_cv.plbuild.paths import images_path
from derobertis_cv.pldata.constants.contact import CONTACT_LINES, NAME
from derobertis_cv.pldata.courses.fin_model import get_fin_model_course

AUTHORS = ['Nick DeRobertis']

DOCUMENT_CLASS = pl.Document
OUTPUT_LOCATION = plbuild.paths.DOCUMENTS_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = None

title = 'Diversity Statement'

blue = pl.RGB(50, 82, 209, color_name="darkblue")
financial_modeling_url = get_fin_model_course().website_url
modeling_link = pl.Hyperlink(
    financial_modeling_url,
    pl.Bold(
        pl.TextColor(financial_modeling_url, color=blue)
    ),
)
modeling_footnote = pl.Footnote(
    [pl.TextSize(-3), 'See the Financial Modeling course content at the course website: ', modeling_link])

def get_content():
    return [
        blue,
        pl.Hyperlink(''),
f"""
From my CV and cover letter, it should be apparent that I am not the typical Finance Ph.D. applicant: I have a much
larger emphasis on creating open-source software. My commitment to open-source is a commitment to inclusion and 
diversity: I believe everyone should have access to these tools regardless of their economic position, 
and that anyone should be able to contribute to them, regardless of their location in the world or cultural 
background.

I am a strong proponent of equal access to education, and I recognize the value of diverse backgrounds to
education and research efforts. While I was fortunate enough to be raised in a middle-class family, I understand 
some of the adverse impacts poverty can have on educational outcomes. I also realize that those with different 
socioeconomic and cultural backgrounds can bring unique perspectives which broaden our understanding of the world.

I always structure my courses to appeal to multiple learning styles including 
auditory, visual, and kinesthetic learning. Too many instructors focus on their preferred style but this will 
disadvantage large portions of the class. Going even further towards equal access, I have made the lecture videos 
and course materials from my Financial Modeling course publicly available{modeling_footnote}, 
so anyone with an internet connection 
can learn financial modeling with Python and Excel.

Going forward, I will make sure to bring these ideals of equal access into my work in the industry as well.
With the permission of my employer, I'd like to continue creating open-source software that increases access to the 
industry. Should I need to train anyone or present research findings, I will apply the same lessons I have learned in 
teaching my classes to ensure I am being as inclusive as possible.
""".strip()
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
OUTPUT_NAME = 'Industry Diversity Statement'

