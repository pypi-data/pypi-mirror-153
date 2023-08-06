from copy import deepcopy
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from derobertis_cv.pldata.cv import CVModel

from derobertis_cv.models.organization import OrganizationCharacteristics
from derobertis_cv.models.university import UniversityModel
from derobertis_cv.pldata.constants.institutions import UF_NAME, VCU_NAME
from derobertis_cv.pldata.cover_letters.models import HiringManager, ApplicationTarget, Gender
from derobertis_cv.pldata.interests import RESEARCH_INTERESTS
from derobertis_cv.pltemplates.logo import image_base64

AP = 'Assistant Professor'

UF = UniversityModel(UF_NAME, 'Gainesville, FL', abbreviation='UF', logo_base64=image_base64('uf-logo.png'))
VCU = UniversityModel(VCU_NAME, 'Richmond, VA', abbreviation='VCU', logo_base64=image_base64('vcu-logo.png'))

HONG_KONG_KWARGS = dict(
    location='Hong Kong, Hong Kong',
    city='Hong Kong',
    country='Hong Kong',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.WARM_WEATHER,
    ]
)

PLACEHOLDER_UNIVERSITY = UniversityModel(
    '(School name)',
    '(City, state)',
    abbreviation='(School abbreviation)',
    address_lines=[
        '(Department name)',
        '(Street address)',
        '(City, state, ZIP)',
    ]
)

PLACEHOLDER_UNIVERSITY_TARGET = ApplicationTarget(
    PLACEHOLDER_UNIVERSITY,
    AP,
)

EL_PASO = UniversityModel(
    'University of Texas at El Paso',
    'El Paso, TX',
    abbreviation='UTEP',
    address_lines=[
        'Economics and Finance',
        'Business Room 236',
        '500 West University Avenue',
        'El Paso, TX  79968'
    ]
)

EL_PASO_TARGET = ApplicationTarget(
    EL_PASO,
    AP,
)

DRAKE = UniversityModel(
    'Drake University College of Business & Public Administration',
    'Des Moines, IA',
    abbreviation='DU',
    address_lines=[
        'Finance Department',
        'Aliber Hall',
        '2507 University Ave',
        'Des Moines, IA 50311',
    ]
)

DRAKE_TARGET = ApplicationTarget(
    DRAKE,
    AP,
)

MONASH = UniversityModel(
    'Monash University',
    'Melbourne, Victoria, Australia',
    abbreviation='MU',
    address_lines=[
        'Monash Business School',
        '900 Dandenong Road',
        'Caulfield East',
        'Victoria 3145',
        'Australia'
    ]
)

MONASH_HIRING_MANAGER = HiringManager(
    'Banking and Finance Recruitment Team',
    is_person=False
)

MONASH_TARGET = ApplicationTarget(
    MONASH,
    AP,
    person=MONASH_HIRING_MANAGER,
)

OREGON_STATE = UniversityModel(
    'Oregon State University',
    'Corvallis, OR',
    abbreviation='OSU',
    address_lines=[
        'College of Business',
        '2751 SW Jefferson Way',
        'Corvallis, OR  97331'
    ]
)

OREGON_STATE_TARGET = ApplicationTarget(
    OREGON_STATE,
    AP,
)

FIU = UniversityModel(
    'Florida International University',
    'Miami, FL',
    abbreviation='FIU',
    address_lines=[
        'College of Business',
        '11200 SW 8th St.',
        'Miami, FL  33174'
    ],
    city='Miami',
    characteristics=[
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.LARGE_CITY,
    ]
)

FIU_TARGET = ApplicationTarget(FIU, AP)

UWM = UniversityModel(
    'University of Wisconsin Milwaukee',
    'Milwaukee, WI',
    abbreviation='UWM',
    address_lines=[
        'Sheldon B. Lubar School of Business',
        '3202 N Maryland Ave',
        'Milwaukee, WI  53202'
    ],
    city='Milwaukee',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
    ]
)

UWM_TARGET = ApplicationTarget(UWM, AP)


