from copy import deepcopy
from typing import Sequence, Dict

import pyexlatex as pl
import pyexlatex.resume as lr

from derobertis_cv.models.organization import Organization, OrganizationCharacteristics
from derobertis_cv.pldata.cover_letters.models import ApplicationTarget, HiringManager, Gender
from derobertis_cv.pldata.cv import CVModel, ResumeSection
from derobertis_cv.pldata.employment_model import JobIDs
from private_cv.contact import get_private_contact_lines

DC_KWARGS = dict(
    location='Washington, DC',
    city='DC',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.FAMILY_CLOSE
    ]
)

PLACEHOLDER_GOV = Organization(
    '(Government Organization name)',
    '(City, state)',
    abbreviation='(Government Organization abbreviation)',
    address_lines=[
        '(Organization division)',
        '(Street address)',
        '(City, state, ZIP)',
    ]
)

PLACEHOLDER_GOV_TARGET = ApplicationTarget(
    PLACEHOLDER_GOV,
    '(Position name)',
)

PLACEHOLDER_INDUSTRY = Organization(
    '(Organization name)',
    '(City, state)',
    abbreviation='(Organization abbreviation)',
    address_lines=[
        '(Street address)',
        '(City, state, ZIP)',
    ]
)

PLACEHOLDER_INDUSTRY_TARGET = ApplicationTarget(
    PLACEHOLDER_INDUSTRY,
    '(Position name)',
)

SEC_DERA = Organization(
    'U.S. Securities and Exchange Commission',
    'Washington, DC',
    abbreviation='DERA',
    address_lines=[
        'Division of Economic and Risk Analysis',
        '100 F Street, NE',
        'Washington, DC 20549',
    ],
    city='DC',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.FAMILY_CLOSE,
        OrganizationCharacteristics.MULTIPLE_LOCATIONS,
    ]
)

WYNETTA_JONES = HiringManager(
    'Jones',
    first_name='Wynetta',
    gender=Gender.FEMALE,
    title='Lead HR Specialist',
)

DERA_COMMITTEE = HiringManager(
    'DERA Hiring Committee',
    is_person=False
)

SEC_DERA_TARGET = ApplicationTarget(
    SEC_DERA,
    'Financial Economic Fellow',
    person=DERA_COMMITTEE
)


def get_dera_cv_model(model: CVModel) -> CVModel:
    def modify_uf_description(desc: Sequence[str]) -> Sequence[str]:
        new_first_point = """
Conduct full economics and finance research projects, including project planning, data collection, analysis, 
and report preparation.
Submit papers on topics such as market microstructure and financial market regulation for publication in peer-reviewed journal articles
        """.strip()
        extra_point = """
Evaluate impacts of economic policies and propose policy ideas, working in research teams and independently
        """.strip()
        new_desc = [
            new_first_point,
            *desc[1:],
            extra_point
        ]
        return new_desc
    model.modify_job_descriptions = {JobIDs.UF_GA: modify_uf_description}
    return model


OFR = Organization(
    'Office of Financial Research',
    'Washington, DC',
    abbreviation='OFR',
    address_lines=[
        'cover letter being sent as email',
    ]
)

OFR_TARGET = ApplicationTarget(
    OFR,
    'Research Economist',
)

RICH_FED = Organization(
    'Federal Reserve Bank of Richmond',
    'Charlotte, NC',
    abbreviation='QSR',
    address_lines=[
        'Quantitative Supervision & Research',
        '530 East Trade Street',
        'Charlotte, NC  28202',
    ]
)

RICH_FED_TARGET = ApplicationTarget(
    RICH_FED,
    'Financial Economist',
)

OCC_MARKET_RAD = Organization(
    'Office of the Comptroller of the Currency',
    'Washington, DC',
    abbreviation='OCC Market RAD',
    address_lines=[
        'Market Risk Analysis Division',
        '400 7th St. SW',
        'Washington, DC  20219'
    ]
)

OCC_MARKET_RAD_TARGET = ApplicationTarget(OCC_MARKET_RAD, 'Financial Economist')
OCC_MARKET_RAD_USAJOBS_TARGET = ApplicationTarget(OCC_MARKET_RAD, 'Financial Economist', custom_app_name='OCC Market RAD USAJOBS')

