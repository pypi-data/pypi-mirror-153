import os
from typing import Optional, Sequence, Union, List
from datetime import datetime
import pyexlatex as pl
import pyexlatex.layouts as ll
from pyexlatex.models.item import ItemBase
import requests

from derobertis_cv.pltemplates.logo import HasLogo


class SoftwareProject(HasLogo, pl.Template):

    def __init__(self, title: str,
                 description: str,
                 display_title: Optional[Union[str, ItemBase, Sequence[Union[str, ItemBase]]]] = None,
                 created: Optional[datetime] = None, updated: Optional[datetime] = None,
                 loc: Optional[int] = None, commits: Optional[int] = None,
                 url: Optional[str] = None, compact: bool = False,
                 github_url: Optional[str] = None,
                 docs_url: Optional[str] = None, logo_url: Optional[str] = None,
                 package_directory: Optional[str] = None, logo_svg_text: Optional[str] = None,
                 logo_base64: Optional[str] = None, logo_fa_icon_class_str: Optional[str] = None):
        self.title = title
        self.display_title = display_title
        self.description = description
        self.created = created
        self.updated = updated
        self.loc = loc
        self.commits = commits
        self.url = url
        self.compact = compact
        self.github_url = github_url
        self.docs_url = docs_url
        self.logo_url = logo_url
        self.package_directory = package_directory
        self.logo_svg_text = logo_svg_text
        self.logo_base64 = logo_base64
        self.logo_fa_icon_class_str = logo_fa_icon_class_str
        self.contents = self._get_contents()
        super().__init__()

    @property
    def url(self) -> Optional[str]:
        try:
            return self._url
        except AttributeError:
            return self.github_url

    @url.setter
    def url(self, value: Optional[str]):
        if value is not None:
            self._url = value

    def _get_contents(self):
        headers = self._get_header()
        description_area = self._get_description_area()

        all_contents = [
            *headers,
            *description_area,
        ]

        return pl.NoPageBreak(all_contents)

    def _get_description_area(self):
        if not self.description:
            return []

        return [
            pl.OutputLineBreak(size_adjustment='8pt'),
            self.description,
            pl.OutputLineBreak(size_adjustment='-3pt')
        ]

    def _get_header(self):
        if self.compact:
            return [ll.HorizontallySpaced([
                self._title_obj,
                self._loc_commits_obj
            ])]

        title_created_line = ll.HorizontallySpaced([
            self._title_obj,
            f'Created: {self._date_str(self.created)}' if self.created else None
        ])

        loc_commits_updated_line = ll.HorizontallySpaced([
            self._loc_commits_obj,
            f'Updated: {self._date_str(self.updated)}' if self.updated else None
        ])

        return [
            title_created_line,
            pl.OutputLineBreak(),
            loc_commits_updated_line
        ]

    def _date_str(self, dt: datetime) -> str:
        return f'{dt.date()}'

    @property
    def _loc_str(self) -> str:
        if self.loc is None:
            return ''

        if self.loc < 1000:
            return f'{self.loc} LOC'

        # Convert to thousands format with k, e.g. 20k lines
        thousands = round(self.loc/1000, 0)
        return f'{thousands:.0f}k LOC'

    @property
    def _title_obj(self) -> Union[pl.Bold, List[Union[pl.Hyperlink, pl.Bold]]]:
        if self.display_title:
            title_content = f'{self.title} ({self.display_title})'
        else:
            title_content = self.title
        if self.url is None:
            title = pl.Bold(title_content)
        else:
            # Handle hyperlink
            styled_title = pl.TextColor(self.title, color=pl.RGB(50, 82, 209, color_name='darkblue'))
            styled_title = pl.Bold(styled_title)
            title = [
                pl.Hyperlink(self.url, styled_title),
                pl.Bold(f' ({self.display_title})') if self.display_title else None
            ]
            title = [t for t in title if t is not None]
            self.add_data_from_content(title)
        return title

    @property
    def _loc_commits_obj(self) -> Optional[pl.Italics]:
        if not (self.loc or self.commits):
            return None

        loc_commits_str = ''
        if self.loc:
            loc_commits_str += self._loc_str
        if self.loc and self.commits:
            loc_commits_str += ', '
        if self.commits:
            loc_commits_str += f'{self.commits} commits'
        return pl.Italics(loc_commits_str)

    @classmethod
    def from_project_report_dict(cls, pr_dict: dict, use_full_loc: bool = True):
        create_dict = {}
        direct_attrs = [
            'created',
            'updated',
            'description',
            'package_directory',
            'url',
            'docs_url',
            'github_url',
            'logo_url',
            'logo_svg_text',
        ]

        if use_full_loc:
            loc_attr = 'full_lines'
        else:
            loc_attr = 'lines'

        map_attrs = {
            'name': 'title',
            loc_attr: 'loc',
            'num_commits': 'commits'
        }

        for attr in direct_attrs:
            create_dict[attr] = pr_dict.get(attr)
        for pr_attr, create_attr in map_attrs.items():
            create_dict[create_attr] = pr_dict[pr_attr]

        return cls(**create_dict)  # type: ignore

    @classmethod
    def list_from_project_report_dict_list(cls, pr_dict_list: List[dict], use_full_loc: bool = True):
        return [cls.from_project_report_dict(pr_dict, use_full_loc=use_full_loc) for pr_dict in pr_dict_list]