QUEENS = UniversityModel(
    "Queen's University",
    'Kingston, ON, Canada',
    abbreviation='QU',
    address_lines=[
        'Smith School of Business',
        'Goodes Hall',
        '143 Union St.',
        'Kingston, Ontario',
        'Canada K7L 3N6'
    ],
    city='Kingston',
    country='Canada',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

QUEENS_TARGET = ApplicationTarget(QUEENS, AP)

UMASS_BOSTON = UniversityModel(
    'University of Massachusetts Boston',
    'Boston, MA',
    abbreviation='UMass Boston',
    address_lines=[
        'Department of Accounting and Finance',
        '100 Morrissey Blvd.',
        'Boston, MA  02125-3393'
    ],
    city='Boston',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
    ]
)

UMASS_BOSTON_TARGET = ApplicationTarget(UMASS_BOSTON, AP)

CAL_STATE_FULLERTON = UniversityModel(
    'California State University, Fullerton',
    'Fullerton, CA',
    abbreviation='CSUF',
    address_lines=[
        'College of Business and Economics',
        '2550 Nutwood Ave.',
        'Fullerton, CA  92831'
    ],
    city='Fullerton',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.WEST_COAST,
        OrganizationCharacteristics.WARM_WEATHER
    ]
)

CAL_STATE_FULLERTON_TARGET = ApplicationTarget(CAL_STATE_FULLERTON, AP)