def get_occ_market_rad_usajobs_cv_model(model: CVModel) -> CVModel:
    def modify_uf_description(desc: Sequence[str]) -> Sequence[str]:
        new_first_point = """
Independently conduct full economics and finance research projects, including planning, information assembly, 
analysis and evaluation, conclusions and report preparation.
Submit papers for publication in peer-reviewed journal articles. Topics include analyses of banking legislation
and regulations, and assessments of significant trends and developments in financial markets
        """.strip()
        extra_begin_point = """
Apply finance, econometrics, economics, mathematics, and statistics theories and methods to develop 
quantitative or statistical models to assess the impact of financial developments on the economy
        """.strip()
        extra_begin_point2 = """
Apply analytical and research techniques including econometrics, mathematical economics, 
and cost-benefit analyses
        """.strip()
        extra_end_point = """
Evaluate impacts of economic policies and propose policy ideas, working in research teams and independently
        """.strip()
        extra_end_point2 = """
Develop analytical tools and publish them as open-source packages
        """.strip()
        extra_end_point3 = """
Develop comprehensive reports reflecting analysis, conclusions, and recommendations, and present 
such findings to faculty and students
        """.strip()
        extra_end_point4 = """
Implement quantitative analyses and data collection/management in Python, SAS, Stata, MATLAB, and R
        """.strip()
        extra_end_point5 = """
Independently develop and teach courses relating to economics subjects including financial markets, modeling, and banking.
Create presentation slides, problem sets, examples, and projects. Present slides and examples 
to students for class instruction in person and virtually. Grade problems sets and projects and provide feedback
to students. Guide selected students through personal research to produce evidence of results.
        """
        extra_end_point6 = """
Utilize economic and financial data sets including CRSP, Compustat, OptionMetrics, OPRA, TAQ, Ravenpack,
Cryptocompare, FRED, IBES, Datastream, EIKON, and Morningstar  
        """.strip()
        new_desc = [
            new_first_point,
            extra_begin_point,
            extra_begin_point2,
            *desc[1:],
            extra_end_point,
            extra_end_point2,
            extra_end_point3,
            extra_end_point4,
            extra_end_point5,
            extra_end_point6,
        ]
        return new_desc

    def modify_evb_description(desc: Sequence[str]) -> Sequence[str]:
        extra_begin_point = """
Conduct bank-specific quantitative analyses relating to financial risks, using quantitative models 
to evaluate the use of capital
        """.strip()
        new_first_point = """
Analyze and model bank commercial credit risk by forecasting credit losses, determining how much capital is required 
to meet regulatory requirements, through rebuilding the Allowance for Loan and Lease Losses (ALLL) models, 
ultimately saving \$5.4 million for the bank
        """.strip()
        new_second_point = """
Developed credit risk metrics such as probability of default (PD) and loss given default (LGD) for 
over 10,000 commercial
and consumer loans by internal risk grade, delinquency status, and FFIEC code using migration analysis
        """.strip()
        new_third_point = """
Evaluate operational and model risk by developing a stress testing framework
        """.strip()
        extra_end_point = """
Analyze the conditions of the banking industry to understand competitors' capitalization relating 
to regulatory requirements
        """.strip()
        extra_end_point2 = """
Provide advice and keep management informed about issues relating to bank capitalization 
via comprehensive reports, narratives, and briefings reflecting analysis, 
conclusions, and recommendations
        """.strip()
        new_desc = [
            extra_begin_point,
            new_first_point,
            new_second_point,
            new_third_point,
            extra_end_point,
            extra_end_point2,
        ]
        return new_desc

    def modify_fed_description(desc: Sequence[str]) -> Sequence[str]:
        extra_begin_point = """
Support projects that respond to requests by senior management for materials
on a variety of topics including policy and management issues confronting the Fed,
analyses of banking legislation and regulations, and assessments of 
significant trends and developments in the banking industry
        """.strip()
        new_begin_point = """
Analyzed the market of banking institutions to understand their assessments of risk, 
to prepare reports and briefings and develop a standardized risk scale
        """.strip()
        new_end_point = """
Contribute to the collection, analysis, and interpretation of Shared National Credit (SNC) 
data, to respond to inquiries that affect the banking system and financial markets
        """
        return [
            extra_begin_point,
            new_begin_point,
            new_end_point
        ]

    model.modify_job_descriptions = {
        JobIDs.UF_GA: modify_uf_description,
        JobIDs.EVB_PORTFOLIO_ANALYST: modify_evb_description,
        JobIDs.FRB_INTERN: modify_fed_description,
    }

    app_info: Dict[str, str] = {
        'Job Announcement Number': 'DH-HQ-TL-20-2212',
        'Job Title': 'Financial Economist',
        'Grade Level(s)': 'NB V2',
        'Location(s)': 'Washington, DC',
        'Full Legal Name': 'Nicholas Andrew DeRobertis',
        'US Citizen': 'Yes'
    }
    model.application_info = app_info

    model.include_hours_per_week = True

    model.font_scale = 0.85
    model.line_spacing = 0.85

    model.sections.insert(6, ResumeSection.CONTINUED)
    model.sections.insert(5, ResumeSection.CONTINUED)

    return model

OCC_CCRAD = Organization(
    'Office of the Comptroller of the Currency',
    'Washington, DC',
    abbreviation='OCC CCRAD',
    address_lines=[
        'Commercial Credit Risk Analysis Division',
        '400 7th St. SW',
        'Washington, DC  20219'
    ]
)

OCC_CCRAD_TARGET = ApplicationTarget(OCC_CCRAD, 'Financial Economist')
OCC_CCRAD_USAJOBS_TARGET = ApplicationTarget(OCC_CCRAD, 'Financial Economist', custom_app_name='OCC CCRAD USAJOBS')

