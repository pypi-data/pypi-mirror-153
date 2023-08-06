from dataclasses import dataclass
from typing import Optional, Sequence, List, Any

from derobertis_cv.models.category import CategoryModel
from derobertis_cv.models.grades.main import GradingModel
from derobertis_cv.models.prereq import CoursePrerequsitesModel
from derobertis_cv.models.resources import ResourceModel, ResourceSection
from derobertis_cv.models.textbook import TextbookModel
from derobertis_cv.models.university import UniversityModel
from derobertis_cv.pltemplates.software.project import SoftwareProject


@dataclass
class CourseModel:
    title: str
    description: str
    highlight_description: Optional[str] = None
    long_description: Optional[str] = None
    periods_taught: Optional[Sequence[str]] = None
    evaluation_score: Optional[float] = None
    evaluation_max_score: int = 5
    university: Optional[UniversityModel] = None
    course_id: Optional[str] = None
    textbook: Optional[TextbookModel] = None
    instructor: str = 'Nick DeRobertis'
    instructor_email: Optional[str] = 'derobertisna@ufl.edu'
    office_location: Optional[str] = 'Stuzin 301A'
    office_hours: Optional[str] = None
    daily_prep: Optional[str] = None
    prerequisites: Optional[CoursePrerequsitesModel] = None
    class_structure_body: Any = None
    grading: Optional[GradingModel] = None
    topics: Optional[Sequence[CategoryModel]] = None
    current_period: Optional[str] = None
    current_time: Optional[str] = None
    website_url: Optional[str] = None
    software_projects: Optional[Sequence[SoftwareProject]] = None
    resources: Optional[Sequence[ResourceSection]] = None

    @property
    def periods_taught_str(self) -> str:
        if self.periods_taught is None:
            return ''
        return ', '.join(self.periods_taught)

    @property
    def name_score_description(self) -> str:
        if self.highlight_description is not None:
            desc = self.highlight_description
        else:
            desc = self.description

        if self.evaluation_score is not None:
            eval_str = f', {self.evaluation_score}/{self.evaluation_max_score} evaluations'
        else:
            eval_str = ''

        if desc or eval_str:
            extra_info = f' ({desc}{eval_str})'
        else:
            extra_info = ''

        name_score_desc_str = f'{self.title}{extra_info}'

        return name_score_desc_str