WILFRID_LAURIER = UniversityModel(
    'Wilfrid Laurier University',
    'Waterloo, ON, Canada',
    abbreviation='Laurier',
    address_lines=[
        'Associate Dean of Business: Faculty Development & Research',
        'Lazaridis School of Business & Economics',
        'Wilfrid Laurier University',
        'Waterloo, Ontario, N2L 3C5'
    ],
    city='Waterloo',
    country='Canada',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

WILFRID_LAURIER_HM = HiringManager(
    'Mathieu',
    first_name='Robert',
    gender=Gender.MALE,
    title='Associate Dean of Business: Faculty Development & Research',
    is_doctor=True
)

WILFRID_LAURIER_TARGET = ApplicationTarget(WILFRID_LAURIER, AP + ' (2020-04)', person=WILFRID_LAURIER_HM)

U_TORONTO_SCARBOROUGH = UniversityModel(
    'University of Toronto Scarborough',
    'Scarborough, ON, Canada',
    abbreviation='UTSC',
    address_lines=[
        'Department of Management',
        '1265 Military Trail',
        'Scarborough, ON M1C 1A4',
    ],
    city='Toronto',
    country='Canada',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

U_TORONTO_SCARBOROUGH_TARGET = ApplicationTarget(U_TORONTO_SCARBOROUGH, AP)

AMSTERDAM = UniversityModel(
    'University of Amsterdam',
    'Amsterdam, Netherlands',
    abbreviation='UvA',
    address_lines=[
        'Amsterdam Business School',
        'Plantage Muidergracht 12',
        '1018 TV Amsterdam, Netherlands'
    ],
    city='Amsterdam',
    country='Netherlands',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

AMSTERDAM_TARGET = ApplicationTarget(AMSTERDAM, AP)

COPENHAGEN = UniversityModel(
    'Copenhagen Business School',
    'Frederiksberg, Denmark',
    abbreviation='CBS',
    address_lines=[
        'Solbjerg Plads 3',
        'DK-2000 Frederiksberg, Denmark'
    ],
    city='Frederiksberg',
    country='Denmark',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

COPENHAGEN_TARGET = ApplicationTarget(COPENHAGEN, AP)

HEC_PARIS = UniversityModel(
    'HEC Paris',
    'Jouy-en-Josas, France',
    abbreviation='HEC',
    address_lines=[
        '1 Rue de la Libération',
        '78350 Jouy-en-Josas, France'
    ],
    city='Paris',
    country='France',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

HEC_PARIS_TARGET = ApplicationTarget(HEC_PARIS, AP)

POMPEU_FABRA = UniversityModel(
    'Universitat Pompeu Fabra',
    'Barcelona, Spain',
    abbreviation='UPF',
    address_lines=[
        'Department of Economics and Business',
        'Edifici Jaume I (campus de la Ciutadella)',
        'Ramon Trias Fargas, 25-27',
        '08005 Barcelona'
    ],
    city='Barcelona',
    country='Spain',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.WARM_WEATHER,
    ]
)

POMPEU_FABRA_TARGET = ApplicationTarget(POMPEU_FABRA, AP)

EDHEC = UniversityModel(
    'EDHEC Business School',
    'Nice, France',
    abbreviation='EDHEC',
    address_lines=[
        '24 Avenue Gustave Delory',
        '59100 Roubaix, France'
    ],
    city='Nice',
    country='France',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

EDHEC_TARGET = ApplicationTarget(EDHEC, AP)

BOCCONI = UniversityModel(
    'Bocconi University',
    'Milan, Italy',
    abbreviation='Bocconi',
    address_lines=[
        'Via Roberto Sarfatti',
        '25, 20100 Milano MI',
        'Italy',
    ],
    city='Milan',
    country='Italy',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)

BOCCONI_TARGET = ApplicationTarget(BOCCONI, AP)

HEC_MONTREAL = UniversityModel(
    'HEC Montréal',
    'Montréal, Canada',
    abbreviation='HEC Montréal',
    address_lines=[
        'Finance Department',
        '3000 Chemin de la Côte-Sainte-Catherine',
        'Montréal, QC H3T 2A7',
        'Canada'
    ],
    city='Montréal',
    country='Canada',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)
HEC_MONTREAL_TARGET = ApplicationTarget(HEC_MONTREAL, AP)

ESSEC = UniversityModel(
    'ESSEC Business School',
    'Cergy, France',
    abbreviation='ESSEC',
    address_lines=[
        'Finance Department',
        '3 Avenue Bernard Hirsch',
        '95000 Cergy, France'
    ],
    city='Paris',
    country='France',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.LARGE_CITY,
    ]
)
ESSEC_TARGET = ApplicationTarget(ESSEC, AP)

NOVA = UniversityModel(
    'Universidade Nova de Lisboa',
    'Cascais, Portugal',
    abbreviation='Nova',
    address_lines=[
        'Nova School of Business and Economics',
        'Campus de Carcavelos',
        'Rua da Holanda, n.1',
        '2775-405 Carcavelos, Cascais',
        'Portugal'
    ],
    city='Cascais',
    country='Portugal',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.WARM_WEATHER,
    ]
)
NOVA_HM = HiringManager('Nova Search Committee', is_person=False)
NOVA_TARGET = ApplicationTarget(NOVA, AP, person=NOVA_HM)

NOTTINGHAM = UniversityModel(
    'University of Nottingham',
    'Nottingham, UK',
    abbreviation='UoN',
    address_lines=[
        'School of Economics',
        'Nottingham NG7 2QX',
        'United Kingdom'
    ],
    city='Nottingham',
    country='the UK',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)
NOTTINGHAM_TARGET = ApplicationTarget(NOTTINGHAM, AP)

CHAPMAN = UniversityModel(
    'Chapman University',
    'Orange, CA',
    abbreviation='Chapman',
    address_lines=[
        'George L. Argyros School of Business and Economics',
        'One University Drive',
        'Beckman Hall 301',
        'Orange, CA  92866'
    ],
    city='Orange',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.WEST_COAST,
        OrganizationCharacteristics.WARM_WEATHER,
    ]
)
CHAPMAN_PERSON = HiringManager('Warachka', 'Mitchell', is_doctor=True)
CHAPMAN_TARGET = ApplicationTarget(CHAPMAN, AP, person=CHAPMAN_PERSON)

CENTRAL_EUROPEAN = UniversityModel(
    'Central European University',
    'Vienna, Austria',
    abbreviation='CEU',
    address_lines=[
        'Department of Economics and Business',
        'Quellenstraße 51',
        'A-1100 Wien, Austria',
        'Vienna Commercial Court',
        'FN 502313 x'
    ],
    city='Vienna',
    country='Austria',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)
CENTRAL_EUROPEAN_TARGET = ApplicationTarget(CENTRAL_EUROPEAN, AP)

IMPERIAL_COLLEGE = UniversityModel(
    'Imperial College London',
    'South Kensington, UK',
    abbreviation='Imperial',
    address_lines=[
        'Imperial College Business School',
        'South Kensington Campus',
        'Exhibition Rd.',
        'London SW7 2AZ',
        'United Kingdom'
    ],
    city='London',
    country='the UK',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
    ]
)
IMPERIAL_COLLEGE_TARGET = ApplicationTarget(IMPERIAL_COLLEGE, AP)

UT_ARLINGTON = UniversityModel(
    'University of Texas at Arlington',
    'Arlington, TX',
    abbreviation='UTA',
    address_lines=[
        'College of Business',
        '701 S W St',
        'Arlington, TX  76010'
    ],
    city='Arlington',
    characteristics=[
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.MID_SIZE_CITY,
    ]
)
UT_ARLINGTON_TARGET = ApplicationTarget(UT_ARLINGTON, AP)

WHU_OTTO_BEISHEIM = UniversityModel(
    'WHU - Otto Beisheim School of Management',
    'Vallendar, Germany',
    abbreviation='WHU',
    address_lines=[
        'Burgpl. 2',
        '56179 Vallendar',
        'Germany'
    ],
    city='Vallendar',
    country='Germany',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.SMALL_TOWN,
    ]
)
WHU_OTTO_BEISHEIM_TARGET = ApplicationTarget(WHU_OTTO_BEISHEIM, AP)