def get_occ_ccrad_usajobs_cv_model(model: CVModel) -> CVModel:
    def modify_uf_description(desc: Sequence[str]) -> Sequence[str]:
        new_first_point = """
Conduct full economics and finance research projects, including project development, data collection, and analysis.
Submit papers for publication in peer-reviewed journal articles
        """.strip()
        extra_begin_point = """
Apply finance, econometrics, and statistics theories and methods to develop statistical models based on economic theory
        """.strip()
        extra_end_point = """
Evaluate impacts of economic policies and propose policy ideas, working in research teams and independently
        """.strip()
        new_desc = [
            new_first_point,
            extra_begin_point,
            *desc[1:],
            extra_end_point
        ]
        return new_desc

    def modify_evb_description(desc: Sequence[str]) -> Sequence[str]:
        new_first_point = """
Analyze and model bank commercial credit risk by forecasting credit losses, determining how much capital is required 
to meet regulatory requirements, through rebuilding the Allowance for Loan and Lease Losses (ALLL) models, 
ultimately saving \$5.4 million for the bank
        """.strip()
        new_second_point = """
Developed credit risk metrics such as probability of default (PD) and loss given default (LGD) for 
over 10,000 commercial
and consumer loans by internal risk grade, delinquency status, and FFIEC code using migration analysis
        """.strip()
        new_third_point = """
Evaluate operational and model risk by developing a stress testing framework
        """.strip()
        new_desc = [
            new_first_point,
            new_second_point,
            new_third_point
        ]
        return new_desc
    model.modify_job_descriptions = {
        JobIDs.UF_GA: modify_uf_description,
        JobIDs.EVB_PORTFOLIO_ANALYST: modify_evb_description,
    }

    app_info: Dict[str, str] = {
        'Job Announcement Number': 'DH-HQ-TL-21-2310',
        'Job Title': 'Financial Economist, NB-0110-V.2',
        'Grade Level(s)': 'NB V2',
        'Location(s)': 'Washington, DC',
        'Full Legal Name': 'Nicholas Andrew DeRobertis',
        'US Citizen': 'Yes'
    }
    model.application_info = app_info

    model.include_hours_per_week = True

    model.font_scale = 0.85
    model.line_spacing = 0.85

    return model

SEC_OIAD = Organization(
    'U.S. Securities and Exchange Commission',
    'Washington, DC',
    abbreviation='OIAD',
    address_lines=[
        'Office of the Investor Advocate',
        '100 F Street, NE',
        'Washington, DC 20549',
    ]
)

SEC_OIAD_TARGET = ApplicationTarget(SEC_OIAD, 'Financial Economist')

NY_FED = Organization(
    'Federal Reserve Bank of New York',
    'New York, NY',
    abbreviation='FRBNY',
    address_lines=[
        '33 Liberty Street',
        'New York, NY  10045',
    ]
)

NY_FED_TARGET = ApplicationTarget(
    NY_FED,
    'PhD Economist',
)


WORLD_BANK_DRG = Organization(
    'World Bank',
    'Washington, D.C.',
    abbreviation='DRG',
    address_lines=[
        'Development Research Group'
    ]
)

WORLD_BANK_DRG_HIRING = HiringManager(
    'DRG Hiring Committee',
    is_person=False
)

WORLD_BANK_DRG_TARGET = ApplicationTarget(WORLD_BANK_DRG, 'Researcher', person=WORLD_BANK_DRG_HIRING)

FED_BOARD = Organization(
    'Federal Reserve Board of Governors',
    'Washington, D.C.',
    abbreviation='the Board',
    address_lines=[
        '1850 K Street, NW',
        'Washington, D.C.  20006'
    ]
)

FED_BOARD_HIRING = HiringManager('Federal Reserve Board Hiring Committee', is_person=False)

FED_BOARD_TARGET = ApplicationTarget(FED_BOARD, 'Financial Economist', person=FED_BOARD_HIRING)

NORGES_BANK = Organization(
    'Norges Bank',
    'Oslo, Norway',
    abbreviation='Norges Bank',
    address_lines=[
        'Research Department',
        'Bankplassen 2',
        'Oslo, 0151',
        'Norway'
    ],
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.LARGE_CITY,
    ],
    city='Oslo',
    country='Norway',
)

NORGES_HIRING = HiringManager('Research Department Search Committee', is_person=False)
NORGES_TARGET = ApplicationTarget(NORGES_BANK, 'Research Economist', person=NORGES_HIRING)

FED_DALLAS = Organization(
    'Federal Reserve Bank of Dallas',
    'Dallas, TX',
    abbreviation='the Dallas Fed',
    address_lines=[
        'Research Department',
        '2200 North Pearl Street',
        'Dallas, TX,  75201'
    ],
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.WARM_WEATHER,
    ],
    city='Dallas'
)

FED_DALLAS_HIRING = HiringManager('Research Department Search Committee', is_person=False)
FED_DALLAS_TARGET = ApplicationTarget(FED_DALLAS, 'Economist', person=FED_DALLAS_HIRING)

CFPB = Organization(
    'Consumer Financial Protection Bureau',
    'Washington, DC',
    abbreviation='CFPB',
    address_lines=[
        'Office of Research',
        'Research, Markets, & Regulations',
        '1700 G St. NW',
        'Washington, DC  20552'
    ],
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.FAMILY_CLOSE,
    ],
    city='DC'
)
CFPB_TARGET = ApplicationTarget(CFPB, 'Economist')


