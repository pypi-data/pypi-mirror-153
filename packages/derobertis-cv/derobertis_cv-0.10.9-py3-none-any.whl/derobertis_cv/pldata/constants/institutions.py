
# TODO [#1]: restructure into class

UF_NAME = 'University of Florida'
WARRINGTON = 'Warrington College of Business Administration'
FIRE = 'Department of Finance, Insurance, & Real Estate'
UF_STREET_ADDRESS = 'PO Box 117168'
UF_CITY = 'Gainesville'
UF_STATE = 'FL'
UF_ZIP = '32611-7168'

UF_ADDRESS_LINES = [
    f'{UF_STREET_ADDRESS},',
    f'{UF_CITY}, {UF_STATE} {UF_ZIP}'
]

UF_CONTACT_LINES = [
    WARRINGTON,
    FIRE,
    *UF_ADDRESS_LINES
]

UF_WITH_CONTACT_LINES = [
    UF_NAME,
    *UF_CONTACT_LINES
]

VCU_NAME = 'Virginia Commonwealth University'


ALABAMA = 'University of Alabama'
CULVERHOUSE = 'Culverhouse College of Business'
EFL = 'Department of Economics, Finance, & Legal Studies'
ALABAMA_STREET_ADDRESS = '361 Stadium Dr.'
ALABAMA_CITY = 'Tuscaloosa'
ALABAMA_STATE = 'AL'
ALABAMA_ZIP = '35487'
ALABAMA_ADDRESS_LINES = [
    f'{ALABAMA_STREET_ADDRESS},',
    f'{ALABAMA_CITY}, {ALABAMA_STATE} {ALABAMA_ZIP}'
]

ALABAMA_CONTACT_LINES = [
    CULVERHOUSE,
    EFL,
    *ALABAMA_ADDRESS_LINES
]

ALABAMA_WITH_CONTACT_LINES = [
    ALABAMA,
    *ALABAMA_CONTACT_LINES
]