NATIONAL_SINGAPORE = UniversityModel(
    'National University of Singapore',
    'Singapore, Singapore',
    abbreviation='NUS',
    address_lines=[
        'NUS Business School',
        'Department of Finance',
        '15 Kent Ridge Dr',
        'Singapore 119245',
        'Singapore',
    ],
    city='Singapore',
    country='Singapore',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.LARGE_CITY,
    ]
)
NATIONAL_SINGAPORE_TARGET = ApplicationTarget(NATIONAL_SINGAPORE, AP)

BI_NORWEGIAN = UniversityModel(
    'BI Norwegian Business School',
    'Oslo, Norway',
    abbreviation='BI',
    address_lines=[
        'Nydalsveien 37',
        '0484 Oslo',
        'Norway'
    ],
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.LARGE_CITY,
    ],
    city='Oslo',
    country='Norway',
)
BI_NORWEGIAN_TARGET = ApplicationTarget(BI_NORWEGIAN, AP)

UC_SAN_DIEGO = UniversityModel(
    'University of California San Diego',
    'San Diego, CA',
    abbreviation='UC San Diego',
    address_lines=[
        'Rady School of Management',
        '9500 Gilman Dr',
        'La Jolla, CA  92093'
    ],
    city='San Diego',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.WEST_COAST,
    ]
)
UC_SAN_DIEGO_TARGET = ApplicationTarget(UC_SAN_DIEGO, AP)

CHINESE_HONG_KONG = UniversityModel(
    'Chinese University of Hong Kong',
    'Hong Kong, Hong Kong',
    abbreviation='CUHK',
    address_lines=[
        'Department of Finance',
        '12/F, Cheng Yu Tung Building',
        '12 Chak Cheung Street',
        'Shatin, N.T., Hong Kong',
        'Hong Kong',
    ],
    city='Hong Kong',
    country='Hong Kong',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.WARM_WEATHER,
    ]
)
CHINESE_HONG_KONG_TARGET = ApplicationTarget(CHINESE_HONG_KONG, AP)

SINGAPORE_MANAGEMENT = UniversityModel(
    'Singapore Management University',
    'Singapore, Singapore',
    abbreviation='SMU',
    address_lines=[
        'Lee Kong Chian School of Business',
        '50 Stamford Rd',
        'SAM - Singapore Management University',
        'Singapore 178899',
        'Singapore'
    ],
    city='Singapore',
    country='Singapore',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.WARM_WEATHER,
    ]
)
SINGAPORE_MANAGEMENT_PERSON = HiringManager('Otto', 'Clemens', is_doctor=True)
SINGAPORE_MANAGEMENT_TARGET = ApplicationTarget(SINGAPORE_MANAGEMENT, AP, person=SINGAPORE_MANAGEMENT_PERSON)
SINGAPORE_MANAGEMENT_QUANT_PERSON = HiringManager('Huang', 'Shirley', is_doctor=True)
SINGAPORE_MANAGEMENT_QUANT_TARGET = ApplicationTarget(
    SINGAPORE_MANAGEMENT, AP, person=SINGAPORE_MANAGEMENT_QUANT_PERSON, custom_app_name='SMU Quant'
)