def get_cfpb_cv_model(model: CVModel) -> CVModel:
    def modify_uf_description(desc: Sequence[str]) -> Sequence[str]:
        new_first_point = """
Conduct full economics and finance research projects, including project development, data collection, and analysis.
Submit papers for publication in peer-reviewed journal articles
        """.strip()
        extra_point = """
Evaluate impacts of economic policies and propose policy ideas, working in research teams and independently
        """.strip()
        new_desc = [
            new_first_point,
            *desc[1:],
            extra_point
        ]
        return new_desc
    model.modify_job_descriptions = {JobIDs.UF_GA: modify_uf_description}

    app_info: Dict[str, str] = {
        'Job Announcement Number': '21-CFPB-38-DH',
        'Job Title': 'Economist',
        'Grade Level(s)': 'CN-52, CN-53, CN-60',
        'Location(s)': 'Washington, DC',
        'Full Legal Name': 'Nicholas Andrew DeRobertis',
        'US Citizen': 'Yes'
    }
    model.application_info = app_info

    model.font_scale = 0.9
    model.line_spacing = 0.9

    return model

BIS = Organization(
    'Bank for International Settlements',
    'Basel, Switzerland',
    abbreviation='BIS',
    address_lines=[
        'Centralbahnpl. 2',
        '4002 Basel',
        'Switzerland'
    ],
    city='Basel',
    country='Switzerland',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)
BIS_TARGET = ApplicationTarget(BIS, 'Economist')

FED_SF = Organization(
    'Federal Reserve Bank of San Francisco',
    'San Francisco, CA',
    abbreviation='FRBSF',
    address_lines=[
        'Research Department',
        '101 Market St.',
        'San Francisco, CA  94105'
    ],
    city='San Francisco',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.WEST_COAST,
        OrganizationCharacteristics.WARM_WEATHER,
    ]
)
FED_SF_TARGET = ApplicationTarget(FED_SF, 'Economist')

FED_ATLANTA = Organization(
    'Federal Reserve Bank of Atlanta',
    'Atlanta, GA',
    abbreviation='the Atlanta Fed',
    address_lines=[
        'Research Department',
        '1000 Peachtree Street, NE',
        'Atlanta, GA  30309-4470'
    ],
    city='Atlanta',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.WARM_WEATHER
    ]
)
FED_ATLANTA_HIRING = HiringManager('Research Department Search Committee', is_person=False)
FED_ATLANTA_TARGET = ApplicationTarget(FED_ATLANTA, 'Financial Economist', person=FED_ATLANTA_HIRING)

UBER = Organization(
    'Uber',
    'San Francisco, CA',
    abbreviation='Uber',
    address_lines=[
        '1455 Market St #400',
        'San Francisco, CA  94103',
    ],
    city='San Francisco',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.WEST_COAST,
        OrganizationCharacteristics.WARM_WEATHER
    ]
)
UBER_TARGET = ApplicationTarget(UBER, 'Economist')


MICROSOFT = Organization(
    'Microsoft',
    'Redmond, WA',
    abbreviation='Microsoft',
    address_lines=[
        'Office of the Chief Economist',
        '14820 NE 36th St.',
        'Redmond, WA  98052'
    ],
    city='Redmond/Seattle',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.WEST_COAST,
    ]
)
MICROSOFT_ECONOMIST_TARGET = ApplicationTarget(MICROSOFT, 'Research Economist')

BARCLAYS = Organization(
    'Barclays',
    'New York, NY',
    abbreviation='Barclays',
    address_lines=[
        'Quantitative Portfolio Strategy Group',
        '745 7th Ave.',
        'New York, NY  10019'
    ],
    city='New York',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
    ]
)

BARCLAYS_TARGET = ApplicationTarget(BARCLAYS, 'Quantitative Cross-Asset Analyst')

UPSTART = Organization(
    'Upstart',
    'San Mateo, CA',
    abbreviation='Upstart',
    address_lines=[
        '2950 S Delaware St #300',
        'San Mateo, CA  94403'
    ],
    city='San Mateo',
    characteristics=[
        OrganizationCharacteristics.WEST_COAST,
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.MID_SIZE_CITY,
    ]
)
UPSTART_TARGET = ApplicationTarget(UPSTART, 'Research Scientist')

TREASURY_OMA = Organization(
    'Department of the Treasury',
    'Washington, DC',
    abbreviation='OMA',
    address_lines=[
        'Office of Economic Policy',
        'Office of Microeconomic Analysis',
        '1500 Pennsylvania Ave., N.W.',
        'Washington, D.C.  20220'
    ],
    city='DC',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.FAMILY_CLOSE,
    ]
)
TREASURY_OMA_TARGET = ApplicationTarget(TREASURY_OMA, 'Economist')


