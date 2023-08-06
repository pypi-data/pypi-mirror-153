import datetime
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Sequence, List, Union, Dict, Callable

import pyexlatex.resume as lr
from pyexlatex.typing import PyexlatexItems

from derobertis_cv.models.course import CourseModel
from derobertis_cv.pldata.timelineable import Timelineable
from derobertis_cv.pltemplates.academic_employment import AcademicEmployment


@dataclass
class EmploymentModel(Timelineable):
    id: str
    description: Sequence[str]
    company_name: str
    job_title: str
    location: str
    begin_date: datetime.date
    end_date: Optional[datetime.date] = None
    date_format: str = "%B %Y"
    latex_contents: Optional[PyexlatexItems] = None
    extra_contents: Optional[Any] = None
    company_short_name: Optional[str] = None
    short_job_title: Optional[str] = None
    hours_per_week: Optional[int] = None

    def __post_init__(self):
        if self.latex_contents is None:
            self.latex_contents = [desc.replace('$', '\\$') for desc in self.description]

    @property
    def sort_key(self) -> datetime.date:
        if self.end_date is not None:
            return self.end_date
        return datetime.datetime.now()

    def to_pyexlatex_employment(self, include_hours_per_week: bool = False) -> lr.Employment:
        date_str = self.date_str
        if include_hours_per_week and self.hours_per_week is not None:
            date_str += f' ({self.hours_per_week} hours/wk)'

        return lr.Employment(
            self.latex_contents,
            self.company_name,
            date_str,
            self.job_title,
            self.location,
        )


@dataclass
class AcademicEmploymentModel(EmploymentModel):
    courses_taught: Optional[Sequence[CourseModel]] = None

    def to_pyexlatex_employment(self, include_hours_per_week: bool = False) -> AcademicEmployment:
        date_str = self.date_str
        if include_hours_per_week and self.hours_per_week is not None:
            date_str += f' ({self.hours_per_week} hours/wk)'

        return AcademicEmployment(
            self.latex_contents,
            self.company_name,
            date_str,
            self.job_title,
            self.location,
            self.courses_taught,
            self.extra_contents
        )


class JobIDs(str, Enum):
    EVB_PORTFOLIO_ANALYST = 'evb_portfolio_analyst'
    CNC_MP = 'cnc_managing_partner'
    FRB_INTERN = 'frb_intern'
    UF_GA = 'uf_ga'
    VCU_GA = 'vcu_ga'
    PARLIAMENT_TUTOR = 'parliament_tutor'
    CLAIMFOUND_CTO = 'claimfound_cto'
    CARBON_HEALTH = "carbon_health"


def filter_jobs(
    jobs: List[Union[EmploymentModel, AcademicEmploymentModel]],
    excluded_companies: Optional[Sequence[str]] = None,
    modify_descriptions: Optional[Dict[JobIDs, Callable[[Sequence[str]], Sequence[str]]]] = None,
) -> List[Union[EmploymentModel, AcademicEmploymentModel]]:
    if excluded_companies:
        jobs = [job for job in jobs if job.id not in excluded_companies]
    jobs.sort(key=lambda job: job.sort_key, reverse=True)
    if modify_descriptions:
        lookup_modifiers: Dict[str, Callable[[Sequence[str]], Sequence[str]]] = {
            key.value: value for key, value in modify_descriptions.items()
        }
        new_jobs: List[EmploymentModel] = []
        for job in jobs:
            if job.id in modify_descriptions:
                new_job = deepcopy(job)
                desc_func = lookup_modifiers[job.id]
                new_job.description = desc_func(new_job.description)
                # TODO [#43]: better handling for modifying latex contents of job descriptions
                new_job.latex_contents = desc_func(new_job.latex_contents)  # type: ignore
                new_jobs.append(new_job)
            else:
                new_jobs.append(job)
        jobs = new_jobs
    return jobs