ERASMUS_ROTTERDAM = UniversityModel(
    'Erasmus University',
    'Rotterdam, Netherlands',
    abbreviation='RSM',
    address_lines=[
        'Rotterdam School of Management',
        'Department of Finance',
        'Burgemeester Oudlaan 50',
        '3062 PA Rotterdam',
        'Netherlands',
    ],
    city='Rotterdam',
    country='the Netherlands',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.MID_SIZE_CITY,
    ]
)
ERASMUS_ROTTERDAM_TARGET = ApplicationTarget(ERASMUS_ROTTERDAM, AP)

CITY_HONG_KONG = UniversityModel(
    'City University of Hong Kong',
    abbreviation='CityU',
    address_lines=[
        'Department of Economics and Finance',
        '9-200, 9/F, Lau Ming Wai Academic Building (LAU)',
        'Tat Chee Avenue, Kowloon Tong, Kowloon',
        'Hong Kong',
    ],
    **HONG_KONG_KWARGS  # type: ignore
)
CITY_HONG_KONG_TARGET = ApplicationTarget(CITY_HONG_KONG, AP)

HKU_BUSINESS = UniversityModel(
    'University of Hong Kong',
    abbreviation='HKU',
    address_lines=[
        'HKU Business School',
        'Faculty of Business and Economics',
        '4/F, K.K. Leung Building',
        'Pok Fu Lam Rd, Pok Fu Lam',
        'Hong Kong'
    ],
    **HONG_KONG_KWARGS  # type: ignore
)
HKU_BUSINESS_TARGET = ApplicationTarget(HKU_BUSINESS, AP)

PONTIFICIA_CHILE = UniversityModel(
    'Pontificia Universidad Católica de Chile',
    'Santiago, Chile',
    abbreviation='UC',
    address_lines=[
        'Escuela de Administración',
        "Av Libertador Bernardo O'Higgins 340",
        "Santiago, Región Metropolitana",
        "Chile"
    ],
    city='Santiago',
    country='Chile',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.SPANISH_SPEAKING,
    ]
)
PONTIFICIA_CHILE_TARGET = ApplicationTarget(PONTIFICIA_CHILE, AP)

VRIJE_AMSTERDAM = UniversityModel(
    'Vrije Universiteit Amsterdam',
    'Amsterdam, Netherlands',
    abbreviation='VU',
    address_lines=[
        'School of Business and Economics',
        'De Boelelaan 1105',
        '1081 HV Amsterdam',
        'Netherlands',
    ],
    city='Amsterdam',
    country='the Netherlands',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.LARGE_CITY,
    ]
)
VRIJE_AMSTERDAM_TARGET = ApplicationTarget(VRIJE_AMSTERDAM, AP)

PARIS_DAUPHINE = UniversityModel(
    'Université Paris-Dauphine',
    'Paris, France',
    abbreviation='Dauphine',
    address_lines=[
        'GFR Finance',
        'Place du Maréchal de Lattre de Tassigny',
        '75016 Paris',
        'France'
    ],
    city='Paris',
    country='France',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.FRENCH_SPEAKING,
    ]
)
PARIS_DAUPHINE_TARGET = ApplicationTarget(PARIS_DAUPHINE, AP)

HONG_KONG_BAPTIST = UniversityModel(
    'Hong Kong Baptist University',
    abbreviation='HKBU',
    address_lines=[
        'Department of Finance and Decision Sciences',
        '224 Waterloo Rd',
        'Kowloon Tong, Hong Kong'
    ],
    **HONG_KONG_KWARGS  # type: ignore
)
HONG_KONG_BAPTIST_TARGET = ApplicationTarget(HONG_KONG_BAPTIST, AP)

BOSTON_U = UniversityModel(
    'Boston University',
    'Boston, MA',
    abbreviation='BU',
    address_lines=[
        'Questrom School of Business',
        'Department of Finance',
        '595 Commonwealth Avenue',
        'Boston, MA  02215'
    ],
    city='Boston',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.FAMILY_CLOSE,
    ]
)
BOSTON_U_TARGET = ApplicationTarget(BOSTON_U, AP)


def get_bu_cv_model(model: 'CVModel') -> 'CVModel':
    interests = deepcopy(RESEARCH_INTERESTS)
    interests.insert(0, 'FinTech')
    model.custom_research_interests = interests
    return model


