import pyexlatex as pl


def cf_link() -> pl.Hyperlink:
    from derobertis_cv.pldata.cover_letters.models import BLUE

    claimfound_link = pl.Hyperlink(
        'https://claimfound.com',
        pl.Bold(
            pl.TextColor('ClaimFound', color=BLUE)
        ),
    )
    return claimfound_link


def get_tech_company_desire_paragraph(company_abbreviation: str, a_position: str) -> str:
    return f"""
I believe I am an ideal fit at {company_abbreviation} as {a_position} as I not only have excellent
data science and research skills from completing the Ph.D. program, but I also have seven years of 
experience building production software, including the last four as Co-Founder and CTO of a 
software startup, {cf_link()}, which is focused on helping individuals find, process, and 
monitor for unclaimed property. For the first six months as CTO, I single-handedly created and deployed
the full-stack prototype of the web application. With the help of my Co-Founder, we raised enough
investment to build a team and so I transitioned into a combined product management, architecture, technical 
lead, developer support, and QA role. I created a management system drawing from Agile practices
and it effectively helped to plan and organize the development team that grew up to 10 members at one time.
We are now in the process of exiting the company so I am looking for an employer who would best benefit from my unique
combination of data science, software engineering, and product management experience.
""".strip()


def get_data_science_company_desire_paragraph(company_abbreviation: str, a_position: str) -> str:
    para = get_tech_company_desire_paragraph(company_abbreviation, a_position)
    para += ' ' + """
Together, these skills make me adept at conducting reproducible data science studies and communicating 
important conclusions to stakeholders. Within ClaimFound I built internal data science applications 
which connect to live data sources to visualize key user, server, and unclaimed property metrics 
on interactive dashboards, and I regularly 
had to communicate research findings to my non-technical Co-Founder.
        """.strip()
    return para


def get_banking_desire_paragraph(company_abbreviation: str, a_position: str) -> str:
    para = get_tech_company_desire_paragraph(company_abbreviation, a_position)
    para += ' ' + """
Further, I am familiar with credit risk work from both industry and supervisory
perspectives: I rebuilt the models for the Allowance for Loan
and Lease Losses and designed a stress testing program as a Portfolio Analyst at Eastern Virginia Bankshares, 
and I was an intern in the Credit Risk department at the Federal Reserve Board of Governors.
    """.strip()
    return para


def get_economist_desire_paragraph(company_abbreviation: str, a_position: str) -> str:
    para = f"""
I believe I am an ideal fit at {company_abbreviation} as {a_position} given my related research in market microstructure,
macroeconomics, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. Further, I have industry experience in credit risk modeling 
and stress testing 
from when I was a Portfolio Analyst at Eastern Virginia Bankshares and seven years of 
experience building production software, including the last four as Co-Founder and CTO of a 
software startup, {cf_link()}. I'm the only Ph.D. student who has 
been allowed to teach the Financial Modeling class at UF, due to my technical skills and forward thinking. 
I have given numerous informal seminars to fellow
Ph.D students on programming topics such as machine learning and Python for research applications, 
and I am widely viewed in the department as a resource on such topics. During my time at ClaimFound, 
in addition to the software side of building the full-stack prototype then recruiting and managing a development team, 
I also helped form the business model by developing new monetization methods and modeling their potential market 
and profit.
I have a strong interest in modeling and data science and am equally comfortable being both self-guided and a team
player providing high-quality results and recommendations.
    """.strip()
    return para