import datetime
from dataclasses import dataclass
from typing import Optional

from pyexlatex.resume import Education

from derobertis_cv.models.university import UniversityModel
from derobertis_cv.pldata.timelineable import Timelineable


@dataclass
class EducationModel(Timelineable):
    institution: UniversityModel
    degree_name: str
    begin_date: datetime.date
    end_date: Optional[datetime.date] = None
    gpa: Optional[str] = None
    date_format: str = "%B %Y"
    short_degree_name: Optional[str] = None

    @property
    def date_str(self) -> str:
        return f"{self.end_date_str}"

    def to_pyexlatex(self) -> Education:
        return Education(
            self.institution.title,
            self.institution.location,
            self.degree_name,
            self.date_str,
            gpa=self.gpa,
        )