WASHINGTON_STATE = UniversityModel(
    'Washington State University',
    'Pullman, WA',
    abbreviation='WSU',
    address_lines=[
        'Department of Finance and Management Science',
        'Carson College of Business',
        '300 NE College Ave',
        'Pullman, WA  99163',
    ],
    city='Pullman',
    characteristics=[
        OrganizationCharacteristics.SMALL_TOWN,
    ]
)
WASHINGTON_STATE_TARGET = ApplicationTarget(WASHINGTON_STATE, AP)


ESADE = UniversityModel(
    'ESADE Business School',
    'Barcelona, Spain',
    abbreviation='ESADE',
    address_lines=[
        'Av. de Pedralbes, 60-62, ',
        '08034 Barcelona',
        'Spain'
    ],
    city='Barcelona',
    country='Spain',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.WARM_WEATHER,
    ]
)
ESADE_TARGET = ApplicationTarget(ESADE, AP)

WESTERN = UniversityModel(
    'Western University',
    'London, Canada',
    abbreviation='Western',
    address_lines=[
        'Ivey Business School',
        '1255 Western Rd',
        'London, ON N6G 0N1',
        'Canada'
    ],
    city='London',
    country='Canada',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.MID_SIZE_CITY,
    ]
)
WESTERN_TARGET = ApplicationTarget(WESTERN, AP)


VILLANOVA = UniversityModel(
    'Villanova University',
    'Villanova, PA',
    abbreviation='Villanova',
    address_lines=[
        'Villanova School of Business',
        '800 E. Lancaster Ave',
        'Villanova, PA 19085',
    ],
    city='Villanova',
    characteristics=[
        OrganizationCharacteristics.SUBURBAN,
        OrganizationCharacteristics.FAMILY_CLOSE,
    ]
)
VILLANOVA_TARGET = ApplicationTarget(VILLANOVA, AP)

U_GEORGIA = UniversityModel(
    'University of Georgia',
    'Athens, GA',
    abbreviation='UGA',
    address_lines=[
        'Terry College of Business',
        '600 S Lumpkin St.',
        'Athens, GA  30605'
    ],
    city='Athens',
    characteristics=[
        OrganizationCharacteristics.WARM_WEATHER,
        OrganizationCharacteristics.SMALL_TOWN,
    ]
)
U_GEORGIA_TARGET = ApplicationTarget(U_GEORGIA, AP)

VIRGINIA_TECH = UniversityModel(
    'Virginia Polytechnic Institute and State University',
    'Blacksburg, VA',
    abbreviation='VT',
    address_lines=[
        'Pamplin College of Business',
        '1030 Pamplin Hall',
        'Blacksburg, VA 24061',
    ],
    city='Blacksburg',
    characteristics=[
        OrganizationCharacteristics.FAMILY_CLOSE,
        OrganizationCharacteristics.SMALL_TOWN,
    ]
)
VIRGINIA_TECH_TARGET = ApplicationTarget(VIRGINIA_TECH, AP)

PURDUE = UniversityModel(
    'Purdue University',
    'West Lafayette, IN',
    abbreviation='Purdue',
    address_lines=[
        'Krannert School of Management',
        '403 W State St.',
        'West Lafayette, IN  47907'
    ],
    city='West Lafayette',
    characteristics=[
        OrganizationCharacteristics.SMALL_TOWN,
    ]
)
PURDUE_TARGET = ApplicationTarget(PURDUE, AP)

U_KANSAS = UniversityModel(
    'University of Kansas',
    'Lawrence, KS',
    abbreviation='KU',
    address_lines=[
        'The University of Kansas School of Business',
        '1654 Naismith Dr.',
        'Lawrence, KS  66045',
    ],
    city='Lawrence',
    characteristics=[
        OrganizationCharacteristics.SMALL_TOWN,
    ]
)
U_KANSAS_TARGET = ApplicationTarget(U_KANSAS, AP)

U_CONN = UniversityModel(
    'University of Connecticut',
    'Mansfield, Connecticut',
    abbreviation='UConn',
    address_lines=[
        'UConn School of Business',
        'Department of Finance',
        '2100 Hillside Rd.',
        'Storrs, CT  06269',
    ],
    city='Mansfield',
    characteristics=[
        OrganizationCharacteristics.SMALL_TOWN,
    ]
)
U_CONN_TARGET = ApplicationTarget(U_CONN, AP)