def get_treasury_oma_cv_model(model: CVModel) -> CVModel:
    def modify_uf_description(desc: Sequence[str]) -> Sequence[str]:
        new_first_point = """
Conduct full economic research projects, including project development, data collection, and analysis.
Submit papers for publication in peer-reviewed journal articles
        """.strip()
        extra_point = """
Evaluate impacts of economic policies and propose policy ideas, working in research teams
        """.strip()
        new_desc = [
            new_first_point,
            *desc[1:],
            extra_point
        ]
        return new_desc
    model.modify_job_descriptions = {JobIDs.UF_GA: modify_uf_description}

    app_info: Dict[str, str] = {
        'Job Announcement Number': '20-DO-689-DH',
        'Job Title': 'Economist',
        'Grade Level(s)': 'GS-12, GS-13, GS-14',
        'Location(s)': 'Washington, DC',
        'Full Legal Name': 'Nicholas Andrew DeRobertis',
        'US Citizen': 'Yes'
    }
    model.application_info = app_info

    model.font_scale = 0.9
    model.line_spacing = 0.9

    return model

FED_PHILLY = Organization(
    'Federal Reserve Bank of Philadelphia',
    'Philadelphia, PA',
    abbreviation='FRBP',
    address_lines=[
        '10 Independence Mall',
        'Philadelphia, PA,  19106'
    ],
    city='Philadelphia',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.FAMILY_CLOSE,
    ]
)
FED_PHILLY_ML_TARGET = ApplicationTarget(FED_PHILLY, 'Machine Learning Economist')

FDIC_CFR = Organization(
    'Federal Deposit Insurance Corporation',
    'Washington, DC',
    abbreviation='CFR',
    address_lines=[
        'Center for Financial Research',
        '550 17th St NW',
        'Washington, DC  20429'
    ],
    city='DC',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.FAMILY_CLOSE,
    ]
)
FDIC_CFR_TARGET = ApplicationTarget(FDIC_CFR, 'Financial Economist')

GAO = Organization(
    'Government Accountability Office',
    'Washington, DC',
    abbreviation='GAO',
    address_lines=[
        '441 G St., NW',
        'Washington, DC  20548'
    ],
    city='DC',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.FAMILY_CLOSE,
    ]
)
GAO_TARGET = ApplicationTarget(GAO, 'Senior Economist')

FED_CHICAGO = Organization(
    'Federal Reserve Bank of Chicago',
    'Chicago, IL',
    abbreviation='the Chicago Fed',
    address_lines=[
        'Economic Research Department',
        '230 S LaSalle St',
        'Chicago, IL  60604'
    ],
    city='Chicago',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
    ]
)
FED_CHICAGO_PERSON = HiringManager('ERD Search Committee', is_person=False)
FED_CHICAGO_TARGET = ApplicationTarget(FED_CHICAGO, 'Economist', person=FED_CHICAGO_PERSON)

FED_KANSAS = Organization(
    'Federal Reserve Bank of Kansas City',
    'Kansas City, MO',
    abbreviation='FRBKC',
    address_lines=[
        'Economic Research Department',
        '1 Memorial Dr',
        'Kansas City, MO  64198'
    ],
    city='Kansas City',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
    ]
)
FED_KANSAS_TARGET = ApplicationTarget(FED_KANSAS, 'Senior Economist')

BEA = Organization(
    'U.S. Bureau of Economic Analysis',
    'Suitland, MD',
    abbreviation='BEA',
    address_lines=[
        'National Accounts Research Group',
        '4600 Silver Hill Rd.',
        'Suitland, MD  20746'
    ],
    city='DC',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.FAMILY_CLOSE,
    ]
)
BEA_HM = HiringManager('NARG Search Committee', is_person=False)
BEA_TARGET = ApplicationTarget(BEA, 'Research Economist', person=BEA_HM)
BEA_USAJOBS_TARGET = ApplicationTarget(BEA, 'Research Economist', custom_app_name='BEA USAJOBS', person=BEA_HM)


