import datetime
from typing import List

from derobertis_cv.pldata.education_model import EducationModel
from derobertis_cv.pldata.universities import UF, VCU


def get_education() -> List[EducationModel]:
    return [
        EducationModel(
            UF,
            'Ph.D. in Business Administration - Finance and Real Estate',
            begin_date=datetime.datetime(2014, 8, 15),
            end_date=datetime.datetime(2021, 5, 15),
            short_degree_name='Ph.D.',
        ),
        EducationModel(
            VCU,
            'Master of Science in Business, Concentration in Finance',
            begin_date=datetime.datetime(2013, 8, 15),
            end_date=datetime.datetime(2014, 5, 15),
            short_degree_name='MSF',
        ),
        EducationModel(
            VCU,
            'Bachelor of Science in Business, Concentration in Finance',
            begin_date=datetime.datetime(2010, 8, 15),
            end_date=datetime.datetime(2013, 5, 15),
            short_degree_name='BSF',
        ),
    ]