TEXAS_TECH = UniversityModel(
    'Texas Tech University',
    'Lubbock, TX',
    abbreviation='TTU',
    address_lines=[
        'Jerry S. Rawls College of Business',
        'Area of Finance',
        '703 Flint Ave',
        'Lubbock, TX 79409',
    ],
    city='Lubbock',
    characteristics=[
        OrganizationCharacteristics.MID_SIZE_CITY,
        OrganizationCharacteristics.WARM_WEATHER,
    ]
)
TEXAS_TECH_TARGET = ApplicationTarget(TEXAS_TECH, AP)

WARWICK = UniversityModel(
    'University of Warwick',
    'Coventry, UK',
    abbreviation='Warwick',
    address_lines=[
        'Warwick Business School',
        'Scarman Rd.',
        'Coventry CV4 7AL',
        'United Kingdom',
    ],
    city='Coventry',
    country='the UK',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.MID_SIZE_CITY,
    ]
)
WARWICK_TARGET = ApplicationTarget(WARWICK, AP)

IOWA_STATE = UniversityModel(
    'Iowa State University of Science and Technology',
    'Ames, IA',
    abbreviation='Iowa State',
    address_lines=[
        'Ivy College of Business',
        'Gerdin Business Bldg., 1200',
        '2167 Union Dr.',
        'Ames, IA  50011',
    ],
    city='Ames',
    characteristics=[
        OrganizationCharacteristics.SMALL_TOWN,
    ]
)
IOWA_STATE_TARGET = ApplicationTarget(IOWA_STATE, AP)

KINGS_WESTERN = UniversityModel(
    "King's University College at Western University",
    'London, Canada',
    abbreviation="King's",
    address_lines=[
        'School of Management, Economics, and Mathematics',
        '266 Epworth Ave.',
        'London, ON N6A 2M3',
        'Canada',
    ],
    city='London',
    country='Canada',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.MID_SIZE_CITY,
    ]
)
KINGS_WESTERN_PERSON = HiringManager('Erenburg', 'Grigori', is_doctor=True)
KINGS_WESTERN_TARGET = ApplicationTarget(KINGS_WESTERN, AP, person=KINGS_WESTERN_PERSON)

ST_GALLEN = UniversityModel(
    'University of St.Gallen',
    'St. Gallen, Switzerland',
    abbreviation='HSG',
    address_lines=[
        'Dufourstrasse 50',
        '9000 St. Gallen',
        'Switzerland',
    ],
    city='St. Gallen',
    country='Switzerland',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.MID_SIZE_CITY,
    ]
)
ST_GALLEN_PERSON = HiringManager('Ehrenzeller', 'Bernhard', is_doctor=True)
ST_GALLEN_TARGET = ApplicationTarget(ST_GALLEN, AP, person=ST_GALLEN_PERSON)

TSINGHUA = UniversityModel(
    'Tsinghua University',
    'Beijing, China',
    abbreviation='Tsinghua',
    address_lines=[
        'School of Economics and Management',
        'Weilun Building',
        'Haidian District',
        'Beijing, China'
    ],
    city='Beijing',
    country='China',
    characteristics=[
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.INTERNATIONAL
    ]
)
TSINGHUA_TARGET = ApplicationTarget(TSINGHUA, AP)

NATIONAL_TAIWAN = UniversityModel(
    'National Taiwan University',
    'Taipei, Taiwan',
    abbreviation='NTU',
    address_lines=[
        'Department of Finance',
        'National Taiwan University',
        'No.1, Section 4, Roosevelt Road',
        'Taipei 106, Taiwan',
    ],
    city='Taipei',
    country='Taiwan',
    characteristics=[
        OrganizationCharacteristics.INTERNATIONAL,
        OrganizationCharacteristics.LARGE_CITY,
        OrganizationCharacteristics.WARM_WEATHER,
    ],
)
NATIONAL_TAIWAN_PERSON = HiringManager('Recruiting Chair', is_person=False)
NATIONAL_TAIWAN_TARGET = ApplicationTarget(NATIONAL_TAIWAN, AP, person=NATIONAL_TAIWAN_PERSON)