def get_bea_usajobs_cv_model(model: CVModel) -> CVModel:
    def modify_uf_description(desc: Sequence[str]) -> Sequence[str]:
        new_first_point = """
Conduct full economics and finance research projects, including project development, information assembly 
and data collection from 
multiple sources, and analysis.
Prepare reports including statistical tables and submit papers for publication 
in peer-reviewed journal articles to communicate economic findings
        """.strip()
        extra_begin_point = """
Apply finance, econometrics, and statistics theories and methods to develop statistical models based on economic theory, 
and apply such techniques to manipulate and analyze data
        """.strip()
        extra_end_point = """
Evaluate impacts of economic policies and propose policy ideas for officials, 
working in teams of professional economists and independently
        """.strip()
        second_extra_end_point = """
Communicate economic concepts at various levels including to undergraduate students, graduate students, 
professors, and professional economists 
        """.strip()
        third_extra_end_point = """
Manage multiple simultaneous research tasks, involving economic measurement, identifying and locating data which 
is relevant to the current task, analysis and preparation of statistical tables, and presentation of 
findings in written research papers as well as oral presentations
        """.strip()
        new_desc = [
            new_first_point,
            extra_begin_point,
            *desc[1:],
            extra_end_point,
            second_extra_end_point,
            third_extra_end_point,
        ]
        return new_desc

    def modify_evb_description(desc: Sequence[str]) -> Sequence[str]:
        new_first_point = """
Analyze and model bank commercial credit risk by forecasting credit losses, determining how much capital is required 
to meet regulatory requirements, through rebuilding the Allowance for Loan and Lease Losses (ALLL) models, 
ultimately saving \$5.4 million for the bank
        """.strip()
        new_second_point = """
Developed credit risk metrics such as probability of default (PD) and loss given default (LGD) for 
over 10,000 commercial
and consumer loans by internal risk grade, delinquency status, and FFIEC code using migration analysis
        """.strip()
        new_third_point = """
Evaluate operational and model risk by developing a stress testing framework
        """.strip()
        new_desc = [
            new_first_point,
            new_second_point,
            new_third_point
        ]
        return new_desc
    model.modify_job_descriptions = {
        JobIDs.UF_GA: modify_uf_description,
        JobIDs.EVB_PORTFOLIO_ANALYST: modify_evb_description,
    }

    app_info: Dict[str, str] = {
        'Job Announcement Number': 'BEA-ADNEA-2021-0003',
        'Job Title': 'Economist (Research), ZP-0110-III/IV, BEA-DHA-VFP',
        'Grade Level(s)': 'ZP 03 - 04',
        'Location(s)': 'Suitland, MD',
        'Full Legal Name': 'Nicholas Andrew DeRobertis',
        'US Citizen': 'Yes',
        'Registered with Selective Service System': 'Yes'
    }
    model.application_info = app_info

    model.include_hours_per_week = True

    model.font_scale = 0.85
    model.line_spacing = 0.85

    sects = deepcopy(model.sections)
    sects[4] = pl.PageBreak()
    sects.insert(4, ResumeSection.CONTINUED)
    model.sections = sects

    return model


JCT = Organization(
    'Joint Committee on Taxation',
    abbreviation='JCT',
    address_lines=[
        '502 Ford House Office Building',
        'Washington, DC.  20515'
    ],
    **DC_KWARGS  # type: ignore
)
JCT_TARGET = ApplicationTarget(JCT, 'Quantitative Economist')

GS_GMR = Organization(
    'Goldman Sachs',
    'New York, NY',
    abbreviation='GMR',
    address_lines=[
        'Global Investment Research',
        'Macro Research',
        '200 West St',
        'New York, NY  10282'
    ],
    city='NYC',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY
    ]
)
GS_GMR_TARGET = ApplicationTarget(GS_GMR, 'Macro Research Associate')

AIR_LIQUIDE = Organization(
    'Air Liquide',
    'Newark, DE',
    abbreviation='Air Liquide',
    address_lines=[
        'Research & Development',
        'Computational & Data Science',
        '200 Gbc Dr.',
        'Newark, DE  19702'
    ],
    city='Newark',
    characteristics=[
        OrganizationCharacteristics.SMALL_TOWN,
        OrganizationCharacteristics.FAMILY_CLOSE,
    ]
)
AIR_LIQUIDE_HM = HiringManager('R&D Data Science Hiring Committee', is_person=False)
AIR_LIQUIDE_TARGET = ApplicationTarget(AIR_LIQUIDE, 'Data Scientist/Economist', person=AIR_LIQUIDE_HM)

AFINITI = Organization(
    'Afiniti',
    abbreviation='Afiniti',
    address_lines=[
        'AI R&D',
        '1701 Pennsylvania Avenue NW #600',
        'Washington, DC 20006',
    ],
    **DC_KWARGS  # type: ignore
)
AFINITI_TARGET = ApplicationTarget(AFINITI, 'Research Scientist')

FUTUREPROOF = Organization(
    'FutureProof Technologies',
    'San Diego, CA',
    abbreviation='FutureProof',
    address_lines=[
        ''
    ],
    city='San Diego',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.WEST_COAST,
        OrganizationCharacteristics.REMOTE,
    ]
)
FUTUREPROOF_TARGET = ApplicationTarget(FUTUREPROOF, 'PhD Economist')

NOVI = Organization(
    'Novi',
    'Menlo Park, CA',
    abbreviation='Novi',
    address_lines=[
        '1 Hacker Way',
        'Menlo Park, CA  94025'
    ],
    city='the Bay Area',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.WEST_COAST,
    ]
)
NOVI_TARGET = ApplicationTarget(NOVI, 'Research Scientist')

UBER_FREIGHT = Organization(
    'Uber Freight',
    'San Francisco, CA',
    abbreviation='Uber Freight',
    address_lines=[
        '1455 Market St #400',
        'San Francisco, CA  94103',
    ],
    city='San Francisco',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.WEST_COAST,
    ]
)
UBER_FREIGHT_TARGET = ApplicationTarget(UBER_FREIGHT, 'Staff Economist')

FACEBOOK = Organization(
    'Facebook',
    'Menlo Park, CA',
    abbreviation='Facebook',
    address_lines=[
        '1 Hacker Way',
        'Menlo Park, CA  94025'
    ],
    city='the Bay Area',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.WEST_COAST,
    ]
)
FACEBOOK_TARGET = ApplicationTarget(FACEBOOK, 'Economist')

