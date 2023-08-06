from typing import List, Sequence

import pyexlatex as pl

from derobertis_cv.plbuild.paths import private_assets_path
from derobertis_cv.pldata.authors import AUTHORS
from derobertis_cv.pldata.constants.authors import NIMAL, ANDY, SUGATA
from derobertis_cv.pldata.cover_letters.models import CoverLetter, ApplicationComponents, ApplicationFocus, \
    CoverLetterDesireSection, SpecificApplicationFocus
from derobertis_cv.pldata.organizations import SEC_DERA_TARGET, OFR_TARGET, RICH_FED_TARGET, PLACEHOLDER_GOV_TARGET
import derobertis_cv.pldata.organizations as orgs
from derobertis_cv.pldata.universities import EL_PASO_TARGET, DRAKE_TARGET, PLACEHOLDER_UNIVERSITY_TARGET, \
    MONASH_TARGET, OREGON_STATE_TARGET, FIU_TARGET, UWM_TARGET
import derobertis_cv.pldata.universities as univs


def get_cover_letters() -> List[CoverLetter]:
    exclude_components: Sequence[ApplicationComponents] = (
        ApplicationComponents.OTHER_RESEARCH,
        ApplicationComponents.EMAIL_BODY,
        ApplicationComponents.COVER_LETTER_AS_EMAIL,
        ApplicationComponents.ALL,
        ApplicationComponents.REFERENCES,
        ApplicationComponents.COVER_LETTER,
        ApplicationComponents.INVESTOR_ATTENTION_PAPER,
        ApplicationComponents.PERSONAL_WEBSITE,
        ApplicationComponents.APPLICATION,
        ApplicationComponents.CODING_SAMPLE,
        ApplicationComponents.RESEARCH_LIST,
        ApplicationComponents.JMP_VIDEO,
        ApplicationComponents.PASSPORT_PHOTO,
        ApplicationComponents.SKILLS_LIST,
    )
    all_concrete_components = [comp for comp in ApplicationComponents if comp not in exclude_components]

    exclude_government_components: Sequence[ApplicationComponents] = (
        *exclude_components,
        ApplicationComponents.TEACHING_STATEMENT,
        ApplicationComponents.TEACHING_EXPERIENCE_OVERVIEW,
        ApplicationComponents.TEACHING_COVER,
        ApplicationComponents.DIVERSITY,
        ApplicationComponents.EVALUATIONS,
        ApplicationComponents.COURSE_OUTLINES,
    )

    all_government_components = [
        comp for comp in ApplicationComponents if comp not in exclude_government_components
    ]

    all_government_components_no_transcripts = [
        comp for comp in ApplicationComponents
        if comp not in (*exclude_government_components, ApplicationComponents.TRANSCRIPTS)
    ]

    exclude_industry_components: Sequence[ApplicationComponents] = (
        *exclude_government_components,
        ApplicationComponents.TRANSCRIPTS,
        ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
        ApplicationComponents.OPIN_PAPER,
        ApplicationComponents.RESEARCH_STATEMENT,
    )

    all_industry_components = [
        comp for comp in ApplicationComponents if comp not in exclude_industry_components
    ]

    courses_site_footnote = pl.Footnote(
        f'See all the course topics on the {CoverLetter.site_link("courses page", "courses")} of my personal website.'
    )

    return [
        CoverLetter(
            PLACEHOLDER_GOV_TARGET,
            [
"""
(Organization-specific paragraph)
""",
            ],
            included_components=all_concrete_components,
            focus=ApplicationFocus.GOVERNMENT,
        ),
        CoverLetter(
            PLACEHOLDER_UNIVERSITY_TARGET,
            [
                """
                (School-specific paragraph)
                """,
            ],
            included_components=all_concrete_components,
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            orgs.PLACEHOLDER_INDUSTRY_TARGET,
            [
                """
                (Organization-specific paragraph)
                """,
            ],
            included_components=all_concrete_components,
            focus=ApplicationFocus.INDUSTRY,
            use_resume=True,
        ),
        CoverLetter(
            SEC_DERA_TARGET,
            CoverLetterDesireSection(
                orgs.SEC_DERA_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.OTHER_FINANCIAL_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.TRANSCRIPTS,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.REFERENCES,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.90,
            line_spacing=0.8,
            references_are_being_submitted=False,
            references_were_previously_submitted=True,
            cv_modifier_func=orgs.get_dera_cv_model,
        ),
        CoverLetter(
            EL_PASO_TARGET,
            [
"""
I believe I am an ideal fit at UTEP given that you are looking for an applicant in the area of investments and 
corporate finance, and I have research work in both. Further, the posting mentions FinTech under the preferred
specialties, and my Financial Modeling course is geared towards preparation for FinTech roles considering it 
combines finance knowledge and programming. On a personal level, my wife and I both have an affinity for 
mid-size cities and warm weather.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            DRAKE_TARGET,
            [
"""
I believe I am an ideal fit at DU given that you are looking for an applicant who can teach corporate finance, 
valuation, and FinTech, and my Financial Modeling course hits on all these topics. I teach programming and 
modeling skills that prepare students for FinTech roles, and the projects in the course are related to 
DCF valuation and capital budgeting. Further, most of my research work involves valuation and my job market
paper is in the FinTech area due to the topic of cryptocurrencies. On a personal level, my wife and I both 
have an affinity for mid-size cities and outdoor activities so I think we would feel right at home in Des Moines.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.DIVERSITY,
                ApplicationComponents.TRANSCRIPTS,
                ApplicationComponents.EVALUATIONS,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            OFR_TARGET,
            [
"""
I believe I am an ideal fit at OFR as a Research Economist given my related research in market microstructure and 
macroeconomics, as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. Further, I have a locational preference towards Washington, DC as my family lives in
Northern Virginia. Should I be selected, I would like to start at the end of July or beginning of August, but
I can be flexible on the timing.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER
            ],
            focus=ApplicationFocus.GOVERNMENT,
            as_email=True
        ),
        CoverLetter(
            RICH_FED_TARGET,
            [
"""
I believe I am an ideal fit at the Richmond Fed as a Financial Economist given my related research in market microstructure, 
macroeconomics, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I am familiar with the Fed's supervisory work from both ends: 
I was an intern in the Credit Risk department at the Board of Governors and I worked directly with examiners in my 
role as a Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses at 
Eastern Virginia Bankshares. 
I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Virginia so Charlotte and Baltimore would both be 
great locations for us.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.INVESTOR_ATTENTION_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            MONASH_TARGET,
            [
"""
I believe I am an ideal fit at MU given that you are looking for an applicant with research and 
teaching experience in complex financial instruments, financial modeling, and international
finance. As my job market paper develops a model of cryptocurrency valuation and tests it empirically,
it is related to the first two of those areas. The Government Equity Capital Market Intervention study analyzes 
the effects of the Bank of Japan intervening in equity markets through
ETF purchases so it is related to the third. Finally, by the time I would start I will have two years 
of experience teaching my Financial Modeling course. On a personal level, my wife and I have been interested 
in living abroad and would like to be in a larger city with warm weather so Melbourne seems like a great fit.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            line_spacing=1.1,
            by_email=True,
        ),
        CoverLetter(
            OREGON_STATE_TARGET,
            [
"""
My multiple lines of research and strong work ethic will contribute to the College of Business' goal of preeminence in 
research. Further, I will contribute to the goals of innovation and transformative, accessible education. 
It may already be apparent that I am not the typical Finance Ph.D. applicant: I have a much
larger emphasis on creating open-source software. My commitment to open-source is a commitment to inclusion and 
diversity: I believe everyone should have access to these tools regardless of their economic position, 
and that anyone should be able to learn from them, regardless of their location in the world or cultural 
background. I have already built tools for both research and education, and I want to continue innovating
at a university that encourages such efforts. On a personal level, my wife and I have always wanted to move to the 
West Coast and we enjoy outdoor activities so Corvallis seems like a good fit.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.EVALUATIONS
            ],
            focus=ApplicationFocus.ACADEMIC,
            custom_file_renames={
                ApplicationComponents.JOB_MARKET_PAPER: 'Job Market Paper',
            }
        ),
        CoverLetter(
            FIU_TARGET,
            CoverLetterDesireSection(FIU_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.TRANSCRIPTS,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
            ],
            focus=ApplicationFocus.ACADEMIC,
            line_spacing=1.1,
            font_scale=1.05,
        ),
        CoverLetter(
            UWM_TARGET,
            CoverLetterDesireSection(UWM_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.REFERENCES,
            ],
            focus=ApplicationFocus.ACADEMIC,
            line_spacing=1.1,
            font_scale=1.05,
        ),
        CoverLetter(
            univs.QUEENS_TARGET,
            CoverLetterDesireSection(univs.QUEENS_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.COURSE_OUTLINES,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.RESEARCH_STATEMENT,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            univs.UMASS_BOSTON_TARGET,
            [
"""
I believe I am an ideal fit at UMass Boston as you are looking for an applicant in the field of 
financial technology. I have applied machine learning and textual analysis in my research,  
my job market paper is focused on cryptoassets, I am currently researching the broader decentralized 
finance space, and I have deep expertise in programming and 
data science. You are also looking for someone to teach Ph.D. students this kind of material,
and beyond my multiple full undergraduate courses, I have given numerous informal seminars to fellow
Ph.D students on programming topics such as web-scraping, automation, Python for research applications, 
and machine learning,
and I am widely viewed in the department as a resource on such topics. I also very much enjoy teaching Ph.D. students
as we can cover much more material and it is more likely to lead to research ideas and collaboration. On a personal 
level, my wife and I have an affinity for larger cities and we already have family near Boston so it seems 
like a good fit.
""",
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC
        ),
        CoverLetter(
            univs.CAL_STATE_FULLERTON_TARGET,
f"""
I believe I am an ideal fit at CSUF as you are looking for an applicant in the field of investments.
Nearly all of my research work is focused on investments whether it be stocks, options, or cryptoassets. 
Further, both of the courses I've developed and taught, Debt and Money Markets and Financial Modeling,
have substantial portions devoted to investment-related topics.{courses_site_footnote}
On a personal level, my wife and I have an affinity for mid-side
cities, the West Coast, and warm weather so Fullerton seems like a good fit.
""",
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.TRANSCRIPTS,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.DIVERSITY,
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Nick DeRobertis Research Works': [
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ]
            },
            custom_file_renames={
                ApplicationComponents.CV: 'Nick DeRobertis CV',
                ApplicationComponents.DIVERSITY: 'Nick DeRobertis Statement on Commitment to Inclusive Excellence'
            }
        ),
        CoverLetter(
            univs.WILFRID_LAURIER_TARGET,
            CoverLetterDesireSection(univs.WILFRID_LAURIER_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.ACADEMIC,
            by_email=True,
            add_organization_name_to_address=False,
            custom_file_renames={
                ApplicationComponents.CV: 'Nick DeRobertis CV',
                ApplicationComponents.COVER_LETTER: 'Nick DeRobertis Cover Letter AP Finance 2020-04'
            }
        ),
        CoverLetter(
            orgs.OCC_MARKET_RAD_TARGET,
            [
"""
I believe I am an ideal fit at OCC Market RAD as a Financial Economist given my related research in asset pricing,
market microstructure, 
macroeconomics, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I am familiar with banking supervisory work from both ends: 
I was an intern in the Credit Risk department at the Federal Reserve Board of Governors and 
I worked directly with examiners in my 
role as a Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses and developing 
a stress testing program at 
Eastern Virginia Bankshares. 
I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. I am a U.S. citizen so I look forward to serving my country in this capacity.
On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Northern Virginia so DC would be a 
great location for us.
"""
            ],
            included_components=all_government_components_no_transcripts,
            focus=ApplicationFocus.GOVERNMENT,
            as_email=True
        ),
        CoverLetter(
            orgs.OCC_CCRAD_TARGET,
            [
"""
I believe I am an ideal fit at OCC CCRAD as a Financial Economist given my related research in asset pricing,
market microstructure, 
macroeconomics, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I am familiar with banking supervisory work from both ends: 
I was an intern in the Credit Risk department at the Federal Reserve Board of Governors and 
I worked directly with examiners in my 
role as a Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses and developing 
a stress testing program at 
Eastern Virginia Bankshares. 
I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. I am a U.S. citizen so I look forward to serving my country in this capacity.
On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Northern Virginia so DC would be a 
great location for us.
"""
            ],
            included_components=all_government_components_no_transcripts,
            focus=ApplicationFocus.GOVERNMENT,
            as_email=True
        ),
        CoverLetter(
            orgs.SEC_OIAD_TARGET,
            [
"""
I believe I am an ideal fit at OIAD as a Financial Economic Fellow given my related research in behavioral finance,
asset pricing, and corporate finance, as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Northern Virginia so DC would be a 
great location for us.
""",
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.93,
            by_email=True
        ),
        CoverLetter(
            univs.U_TORONTO_SCARBOROUGH_TARGET,
            CoverLetterDesireSection(univs.U_TORONTO_SCARBOROUGH_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.COURSE_OUTLINES,
                ApplicationComponents.EVALUATIONS,
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Nick DeRobertis Application Package': [
                    ApplicationComponents.RESEARCH_STATEMENT,
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                    ApplicationComponents.TEACHING_STATEMENT,
                    ApplicationComponents.COURSE_OUTLINES,
                    ApplicationComponents.EVALUATIONS,
                ]
            },
            output_compression_level=1
        ),
        CoverLetter(
            univs.AMSTERDAM_TARGET,
            CoverLetterDesireSection(univs.AMSTERDAM_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            as_email=True,
        ),
        CoverLetter(
            orgs.NY_FED_TARGET,
            [
"""
I believe I am an ideal fit at FRBNY as a Financial Economist given my related research in market microstructure, 
macroeconomics, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I am familiar with the Fed's supervisory work from both ends: 
I was an intern in the Credit Risk department at the Board of Governors and I worked directly with examiners in my 
role as a Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses at 
Eastern Virginia Bankshares. 
I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. On a personal level, my wife and I both 
have an affinity for large cities and have family near New York so it would be a 
great location for us.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.TRANSCRIPTS,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
            output_compression_level=1,
        ),
        CoverLetter(
            univs.COPENHAGEN_TARGET,
            CoverLetterDesireSection(univs.COPENHAGEN_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.REFERENCES,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            univs.HEC_PARIS_TARGET,
"""
I believe I am an ideal fit at HEC as you are looking for an applicant in the fields of
Finance and AI, Big Data, Blockchains, Cryptocurrencies, and FinTech. 
I have applied machine learning, AI, and textual analysis in my research,  
my job market paper is focused on cryptocurrencies, I am currently researching the broader decentralized 
finance space, and I have deep expertise in programming and 
data science involving large data sets. Beyond my multiple full undergraduate courses, 
I have given numerous informal seminars to fellow
Ph.D students on programming topics such as machine learning/AI and Python for research applications, 
and I am widely viewed in the department as a resource on such topics. I believe the industry is headed 
more towards quantitative finance, machine learning, and big data, and I would be excited at the opportunity 
to continue researching and to teach students these areas. On a personal level, my wife and I have an affinity for larger
cities, and have been hoping for an opportunity to live abroad from the US, so Paris and France seem like
a good fit.
""",
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.JMP_VIDEO,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            univs.POMPEU_FABRA_TARGET,
            CoverLetterDesireSection(univs.POMPEU_FABRA_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.TRANSCRIPTS,
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Nick DeRobertis UPF Cover Letter and Transcripts': [
                    ApplicationComponents.COVER_LETTER,
                    ApplicationComponents.TRANSCRIPTS,
                ]
            }
        ),
        CoverLetter(
            orgs.WORLD_BANK_DRG_TARGET,
            [
"""
I believe I am an ideal fit at DRG as a Researcher given my related research in macroeconomics, 
economic policy,
market microstructure, and corporate finance, 
as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I have a strong interest in development issues
and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations.
On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Northern Virginia so DC would be a 
great location for us.
"""
            ],
            included_components=[
                ApplicationComponents.PERSONAL_WEBSITE,
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
        ),
        CoverLetter(
            univs.EDHEC_TARGET,
            [
"""
I believe I am an ideal fit at EDHEC as you are looking for an applicant willing to teach 
Mathematical Finance or Machine Learning for Finance. I have applied machine learning and textual analysis in my research,  
I do some theory work, and I have deep expertise in programming and 
data science. Beyond my multiple full undergraduate courses, I have given numerous informal seminars to fellow
Ph.D students on programming topics such as machine learning and Python for research applications, 
and I am widely viewed in the department as a resource on such topics. I believe the industry is headed 
more towards quantitative finance, machine learning, and big data, and I would be excited at the opportunity 
to teach students these skills. On a personal level, my wife and I have an affinity for larger
cities, and have been hoping for an opportunity to live abroad from the US, so Paris and France seem like
a good fit.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.REFERENCES,
            ],
            included_references=[AUTHORS[ANDY], AUTHORS[NIMAL]],
            focus=ApplicationFocus.ACADEMIC,
            by_email=True
        ),
        CoverLetter(
            orgs.FED_BOARD_TARGET,
            [
"""
I believe I am an ideal fit at the Board as a Financial Economist given my related research in market microstructure, 
macroeconomics, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I am familiar with the Fed's supervisory work from both ends: 
I was an intern in the Credit Risk department at the Board and I worked directly with examiners in my 
role as a Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses at 
Eastern Virginia Bankshares. 
I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Northern Virginia so DC would be a 
great location for us.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.DIVERSITY,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            univs.BOCCONI_TARGET,
"""
I believe I am an ideal fit at Bocconi as you are looking for an applicant in the fields of 
Financial Markets, Financial Institutions, Corporate Finance, and Mathematical Finance. 
My research touches on all of these components: all of my research is related to financial markets,
my Government Intervention paper focuses on financial institutions and several of my works in progress 
are related to corporate finance.
As far as Mathematical Finance, I have applied machine learning and textual analysis in my research,  
I do some theory work, and I have deep expertise in programming and 
data science. Beyond my multiple full undergraduate courses, I have given numerous informal seminars to fellow
Ph.D students on programming topics such as machine learning and Python for research applications, 
and I am widely viewed in the department as a resource on such topics. On a personal level, my wife 
and I have an affinity for larger
cities, have been hoping for an opportunity to live abroad from the US, and much of my ancestry is Italian
so Milan and Italy seem like a good fit.
""",
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.JMP_VIDEO
            ],
            focus=ApplicationFocus.ACADEMIC,
            video_output_format='mp4',
            video_desired_size_mb=5,
            combine_files={
                'Cover Letter and Other Research Work': [
                    ApplicationComponents.COVER_LETTER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ]
            },
            output_compression_level=1,
        ),
        CoverLetter(
            orgs.NORGES_TARGET,
            CoverLetterDesireSection(
                orgs.NORGES_TARGET, ApplicationFocus.GOVERNMENT, specific_focus=SpecificApplicationFocus.BANKING_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.JMP_VIDEO,
                ApplicationComponents.TRANSCRIPTS,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.RESEARCH_STATEMENT,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.9,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.FED_DALLAS_TARGET,
            CoverLetterDesireSection(
                orgs.FED_DALLAS_TARGET, ApplicationFocus.GOVERNMENT, specific_focus=SpecificApplicationFocus.BANKING_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.JMP_VIDEO,
                ApplicationComponents.TRANSCRIPTS,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.RESEARCH_STATEMENT,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.9,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.CFPB_TARGET,
            CoverLetterDesireSection(
                orgs.CFPB_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.BANKING_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.TRANSCRIPTS,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.9,
            line_spacing=0.8,
            cv_modifier_func=orgs.get_cfpb_cv_model,
        ),
        CoverLetter(
            univs.HEC_MONTREAL_TARGET,
            CoverLetterDesireSection(univs.HEC_MONTREAL_TARGET, ApplicationFocus.ACADEMIC,
                                     extra_content=['I am willing to devote my free time in '
                                                    'the beginning to become fluent in French.',
                                                    '\n']
                                     ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            orgs.BIS_TARGET,
            CoverLetterDesireSection(
                orgs.BIS_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.BANKING_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.FED_SF_TARGET,
            CoverLetterDesireSection(
                orgs.FED_SF_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.BANKING_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
            by_email=True,
        ),
        CoverLetter(
            orgs.FED_ATLANTA_TARGET,
            CoverLetterDesireSection(
                orgs.FED_ATLANTA_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.BANKING_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.UBER_TARGET,
            CoverLetterDesireSection(
                orgs.UBER_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.TECH_COMPANY
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.INDUSTRY,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.MICROSOFT_ECONOMIST_TARGET,
            CoverLetterDesireSection(
                orgs.MICROSOFT_ECONOMIST_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.TECH_COMPANY
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.INDUSTRY,
            font_scale=0.9,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.BARCLAYS_TARGET,
            CoverLetterDesireSection(
                orgs.BARCLAYS_TARGET, ApplicationFocus.SEMI_ACADEMIC,
                specific_focus=SpecificApplicationFocus.ASSET_MANAGER
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.SEMI_ACADEMIC,
            font_scale=0.95,
            line_spacing=0.8,
            references_are_being_submitted=False,
            as_email=True,
        ),
        CoverLetter(
            orgs.UPSTART_TARGET,
            CoverLetterDesireSection(
                orgs.UPSTART_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.TECH_COMPANY
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.INDUSTRY,
            font_scale=0.9,
            line_spacing=0.8,
            references_are_being_submitted=False
        ),
        CoverLetter(
            orgs.TREASURY_OMA_TARGET,
            CoverLetterDesireSection(
                orgs.TREASURY_OMA_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.OTHER_FINANCIAL_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.TRANSCRIPTS,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.9,
            line_spacing=0.8,
            by_email=True,
            cv_modifier_func=orgs.get_treasury_oma_cv_model,
            output_compression_level=1,
            custom_file_renames={
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER: 'Government Equity Market Intervention',
            }
        ),
        CoverLetter(
            univs.ESSEC_TARGET,
            CoverLetterDesireSection(univs.ESSEC_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            orgs.FED_PHILLY_ML_TARGET,
"""
I believe I am an ideal fit at FRBP as a Machine Learning Economist given my related research in market
microstructure, macroeconomics, and economic policy as well as technical skills related to developing economic
models and communicating insights from large quantities of data. 
I have applied machine learning and textual analysis in my research, have given numerous informal seminars 
to fellow Ph.D students on programming topics such as machine learning and Python for research applications, 
and I am widely viewed in the department as a resource on such topics. 
I am familiar with banking supervisory work
from both ends: I was an intern in the Credit Risk department at the Federal Reserve Board of Governors and I
worked directly with bank examiners in my role as a Portfolio Analyst rebuilding the models for the Allowance
for Loan and Lease Losses at Eastern Virginia Bankshares. I have a strong interest in regulatory issues in
financial markets and am equally comfortable being both self-guided and a team player providing high-quality
results and recommendations. On a personal level, my wife and I have an affinity for larger cities and we have
family close by so Philadelphia seems like a good fit.
""",
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.JMP_VIDEO,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.9,
            line_spacing=0.8,
        ),
        CoverLetter(
            univs.NOVA_TARGET,
            CoverLetterDesireSection(univs.NOVA_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            orgs.FDIC_CFR_TARGET,
            CoverLetterDesireSection(
                orgs.FDIC_CFR_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.BANKING_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.GAO_TARGET,
            CoverLetterDesireSection(
                orgs.GAO_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.OTHER_FINANCIAL_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.TRANSCRIPTS,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            univs.NOTTINGHAM_TARGET,
            CoverLetterDesireSection(univs.NOTTINGHAM_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.JMP_VIDEO,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.RESEARCH_STATEMENT
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            univs.CHAPMAN_TARGET,
            CoverLetterDesireSection(univs.CHAPMAN_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.APPLICATION,
            ],
            focus=ApplicationFocus.ACADEMIC,
            file_locations={
                ApplicationComponents.APPLICATION: private_assets_path('Chapman Application Nick DeRobertis.pdf')
            },
            by_email=True,
        ),
        CoverLetter(
            univs.CENTRAL_EUROPEAN_TARGET,
            """
I believe I am an ideal fit at CEU as you are looking for an applicant in the area of
applied econometrics with a focus on machine learning. I have applied machine learning and textual 
analysis in my research, and I have deep expertise in programming and 
data science. I hope to further our understanding on how machine learning can be applied in 
empirical finance and economics research, especially around extracting meaning out of 
the predictions made by such models. Beyond my multiple full undergraduate courses, 
I have given numerous informal seminars to fellow
Ph.D students on programming topics such as machine learning and Python for research applications, 
and I am widely viewed in the department as a resource on such topics. I believe the industry is headed 
more towards quantitative finance, machine learning, and big data, and I would be excited at the opportunity 
to teach students these skills. On a personal level, my wife and I have an affinity for larger
cities, and have been hoping for an opportunity to live abroad from the US, so Vienna and Austria seem like
a good fit.
            """,
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.JMP_VIDEO,
            ],
            focus=ApplicationFocus.ACADEMIC,
            included_references=[
                AUTHORS[ANDY], AUTHORS[NIMAL]
            ]
        ),
        CoverLetter(
            orgs.FED_CHICAGO_TARGET,
            CoverLetterDesireSection(
                orgs.FED_CHICAGO_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.BANKING_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.DIVERSITY,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.FED_KANSAS_TARGET,
            CoverLetterDesireSection(
                orgs.FED_KANSAS_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.BANKING_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            combine_files={
                'Research Papers': [
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ]
            },
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            univs.IMPERIAL_COLLEGE_TARGET,
            CoverLetterDesireSection(univs.IMPERIAL_COLLEGE_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            orgs.BEA_TARGET,
            CoverLetterDesireSection(
                orgs.BEA_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.OTHER_FINANCIAL_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.JCT_TARGET,
            CoverLetterDesireSection(
                orgs.JCT_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.OTHER_FINANCIAL_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
            by_email=True
        ),
        CoverLetter(
            orgs.GS_GMR_TARGET,
            CoverLetterDesireSection(
                orgs.GS_GMR_TARGET, ApplicationFocus.SEMI_ACADEMIC,
                specific_focus=SpecificApplicationFocus.ASSET_MANAGER
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.SEMI_ACADEMIC,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.AIR_LIQUIDE_TARGET,
            CoverLetterDesireSection(
                orgs.AIR_LIQUIDE_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.TECH_COMPANY
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.INDUSTRY,
            combine_files={
                'Research Papers': [
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ]
            },
            font_scale=0.9,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.AFINITI_TARGET,
            CoverLetterDesireSection(
                orgs.AFINITI_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.TECH_COMPANY
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            included_references=[
                AUTHORS[ANDY], AUTHORS[NIMAL]
            ],
            focus=ApplicationFocus.INDUSTRY,
            font_scale=0.9,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.FUTUREPROOF_TARGET,
            CoverLetterDesireSection(
                orgs.FUTUREPROOF_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.TECH_COMPANY,
                extra_professional_content="""
I am especially interested in FutureProof as I have often lamented that I could not make a greater impact on 
the world as a finance academic, so I was ecstatic to find an opportunity to mitigate climate change from 
this perspective.
                """.strip()
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.CODING_SAMPLE,
            ],
            references_are_being_submitted=False,
            focus=ApplicationFocus.INDUSTRY,
            font_scale=0.9,
            line_spacing=0.8,
            as_email=True,
        ),
        CoverLetter(
            orgs.NOVI_TARGET,
            CoverLetterDesireSection(
                orgs.NOVI_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.TECH_COMPANY,
                extra_professional_content="""
I am especially interested in Novi as I have long believed that digital currencies will revolutionize payments, 
and that the main barrier was an easy to use, secure wallet which handles currency conversion automatically. It 
would be exciting to be part of a team making that a reality. I even already have substantial knowledge and 
experience in the field from researching the valuation of cryptocurrencies in my job market paper.
                    """.strip()
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.SKILLS_LIST,
            ],
            included_references=[
                AUTHORS[ANDY], AUTHORS[NIMAL],
            ],
            focus=ApplicationFocus.INDUSTRY,
            font_scale=0.85,
            line_spacing=0.75,
        ),
        CoverLetter(
            orgs.UBER_FREIGHT_TARGET,
            CoverLetterDesireSection(
                orgs.UBER_FREIGHT_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.TECH_COMPANY,
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            references_are_being_submitted=False,
            focus=ApplicationFocus.INDUSTRY,
            font_scale=0.85,
            line_spacing=0.75,
        ),
        CoverLetter(
            orgs.FACEBOOK_TARGET,
            CoverLetterDesireSection(
                orgs.FACEBOOK_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.TECH_COMPANY,
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.INDUSTRY,
            font_scale=0.9,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.OLIVER_WYMAN_TARGET,
"""
I believe I am an ideal fit at Oliver Wyman as an Analyst as I have experience analyzing and 
visualizing large data sets, predicting and classifying using machine learning, and have industry 
experience in credit risk modeling. 
""",
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.TRANSCRIPTS,
            ],
            focus=ApplicationFocus.SEMI_ACADEMIC,
            font_scale=1.1,
            line_spacing=1.2,
            include_general_overview=False,
            references_are_being_submitted=False,
            included_references=[
                AUTHORS[SUGATA], AUTHORS[ANDY], AUTHORS[NIMAL]
            ]
        ),
        CoverLetter(
            univs.UT_ARLINGTON_TARGET,
            CoverLetterDesireSection(univs.UT_ARLINGTON_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.DIVERSITY,
            ],
            focus=ApplicationFocus.ACADEMIC,
            references_are_being_submitted=False,
        ),
        CoverLetter(
            univs.WHU_OTTO_BEISHEIM_TARGET,
            CoverLetterDesireSection(univs.WHU_OTTO_BEISHEIM_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.EVALUATIONS,
            ],
            focus=ApplicationFocus.ACADEMIC,
            references_are_being_submitted=False,
        ),
        CoverLetter(
            univs.NATIONAL_SINGAPORE_TARGET,
            CoverLetterDesireSection(univs.NATIONAL_SINGAPORE_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            by_email=True
        ),
        CoverLetter(
            univs.BI_NORWEGIAN_TARGET,
            CoverLetterDesireSection(univs.BI_NORWEGIAN_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            by_email=True
        ),
        CoverLetter(
            univs.UC_SAN_DIEGO_TARGET,
            CoverLetterDesireSection(univs.UC_SAN_DIEGO_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.DIVERSITY,
            ],
            focus=ApplicationFocus.ACADEMIC,
            references_are_being_submitted=False,
        ),
        CoverLetter(
            univs.CHINESE_HONG_KONG_TARGET,
            CoverLetterDesireSection(univs.CHINESE_HONG_KONG_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            output_compression_level=1,
        ),
        CoverLetter(
            univs.SINGAPORE_MANAGEMENT_TARGET,
            CoverLetterDesireSection(univs.SINGAPORE_MANAGEMENT_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.RESEARCH_COVER,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.EVALUATIONS,
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Selected Research': [
                    ApplicationComponents.RESEARCH_COVER,
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ]
            },
            output_compression_level=1,
        ),
        CoverLetter(
            univs.ERASMUS_ROTTERDAM_TARGET,
            CoverLetterDesireSection(univs.ERASMUS_ROTTERDAM_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            by_email=True,
        ),
        CoverLetter(
            univs.CITY_HONG_KONG_TARGET,
            CoverLetterDesireSection(univs.CITY_HONG_KONG_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            univs.HKU_BUSINESS_TARGET,
            CoverLetterDesireSection(univs.HKU_BUSINESS_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.EVALUATIONS,
            ],
            focus=ApplicationFocus.ACADEMIC,
            custom_file_renames={
                ApplicationComponents.OPIN_PAPER: 'OSPIN Informed Trading in Options and Stock Markets'
            }
        ),
        CoverLetter(
            univs.PONTIFICIA_CHILE_TARGET,
            CoverLetterDesireSection(univs.PONTIFICIA_CHILE_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.JMP_VIDEO
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            orgs.CAPITAL_ONE_TARGET,
            CoverLetterDesireSection(
                orgs.CAPITAL_ONE_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.BANK,
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.INDUSTRY,
            font_scale=0.85,
            line_spacing=0.75,
            references_are_being_submitted=False,
        ),
        CoverLetter(
            orgs.JACOBS_LEVY_TARGET,
            CoverLetterDesireSection(
                orgs.JACOBS_LEVY_TARGET, ApplicationFocus.SEMI_ACADEMIC,
                specific_focus=SpecificApplicationFocus.ASSET_MANAGER
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.SEMI_ACADEMIC,
            font_scale=0.95,
            line_spacing=0.8,
            references_are_being_submitted=False,
        ),
        CoverLetter(
            univs.VRIJE_AMSTERDAM_TARGET,
            CoverLetterDesireSection(univs.VRIJE_AMSTERDAM_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            as_email=True,
        ),
        CoverLetter(
            univs.PARIS_DAUPHINE_TARGET,
            CoverLetterDesireSection(univs.PARIS_DAUPHINE_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.PASSPORT_PHOTO,
            ],
            focus=ApplicationFocus.ACADEMIC,
            by_email=True,
        ),
        CoverLetter(
            orgs.GEODE_CAPITAL_TARGET,
            CoverLetterDesireSection(
                orgs.GEODE_CAPITAL_TARGET, ApplicationFocus.SEMI_ACADEMIC,
                specific_focus=SpecificApplicationFocus.ASSET_MANAGER
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.SEMI_ACADEMIC,
            font_scale=0.95,
            line_spacing=0.8,
            references_are_being_submitted=False,
            by_email=True,
        ),
        CoverLetter(
            orgs.FED_BOSTON_TARGET,
            CoverLetterDesireSection(
                orgs.FED_BOSTON_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.BANKING_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
            by_email=True
        ),
        CoverLetter(
            orgs.VANGUARD_QEG_TARGET,
            CoverLetterDesireSection(
                orgs.VANGUARD_QEG_TARGET, ApplicationFocus.SEMI_ACADEMIC,
                specific_focus=SpecificApplicationFocus.ASSET_MANAGER
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.SEMI_ACADEMIC,
            font_scale=0.95,
            line_spacing=0.8,
            references_are_being_submitted=False,
        ),
        CoverLetter(
            orgs.FHFA_DBR_TARGET,
            CoverLetterDesireSection(
                orgs.FHFA_DBR_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.BANKING_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.TRANSCRIPTS,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.STEVENS_CAPITAL_TARGET,
            CoverLetterDesireSection(
                orgs.STEVENS_CAPITAL_TARGET, ApplicationFocus.SEMI_ACADEMIC,
                specific_focus=SpecificApplicationFocus.ASSET_MANAGER
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.SEMI_ACADEMIC,
            font_scale=0.95,
            line_spacing=0.8,
            references_are_being_submitted=False,
        ),
        CoverLetter(
            orgs.FED_PHILLY_RADAR_TARGET,
            CoverLetterDesireSection(
                orgs.FED_PHILLY_RADAR_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.BANKING_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.TRANSCRIPTS,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            univs.HONG_KONG_BAPTIST_TARGET,
            CoverLetterDesireSection(univs.HONG_KONG_BAPTIST_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.TRANSCRIPTS,
            ],
            included_references=[AUTHORS[ANDY], AUTHORS[NIMAL]],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Nick DeRobertis Cover and CV': [
                    ApplicationComponents.COVER_LETTER,
                    ApplicationComponents.CV
                ]
            }
        ),
        CoverLetter(
            univs.BOSTON_U_TARGET,
            """
I believe I am an ideal fit at BU as you are looking for an applicant in the area of
FinTech. My job market paper is focused on cryptoassets and I am exploring research ideas in the 
decentralized finance space enabled by blockchain technology. I have applied machine learning and textual 
analysis in my research, and I have deep expertise in programming and 
data science. I hope to further our understanding on how machine learning can be applied in 
empirical finance and economics research, especially around extracting meaning out of 
the predictions made by such models. Beyond my multiple full undergraduate courses, 
I have given numerous informal seminars to fellow
Ph.D students on programming topics such as machine learning and Python for research applications, 
and I am widely viewed in the department as a resource on such topics. I believe the industry is headed 
more towards quantitative finance, machine learning, and big data, and I would be excited about the opportunity 
to teach students these skills. On a personal level, my wife and I have an affinity for larger cities and we have
family close by so Boston seems like a good fit.
            """,
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            cv_modifier_func=univs.get_bu_cv_model,
        ),
        CoverLetter(
            univs.WASHINGTON_STATE_TARGET,
            CoverLetterDesireSection(univs.WASHINGTON_STATE_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.REFERENCES,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            univs.ESADE_TARGET,
            CoverLetterDesireSection(univs.ESADE_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.RESEARCH_COVER,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            by_email=True
        ),
        CoverLetter(
            univs.WESTERN_TARGET,
            CoverLetterDesireSection(univs.WESTERN_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.APPLICATION,
            ],
            focus=ApplicationFocus.ACADEMIC,
            file_locations={
                ApplicationComponents.APPLICATION: private_assets_path('Nick DeRobertis Ivey Application.pdf')
            },
            by_email=True,
        ),
        CoverLetter(
            orgs.CITADEL_TARGET,
            CoverLetterDesireSection(
                orgs.CITADEL_TARGET, ApplicationFocus.SEMI_ACADEMIC,
                specific_focus=SpecificApplicationFocus.ASSET_MANAGER
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.SEMI_ACADEMIC,
            combine_files={
                'Nick DeRobertis CV and Cover': [
                    ApplicationComponents.COVER_LETTER,
                    ApplicationComponents.CV,
                ],
            },
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            univs.VILLANOVA_TARGET,
            CoverLetterDesireSection(univs.VILLANOVA_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            univs.U_GEORGIA_TARGET,
            CoverLetterDesireSection(univs.U_GEORGIA_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.REFERENCES,
                ApplicationComponents.RESEARCH_COVER,
                ApplicationComponents.TEACHING_COVER,
                ApplicationComponents.COURSE_OUTLINES,
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Nick DeRobertis Research Portfolio': [
                    ApplicationComponents.RESEARCH_STATEMENT,
                    ApplicationComponents.RESEARCH_COVER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ],
                'Nick DeRobertis Teaching Portfolio': [
                    ApplicationComponents.TEACHING_STATEMENT,
                    ApplicationComponents.TEACHING_COVER,
                    ApplicationComponents.COURSE_OUTLINES,
                    ApplicationComponents.EVALUATIONS
                ]
            }
        ),
        CoverLetter(
            univs.VIRGINIA_TECH_TARGET,
            CoverLetterDesireSection(univs.VIRGINIA_TECH_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.REFERENCES,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            univs.PURDUE_TARGET,
            CoverLetterDesireSection(univs.PURDUE_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.RESEARCH_COVER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Selected Research Work': [
                    ApplicationComponents.RESEARCH_COVER,
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ]
            }
        ),
        CoverLetter(
            univs.U_KANSAS_TARGET,
            CoverLetterDesireSection(univs.U_KANSAS_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.TEACHING_EXPERIENCE_OVERVIEW,
                ApplicationComponents.DIVERSITY,
                ApplicationComponents.RESEARCH_COVER,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.TEACHING_COVER,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.COURSE_OUTLINES,
                ApplicationComponents.RESEARCH_STATEMENT,
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Selected Research Work': [
                    ApplicationComponents.RESEARCH_COVER,
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ],
                'Nick DeRobertis Teaching Portfolio': [
                    ApplicationComponents.TEACHING_STATEMENT,
                    ApplicationComponents.TEACHING_EXPERIENCE_OVERVIEW,
                    ApplicationComponents.TEACHING_COVER,
                    ApplicationComponents.COURSE_OUTLINES,
                    ApplicationComponents.EVALUATIONS
                ]
            },
            output_compression_level=1
        ),
        CoverLetter(
            univs.SINGAPORE_MANAGEMENT_QUANT_TARGET,
            CoverLetterDesireSection(univs.SINGAPORE_MANAGEMENT_QUANT_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.TEACHING_EXPERIENCE_OVERVIEW,
                ApplicationComponents.RESEARCH_COVER,
                ApplicationComponents.TEACHING_COVER,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.COURSE_OUTLINES,
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Selected Research Work': [
                    ApplicationComponents.RESEARCH_COVER,
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ],
                'Nick DeRobertis Teaching Portfolio': [
                    ApplicationComponents.TEACHING_EXPERIENCE_OVERVIEW,
                    ApplicationComponents.TEACHING_COVER,
                    ApplicationComponents.COURSE_OUTLINES,
                    ApplicationComponents.EVALUATIONS
                ]
            },
            output_compression_level=1
        ),
        CoverLetter(
            orgs.MINNEAPOLIS_FED_TARGET,
            CoverLetterDesireSection(
                orgs.MINNEAPOLIS_FED_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.BANKING_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
        ),
        CoverLetter(
            univs.U_CONN_TARGET,
"""
I believe I am an ideal fit at BU as you are looking for an applicant in the area of
FinTech. My job market paper is focused on cryptoassets and I am exploring research ideas in the 
decentralized finance space enabled by blockchain technology. I have applied machine learning and textual 
analysis in my research, and I have deep expertise in programming and 
data science. I hope to further our understanding on how machine learning can be applied in 
empirical finance and economics research, especially around extracting meaning out of 
the predictions made by such models. Beyond my multiple full undergraduate courses, 
I have given numerous informal seminars to fellow
Ph.D students on programming topics such as machine learning and Python for research applications, 
and I am widely viewed in the department as a resource on such topics. I believe the industry is headed 
more towards quantitative finance, machine learning, and big data, and I would be excited about the opportunity 
to teach students these skills. On a personal level, my wife and I enjoy outdoor activities so
Mansfield seems like a good fit.
""",
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.TEACHING_EXPERIENCE_OVERVIEW,
                ApplicationComponents.DIVERSITY,
                ApplicationComponents.RESEARCH_COVER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Teaching Statement and Experience': [
                    ApplicationComponents.TEACHING_STATEMENT,
                    ApplicationComponents.TEACHING_EXPERIENCE_OVERVIEW,
                ],
                'Selected Research Work': [
                    ApplicationComponents.RESEARCH_COVER,
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ],
            },
        ),
        CoverLetter(
            univs.TEXAS_TECH_TARGET,
            CoverLetterDesireSection(univs.TEXAS_TECH_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            orgs.LONGTAIL_ALPHA_TARGET,
            CoverLetterDesireSection(
                orgs.LONGTAIL_ALPHA_TARGET, ApplicationFocus.SEMI_ACADEMIC,
                specific_focus=SpecificApplicationFocus.ASSET_MANAGER
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.SEMI_ACADEMIC,
            font_scale=0.95,
            line_spacing=0.8,
            references_are_being_submitted=False,
        ),
        CoverLetter(
            univs.WARWICK_TARGET,
            CoverLetterDesireSection(univs.WARWICK_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.REFERENCES,
                ApplicationComponents.JMP_VIDEO
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            orgs.JANE_STREET_TARGET,
            CoverLetterDesireSection(
                orgs.JANE_STREET_TARGET, ApplicationFocus.SEMI_ACADEMIC,
                specific_focus=SpecificApplicationFocus.ASSET_MANAGER
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.SEMI_ACADEMIC,
            font_scale=0.95,
            line_spacing=0.8,
            references_are_being_submitted=False,
            by_email=True,
        ),
        CoverLetter(
            univs.IOWA_STATE_TARGET,
            CoverLetterDesireSection(univs.IOWA_STATE_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.REFERENCES,
            ],
            focus=ApplicationFocus.ACADEMIC,
        ),
        CoverLetter(
            orgs.FED_PHILLY_RESEARCH_TARGET,
"""
I believe I am an ideal fit at FRBP as you are looking for a researcher to focus on 
digital currencies. My job market paper is focused on cryptocurrencies, and I am 
currently researching the broader decentralized 
finance space. I believe that central bank digital currencies will be necessary 
to retain control over monetary policy by providing some of the same benefits as 
switching to open cryptocurrencies, and would be interested in research and policy evaluation to 
support this objective. I have deep expertise in programming and 
data science involving large data sets. I also have experience evaluating policy through my research
which analyzes the intended and unintended effects of central bank equity market intervention. I have a strong
interest in regulatory issues in financial markets and am equally comfortable being both self-guided and a team
player providing high-quality results and recommendations. On a personal level, my wife and I have an affinity
for larger cities and we have family close by so Philadelphia seems like a good fit.
"""
            ,
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.JMP_VIDEO,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.9,
            line_spacing=0.8,
        ),
        CoverLetter(
            univs.KINGS_WESTERN_TARGET,
            CoverLetterDesireSection(univs.KINGS_WESTERN_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.TEACHING_STATEMENT,
                ApplicationComponents.TEACHING_EXPERIENCE_OVERVIEW,
                ApplicationComponents.TEACHING_COVER,
                ApplicationComponents.COURSE_OUTLINES,
                ApplicationComponents.EVALUATIONS,
                ApplicationComponents.RESEARCH_COVER,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            by_email=True,
            references_are_being_submitted=False,
        ),
        CoverLetter(
            univs.ST_GALLEN_TARGET,
            CoverLetterDesireSection(univs.ST_GALLEN_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.RESEARCH_LIST,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.RESEARCH_STATEMENT,
                ApplicationComponents.TEACHING_STATEMENT
            ],
            focus=ApplicationFocus.ACADEMIC,
            output_compression_level=1,
            included_references=[AUTHORS[ANDY], AUTHORS[NIMAL]]
        ),
        CoverLetter(
            orgs.PIMCO_TARGET,
            CoverLetterDesireSection(
                orgs.PIMCO_TARGET, ApplicationFocus.SEMI_ACADEMIC,
                specific_focus=SpecificApplicationFocus.ASSET_MANAGER,
                extra_professional_content="""
I would be excited to join either the Portfolio Management Analytics 
or the Client Analytics team as my interests and experience overlap
with both.
                """.strip()
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.SEMI_ACADEMIC,
            font_scale=0.95,
            line_spacing=0.8,
            references_are_being_submitted=False,
        ),
        CoverLetter(
            orgs.FORD_TARGET,
            CoverLetterDesireSection(
                orgs.FORD_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.ECONOMIST,
                extra_content='I am especially excited about the role as I been an automotive enthusiast for 12 years.\n'
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.INDUSTRY,
            font_scale=0.85,
            line_spacing=0.75,
            references_are_being_submitted=False,
        ),
        CoverLetter(
            orgs.ICI_TARGET,
"""
I believe I am an ideal fit at ICI as an Economist given my related research in market microstructure, macroeconomics,
ETFs,
and economic policy as well as technical skills related to developing economic models and communicating insights
from large quantities of data. I also have experience evaluating policy through my research which analyzes the 
intended and unintended effects of
central bank equity market intervention through the purchasing of ETFs.
I am also familiar with regulatory work from both ends: I was an intern in the Credit Risk
department at the Federal Reserve Board of Governors and I worked directly with bank examiners in my role as a
Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses at Eastern Virginia Bankshares.
I have a strong interest in regulatory issues in financial markets and am
equally comfortable being both self-guided and a team player providing high-quality results and recommendations. On
a personal level, my wife and I have an affinity for larger cities and we have family close by so DC seems like a good
fit.
""",
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.9,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.ESSENT_GUARANTY_TARGET,
            CoverLetterDesireSection(
                orgs.ESSENT_GUARANTY_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.ECONOMIST,
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.INDUSTRY,
            font_scale=0.9,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.MITRE_TARGET,
            CoverLetterDesireSection(
                orgs.MITRE_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.ECONOMIST,
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.INDUSTRY,
            font_scale=0.9,
            line_spacing=0.8,
            references_are_being_submitted=False,
        ),
        CoverLetter(
            orgs.OCC_CCRAD_USAJOBS_TARGET,
            [
"""
I believe I am an ideal fit at OCC CCRAD as a Financial Economist given my related research in asset pricing,
market microstructure, 
macroeconomics, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I am familiar with banking supervisory work from both ends: 
I was an intern in the Credit Risk department at the Federal Reserve Board of Governors and 
I worked directly with examiners in my 
role as a Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses and developing 
a stress testing program at 
Eastern Virginia Bankshares. 
I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. I am a U.S. citizen so I look forward to serving my country in this capacity.
On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Northern Virginia so DC would be a 
great location for us.
"""
            ],
            included_components=all_government_components + [ApplicationComponents.RESEARCH_COVER],
            focus=ApplicationFocus.GOVERNMENT,
            cv_modifier_func=orgs.get_occ_ccrad_usajobs_cv_model,
            output_compression_level=1,
            font_scale=0.9,
            line_spacing=0.8,
            combine_files={
                'Selected Research Work': [
                    ApplicationComponents.RESEARCH_COVER,
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ]
            }
        ),
        CoverLetter(
            univs.TSINGHUA_TARGET,
            CoverLetterDesireSection(univs.TSINGHUA_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.RESEARCH_COVER,
                ApplicationComponents.TEACHING_EXPERIENCE_OVERVIEW,
                ApplicationComponents.TEACHING_COVER,
                ApplicationComponents.COURSE_OUTLINES,
                ApplicationComponents.EVALUATIONS
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Nick DeRobertis Selected Research Work': [
                    ApplicationComponents.RESEARCH_COVER,
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ],
                'Nick DeRobertis Teaching Portfolio': [
                    ApplicationComponents.TEACHING_EXPERIENCE_OVERVIEW,
                    ApplicationComponents.TEACHING_COVER,
                    ApplicationComponents.COURSE_OUTLINES,
                    ApplicationComponents.EVALUATIONS
                ]
            },
            by_email=True,
        ),
        CoverLetter(
            univs.NATIONAL_TAIWAN_TARGET,
            CoverLetterDesireSection(univs.NATIONAL_TAIWAN_TARGET, ApplicationFocus.ACADEMIC).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
                ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                ApplicationComponents.OPIN_PAPER,
                ApplicationComponents.RESEARCH_COVER,
            ],
            focus=ApplicationFocus.ACADEMIC,
            combine_files={
                'Nick DeRobertis Selected Research Work': [
                    ApplicationComponents.RESEARCH_COVER,
                    ApplicationComponents.JOB_MARKET_PAPER,
                    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
                    ApplicationComponents.OPIN_PAPER,
                ],
                'Nick DeRobertis CV and Cover': [
                    ApplicationComponents.COVER_LETTER,
                    ApplicationComponents.CV,
                ]
            },
            included_references=[AUTHORS[ANDY], AUTHORS[NIMAL]],
            by_email=True,
            add_organization_name_to_address=False,
        ),
        CoverLetter(
            orgs.BEA_USAJOBS_TARGET,
            CoverLetterDesireSection(
                orgs.BEA_USAJOBS_TARGET, ApplicationFocus.GOVERNMENT,
                specific_focus=SpecificApplicationFocus.OTHER_FINANCIAL_REGULATOR
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.JOB_MARKET_PAPER,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            font_scale=0.95,
            line_spacing=0.8,
            cv_modifier_func=orgs.get_bea_usajobs_cv_model,
        ),
        CoverLetter(
            orgs.OCC_MARKET_RAD_USAJOBS_TARGET,
            [
"""
I believe I am an ideal fit at OCC Market RAD as a Financial Economist given my related research in asset pricing,
market microstructure, 
macroeconomics, and economic policy as well as technical skills related to developing economic models and
communicating insights from large quantities of data. I am familiar with banking supervisory work from both ends: 
I was an intern in the Credit Risk department at the Federal Reserve Board of Governors and 
I worked directly with examiners in my 
role as a Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses and developing 
a stress testing program at 
Eastern Virginia Bankshares. 
I have a strong interest in regulatory issues in financial
markets and am equally comfortable being both self-guided and a team player providing high-quality results and
recommendations. I am a U.S. citizen so I look forward to serving my country in this capacity.
On a personal level, my wife and I both 
have an affinity for larger cities and my family is in Northern Virginia so DC would be a 
great location for us.
"""
            ],
            included_components=[
                ApplicationComponents.CV,
                ApplicationComponents.TRANSCRIPTS,
            ],
            focus=ApplicationFocus.GOVERNMENT,
            cv_modifier_func=orgs.get_occ_market_rad_usajobs_cv_model,
            references_are_being_submitted=False,
            references_were_previously_submitted=True,
            font_scale=0.9,
            line_spacing=0.8,
        ),
        CoverLetter(
            orgs.CARBON_HEALTH_TARGET,
            CoverLetterDesireSection(
                orgs.CARBON_HEALTH_TARGET, ApplicationFocus.INDUSTRY,
                specific_focus=SpecificApplicationFocus.TECH_COMPANY
            ).to_pyexlatex(),
            included_components=[
                ApplicationComponents.CV,
            ],
            focus=ApplicationFocus.INDUSTRY,
            specific_focus=SpecificApplicationFocus.TECH_COMPANY,
            cv_modifier_func=orgs.carbon_health_cv_modifier,
            use_resume=True,
        ),
    ]
