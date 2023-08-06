from dataclasses import dataclass
from typing import Optional, Sequence, Union, T, Type, Callable  # type: ignore

import pyexlatex as pl

from derobertis_cv.models.cased import CasedModel


@dataclass
class ResourceModel:
    name: str
    url: str
    author: Optional[str] = None
    description: Optional[str] = None

    def to_pyexlatex_contents(self) -> list:
        contents = [
            pl.TextColor(pl.Underline(pl.Hyperlink(self.url, self.name)), 'blue')
        ]
        if self.author is not None:
            contents.append(f'({self.author})')
        if self.description is not None:
            contents.append('|')
            contents.append(self.description)
        return contents


@dataclass
class ResourceSection(CasedModel):
    resources: Sequence[Union[ResourceModel, 'ResourceSection']]
    title: str
    flexible_case: bool = True
    case_lower_func: Callable[[str], str] = lambda x: x.lower()
    case_title_func: Callable[[str], str] = lambda x: x.title()
    case_capitalize_func: Callable[[str], str] = lambda x: x.capitalize()

    def to_pyexlatex_contents(self) -> list:
        return [res.to_pyexlatex_contents() for res in self.resources]

    def to_pyexlatex_subsection(self, section_class: Type[T] = pl.SubSection) -> T:
        items = []
        bullet_items = []
        for content in self.resources:
            if isinstance(content, ResourceModel):
                bullet_items.append(content.to_pyexlatex_contents())
            elif isinstance(content, type(self)):
                items.append(content.to_pyexlatex_subsection(pl.SubSubSection))
            else:
                raise ValueError(f'did not know how to parse {content} of type {type(content)}')

        if bullet_items:
            items.append(pl.UnorderedList(bullet_items))

        return section_class(items, title=self.to_title_case_str())