OLIVER_WYMAN = Organization(
    'Oliver Wyman',
    'Raleigh, NC',
    abbreviation='Oliver Wyman',
    address_lines=[
        'Financial Services Quantitative Analytics Group',
        '2301 Sugar Bush Road',
        'Raleigh, NC 27612'
    ],
    city='Raleigh',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
    ]
)
OLIVER_WYMAN_HM = HiringManager('FSQA Hiring Committee', is_person=False)
OLIVER_WYMAN_TARGET = ApplicationTarget(OLIVER_WYMAN, 'Analyst', person=OLIVER_WYMAN_HM)

CAPITAL_ONE = Organization(
    'Capital One',
    'McLean, VA',
    abbreviation='Capital One',
    address_lines=[
        'Credit Risk Management Modeling',
        '1680 Capital One Drive',
        'McLean, VA 22102-3491'
    ],
    city='McLean',
    characteristics=[
        OrganizationCharacteristics.NOVA,
        OrganizationCharacteristics.FAMILY_CLOSE,
    ]
)
CAPITAL_ONE_HM = HiringManager('CRMM Hiring Committee', is_person=False)
CAPITAL_ONE_TARGET = ApplicationTarget(CAPITAL_ONE, 'Principal Quantitative Modeler', person=CAPITAL_ONE_HM)

JACOBS_LEVY = Organization(
    'Jacobs Levy Capital Management',
    'Florham Park, NJ',
    abbreviation='Jacobs Levy',
    address_lines=[
        '100 Campus Dr',
        'Florham Park, NJ 07932'
    ],
    city='Florham Park',
    characteristics=[
        OrganizationCharacteristics.SUBURBAN,
    ]
)
JACOBS_LEVY_TARGET = ApplicationTarget(JACOBS_LEVY, 'Senior Quantitative Equity Researcher')

GEODE_CAPITAL = Organization(
    'Geode Capital Management',
    'Boston, MA',
    abbreviation='Geode',
    address_lines=[
        'Quantitative Research Team',
        '100 Summer St. 12th Floor',
        'Boston, MA  02110',
    ],
    city='Boston',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.FAMILY_CLOSE,
    ]
)
GEODE_CAPITAL_TARGET = ApplicationTarget(GEODE_CAPITAL, 'Quantitative Associate Analyst')

FED_BOSTON = Organization(
    'Federal Reserve Bank of Boston',
    'Boston, MA',
    abbreviation='the Boston Fed',
    address_lines=[
        'Research Department',
        '600 Atlantic Ave',
        'Boston, MA 02210'
    ],
    city='Boston',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.FAMILY_CLOSE,
    ]
)
FED_BOSTON_PERSON = HiringManager('Research Department Hiring Committee', is_person=False)
FED_BOSTON_TARGET = ApplicationTarget(FED_BOSTON, 'Financial Economist', person=FED_BOSTON_PERSON)

VANGUARD_QEG = Organization(
    'Vanguard',
    'Malvern, PA',
    abbreviation='Vanguard',
    address_lines=[
        'Quantitative Equity Group',
        '100 Vanguard Blvd',
        'Malvern, PA 19355'
    ],
    city='Malvern',
    characteristics=[
        OrganizationCharacteristics.FAMILY_CLOSE,
        OrganizationCharacteristics.SUBURBAN,
    ]
)
VANGUARD_QEG_TARGET = ApplicationTarget(VANGUARD_QEG, 'Quantitative Analyst')

FHFA_DBR = Organization(
    'Federal Housing Finance Agency',
    abbreviation='FHFA DBR',
    address_lines=[
        'Division of FHLBank Regulation',
        '400 7th St SW',
        'Washington, DC 20024'
    ],
    **DC_KWARGS  # type: ignore
)
FHFA_DBR_TARGET = ApplicationTarget(FHFA_DBR, 'Economist')

STEVENS_CAPITAL = Organization(
    'Stevens Capital Management LP',
    'Radnor, PA',
    abbreviation='Stevens Capital',
    address_lines=[
        '201 King of Prussia Rd',
        'Wayne, PA 19087'
    ],
    city='Radnor',
    characteristics=[
        OrganizationCharacteristics.FAMILY_CLOSE,
        OrganizationCharacteristics.SUBURBAN,
    ]
)
STEVENS_CAPITAL_TARGET = ApplicationTarget(STEVENS_CAPITAL, 'Quantitative Research Analyst')

FED_PHILLY_RADAR = deepcopy(FED_PHILLY)
FED_PHILLY_RADAR.address_lines.insert(0, 'Supervision, Regulation, and Credit Department')  # type: ignore
FED_PHILLY_RADAR.address_lines.insert(0, 'Risk Assessment, Data Analysis, and Research')  # type: ignore
FED_PHILLY_RADAR_TARGET = ApplicationTarget(FED_PHILLY_RADAR, 'Financial Economist', custom_app_name='FRBP RADAR')


