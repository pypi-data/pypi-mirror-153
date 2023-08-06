import datetime
from enum import Enum
from itertools import chain
from typing import Callable, Dict, List, Optional, Sequence

from derobertis_cv.pldata.employment_model import EmploymentModel, JobIDs, filter_jobs


class PrivateSpecificJobIDs(str, Enum):
    # Put any private job ids here
    pass


PrivateJobIDs = Enum("PrivateJobIDs", [(i.name, i.value) for i in chain(JobIDs, PrivateSpecificJobIDs)])  # type: ignore


def get_professional_jobs(
    excluded_companies: Optional[Sequence[str]] = None,
    modify_descriptions: Optional[
        Dict[PrivateJobIDs, Callable[[Sequence[str]], Sequence[str]]]
    ] = None,
) -> List[EmploymentModel]:
    jobs: List[EmploymentModel] = []
    jobs = filter_jobs(jobs, excluded_companies=excluded_companies, modify_descriptions=modify_descriptions)  # type: ignore
    return jobs
