from typing import List

from pyexlatex.typing import PyexlatexItem, PyexlatexItems

from derobertis_cv.pldata.constants import contact as public_contact

PRIVATE_EMAIL_1 = "nick@claimfound.com"


def get_private_contact_lines(include_website: bool) -> PyexlatexItems:
    line_2: List[PyexlatexItem] = [public_contact.PHONE]
    if include_website:
        line_2.append(public_contact.STYLED_SITE)
    lines = [[PRIVATE_EMAIL_1], line_2]
    return lines