FORD = Organization(
    'Ford Motor Company',
    'Dearborn, MI',
    abbreviation='Ford',
    address_lines=[
        'Global Data Insight and Analytics',
        '1 American Road',
        'Dearborn, MI  48126',
    ],
    city='Detroit',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
    ]
)
FORD_TARGET = ApplicationTarget(FORD, 'Economist')

CITADEL = Organization(
    'Citadel',
    'Chicago, IL',
    abbreviation='Citadel',
    address_lines=[
        '131 South Dearborn Street',
        'Chicago, IL 60603',
    ],
    city='Chicago',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
    ]
)
CITADEL_TARGET = ApplicationTarget(CITADEL, 'Quantitative Researcher')

MINNEAPOLIS_FED = Organization(
    'Federal Reserve Bank of Minneapolis',
    'Minneapolis, MN',
    abbreviation='FRBM',
    address_lines=[
        '90 Hennepin Ave.',
        'Minneapolis, MN  55401',
    ],
    city='Minneapolis',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
    ]
)
MINNEAPOLIS_FED_TARGET = ApplicationTarget(MINNEAPOLIS_FED, 'Research Economist')

LONGTAIL_ALPHA = Organization(
    'LongTail Alpha',
    'Newport Beach, CA',
    abbreviation='LongTail',
    address_lines=[
        '500 Newport Center Dr.',
        'Newport Beach, CA  92660'
    ],
    city='Newport Beach',
    characteristics=[
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.WEST_COAST,
        OrganizationCharacteristics.MID_SIZE_CITY,
    ]
)
LONGTAIL_ALPHA_TARGET = ApplicationTarget(LONGTAIL_ALPHA, 'Quantitative Researcher')


JANE_STREET = Organization(
    'Jane Street',
    'New York, NY',
    abbreviation='Jane Street',
    address_lines=[
        '250 Vesey Street',
        'New York, NY  10281',
    ],
    city='New York',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.FAMILY_CLOSE,
    ]
)
JANE_STREET_TARGET = ApplicationTarget(JANE_STREET, 'Quantitative Researcher')

FED_PHILLY_RESEARCH = deepcopy(FED_PHILLY)
FED_PHILLY_RESEARCH.address_lines.insert(0, 'Research Department')  # type: ignore
FED_PHILLY_RESEARCH.address_lines.insert(0, 'Risk Assessment, Data Analysis, and Research')  # type: ignore
FED_PHILLY_RESEARCH_TARGET = ApplicationTarget(FED_PHILLY_RESEARCH, 'Research Economist', custom_app_name='FRBP Research')

PIMCO = Organization(
    'PIMCO',
    'Newport Beach, CA',
    abbreviation='PIMCO',
    address_lines=[
        '650 Newport Center Dr.',
        'Newport Beach, CA  92660',
    ],
    city='Newport Beach',
    characteristics=[
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.WEST_COAST,
        OrganizationCharacteristics.MID_SIZE_CITY,
    ],
)
PIMCO_TARGET = ApplicationTarget(PIMCO, 'Quantitative Research Analyst')

ICI = Organization(
    'Investment Company Institute',
    abbreviation='ICI',
    address_lines=[
        '1401 H St NW',
        'Washington, DC 20005',
    ],
    **DC_KWARGS  # type: ignore
)
ICI_TARGET = ApplicationTarget(ICI, 'Economist')

ESSENT_GUARANTY = Organization(
    'Essent Guaranty',
    'Philadelphia, PA',
    abbreviation='Essent',
    address_lines=[
        'Two Radnor Corporate Center',
        'Matsonford Rd.',
        'Radnor, PA  19087',
    ],
    city='Philadelphia',
    characteristics=[
        OrganizationCharacteristics.FAMILY_CLOSE,
        OrganizationCharacteristics.LARGE_CITY,
    ]
)
ESSENT_GUARANTY_TARGET = ApplicationTarget(ESSENT_GUARANTY, 'Director of Modeling')

MITRE = Organization(
    'MITRE Corporation',
    'McLean, VA',
    abbreviation='MITRE',
    address_lines=[
        '7525 Colshire Dr.',
        'McLean, VA  22102'
    ],
    city='McLean',
    characteristics=[
        OrganizationCharacteristics.FAMILY_CLOSE,
        OrganizationCharacteristics.SUBURBAN,
    ]
)
MITRE_TARGET = ApplicationTarget(MITRE, 'Senior Economist')


CARBON_HEALTH = Organization(
    'Carbon Health',
    'San Francisco, CA',
    abbreviation='Carbon Health',
    address_lines=[
        '55 Pacific Ave',
        'San Francisco, CA 94111'
    ],
    city='San Francisco',
    characteristics=[
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.WEST_COAST,
        OrganizationCharacteristics.LARGE_CITY,
    ]
)
CARBON_HEALTH_TARGET = ApplicationTarget(CARBON_HEALTH, 'Lead Engineer')


def carbon_health_cv_modifier(model: CVModel) -> CVModel:
    model.overview_text = """
    An entrepreneur, full-stack web engineer and architect, PhD empirical researcher,
    data scientist, and project manager with a track record of building, deploying, 
    and managing open- and closed-source applications and research projects.
    """
    model.custom_contact_lines_func = get_private_contact_lines
    return model
