from enum import Enum
from typing import Optional, Sequence, Dict, List, cast

import pyexlatex as pl

from derobertis_cv.pltemplates.coauthor import CoAuthor
from derobertis_cv.pldata.constants.institutions import UF_NAME, UF_CONTACT_LINES, ALABAMA, ALABAMA_CONTACT_LINES
from derobertis_cv.pldata.constants.authors import (
    AT_WARRINGTON,
    ASSISTANT_PROF,
    ANDY,
    NIMAL,
    NITISH,
    SUGATA,
    CORBIN,
    JIMMY, ASSOCIATE_PROF_OF_FINANCE, BAOLIAN
)


class Author:

    def __init__(self, name: str, author_key: str, title_lines: Optional[Sequence[str]] = None,
                 company: Optional[str] = None,
                 contact_lines: Optional[Sequence[str]] = None, email: Optional[str] = None,
                 extra_names: Optional[Dict[str, str]] = None):
        if extra_names is None:
            extra_names = {}

        self.name = name
        self.author_key = author_key
        self.title_lines = title_lines
        self.company = company
        self.contact_lines = contact_lines
        self.email = email
        self.extra_names = extra_names


    @property
    def name_as_doctor(self) -> str:
        return f'Dr. {self.name}'

    def extras_str(self, extras_keys: Sequence[str]) -> str:
        extra_strs = [self.extra_names.get(key, None) for key in extras_keys]
        extra_strs = [e for e in extra_strs if e]
        if extra_strs:
            return ', '.join(extra_strs)  # type: ignore
        return ''

    def name_with_extras(self, extras_keys: Sequence[str], as_doctor: bool = False) -> str:
        if as_doctor:
            name = self.name_as_doctor
        else:
            name = self.name

        extra_str = self.extras_str(extras_keys)

        if not extra_str:
            return name

        return f'{name} ({extra_str})'

    def title_with_extras(self, extras_keys: Sequence[str]) -> Optional[List[str]]:
        if self.title_lines is None:
            title_lines = []
        else:
            title_lines = list(self.title_lines)

        extra_str = self.extras_str(extras_keys)

        if not extra_str and not title_lines:
            return None
        elif not extra_str:
            return title_lines

        return title_lines + [extra_str]


class AuthorExtraTypes(str, Enum):
    CV = 'cv'


authors = [
    Author(
        'Andy Naranjo',
        ANDY,
        title_lines=[
            'John B. Hall Professor of Finance & Chairman',
        ],
        company=UF_NAME,
        contact_lines=UF_CONTACT_LINES + ['(352) 392-3781'],
        email=f'andy.naranjo{AT_WARRINGTON}',
        extra_names={AuthorExtraTypes.CV: 'Dissertation Co-Chair'},
    ),
    Author(
        'Baolian Wang',
        BAOLIAN,
        title_lines=[
            ASSISTANT_PROF
        ],
        company=UF_NAME,
        contact_lines=UF_CONTACT_LINES + ['(352) 392-6649'],
        email=f'Baolian.Wang{AT_WARRINGTON}',
    ),
    Author(
        'Mahendrarajah Nimalendran',
        NIMAL,
        title_lines=[
            'John H. and Mary Lou Dasburg Chair Full Professor'
        ],
        company=UF_NAME,
        contact_lines=UF_CONTACT_LINES + ['(352) 392-9526'],
        email=f'mahen.nimalendran{AT_WARRINGTON}',
        extra_names={AuthorExtraTypes.CV: 'Dissertation Co-Chair'},
    ),
    Author(
        'Sugata Ray',
        SUGATA,
        title_lines=[
            ASSOCIATE_PROF_OF_FINANCE
        ],
        company=ALABAMA,
        contact_lines=ALABAMA_CONTACT_LINES + ['(205) 348-5726'],
        email=f'sray6@cba.ua.edu',
    ),
    Author(
        'Nitish Kumar',
        NITISH,
        title_lines=[
            ASSISTANT_PROF
        ],
        company=UF_NAME,
        contact_lines=UF_CONTACT_LINES + ['(352) 392-0115'],
        email=f'nitish.kumar{AT_WARRINGTON}',
    ),
    Author(
        'Yong Jin',
        JIMMY
    ),
    Author(
        'Corbin Fox',
        CORBIN
    )
]

CO_AUTHORS = {author.author_key: CoAuthor(author.name) for author in authors}
AUTHORS = {author.author_key: author for author in authors}