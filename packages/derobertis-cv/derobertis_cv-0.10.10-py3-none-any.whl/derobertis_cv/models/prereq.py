from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING, Sequence

from derobertis_cv.models.category import CategoryModel

if TYPE_CHECKING:
    from derobertis_cv.models.course import CourseModel


@dataclass
class CoursePrerequsitesModel:
    required_courses: Optional[Sequence['CourseModel']] = None
    recommended_courses: Optional[Sequence['CourseModel']] = None
    courses_description: Optional[str] = None
    technical_skills: Optional[Sequence[CategoryModel]] = None
    technical_skills_description: Optional[str] = None