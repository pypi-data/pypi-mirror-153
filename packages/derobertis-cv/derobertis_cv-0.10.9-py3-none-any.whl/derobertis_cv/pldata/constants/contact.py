import pyexlatex as pl

FIRST_NAME = 'Nick'
LAST_NAME = 'DeRobertis'
NAME = f'{FIRST_NAME} {LAST_NAME}'
EMAIL = "nick.derobertis@warrington.ufl.edu"
ADDRESS_LINES = [
    '816 32nd Street',
    'Sarasota, FL  34234',
]
ADDRESS = ', '.join(ADDRESS_LINES)
PHONE = "(703) 282-4142"
SITE_URL = "https://nickderobertis.com"
SOFTWARE_URL = f"{SITE_URL}/software"
RESEARCH_URL = f"{SITE_URL}/research"
SITE_DISPLAY = "nickderobertis.com"
STYLED_SITE = pl.Hyperlink(
    SITE_URL,
    pl.Bold(
        pl.TextColor(SITE_DISPLAY, color=pl.RGB(50, 82, 209, color_name="darkblue"))
    ),
)

CONTACT_LINES = [[EMAIL], [PHONE]]
