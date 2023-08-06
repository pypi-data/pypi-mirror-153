import pyexlatex.resume as lr
from derobertis_cv.pldata.authors import AUTHORS, AuthorExtraTypes

REFERENCE_AUTHOR_KEYS = [
    'andy',
    'sugata',
    'nimal',
    'baolian',
]


def get_references():
    included_authors = [author for author_key, author in AUTHORS.items() if author_key in REFERENCE_AUTHOR_KEYS]
    references = [
        lr.Reference(
            author.name_as_doctor,
            title_lines=author.title_with_extras([AuthorExtraTypes.CV]),
            company=author.company,
            contact_lines=author.contact_lines,
            email=author.email
        )
        for author in included_authors
    ]
    return references

