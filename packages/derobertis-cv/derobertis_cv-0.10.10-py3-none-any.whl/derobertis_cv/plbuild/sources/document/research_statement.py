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

title = 'Research Statement'
blue = pl.RGB(50, 82, 209, color_name="darkblue")
software_link = pl.Hyperlink(
    SITE_URL + '/software',
    pl.Bold(
        pl.TextColor(SITE_URL + '/software', color=blue)
    ),
)
software_footnote = pl.Footnote(software_link)


def get_content():
    return [
        blue,
        pl.Hyperlink(''),
f"""
I have a broad array of research interests but I am mainly focused on
empirical asset pricing, behavioral finance, alternative assets, and monetary policy. 
A central theme in nearly all of my projects is a focus on financial markets, whether it is analyzing 
the performance of assets, the effects of government intervention, or the role of both fundamental and 
behavioral information in price discovery. I have a unique technical skill set that allows me to 
uncover novel data sets through 
web-scraping and API access, and also to work with large data sets. I am experienced with
machine learning and using it to make predictions and classifications. 
 
Automation and reproducibility are key 
components of my research philosophy: I believe that an empirical research project should be able to run from the original 
data sources to the end analysis and presentation with a single command, and this is how I structure all my projects. 
It will be necessary for the field to adopt these practices to solve the reproducibility crisis in finance research, 
and I want to help move the field towards this objective. I am doing this by isolating components of my research 
that could be useful for multiple projects, and restructuring them into open-source software 
packages{software_footnote} that anyone
can use for free. With every project, I become  
more productive, as I continue to build up my suite of research tools. I believe my development of these tools can make 
a large contribution to the field by improving the efficiency of all empirical researchers. 

My outstanding research contributes to multiple strands of the literature and could assist multiple stakeholders 
in making decisions. My study "Government Equity Capital Market Intervention and Stock Returns" with Andy 
Naranjo and Mahendrarajah Nimalendran informs central bank personnel about the effects of purchasing 
broad-index equity ETFs on asset prices over time, which is valuable information at a time when the 
Federal Reserve is pursuing unprecedented levels of market intervention and even purchasing corporate debt. My job 
market paper, "Valuation without Cash Flows: What are Cryptoasset Fundamentals?" gives cryptocurrency investors 
both a theoretical framework and empirical models to assess the value of these assets. The biggest drawback to 
cryptocurrencies as currencies today is their high volatility, owing in part to the lack of an established 
valuation framework. This research could lead to decreased aggregate volatility, increasing adoption and 
benefiting society through elimination of counterparty risk, increased transparency, and speed of payments. 
My joint work on "OSPIN: Informed Trading in Options and Stock Markets" with
Yong Jin, Mahendrarajah Nimalendran, and Sugata Ray develops a new model to estimate the probability of informed 
trading that is more accurate as it considers the information in both the stock and options markets jointly, 
whereas prior models considered only stock markets,
which should be useful to researchers analyzing the information structure of markets and especially volatility 
information. Finally, my work on
"Are Investors Paying (for) Attention?" furthers the behavioral asset pricing literature focusing on investor attention,
the understanding of which may lead to more efficient prices as investors incorporate these effects into their 
valuation models.

Each of my existing studies puts me down a path to do further research in those areas. So far I have focused primarily
on the asset pricing effects of central bank intervention in stock markets, but some initial work suggests there may 
be profound implications for how the market microstructure is affected including liquidity, volatility, and 
price informativeness. Further, corporate financing behavior changes markedly in response to such intervention. While
my job market paper establishes an effective valuation approach for cryptocurrencies, just as our understanding of 
stock returns has deepened over the last 60 years, I believe there is still a lot of work to be done in this area.
There are also unique features of the cryptoasset market that could lead to interesting microstructure effects, such as 
50-80\\% of the market capitalization being concentrated in a single asset (Bitcoin). 
Further, in that paper I explore the interaction 
of investor attention and sentiment, which I think deserves its own focused study. While I have a strong and 
direct pipeline I will
be focusing on, I am also open to exploring new fields if the right idea comes along and especially if it is related 
to financial markets, and all the while I will be working on improving the efficiency and reproducibility of all the
empirical research in our field.
"""
    ]

"""
Over time I want to push the field to share project code so that others 
can easily reproduce and extend it, and the results are more easily verified.
"""

DOCUMENT_CLASS_KWARGS = dict(
    remove_section_numbering=True,
    title=title,
    page_modifier_str='margin=1in',
    font_size=12,
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

