from typing import List

from derobertis_cv.models.course import CourseModel
from derobertis_cv.pldata.constants.institutions import UF_NAME, VCU_NAME
from derobertis_cv.pldata.course_categories import DEBT_COURSE_MAIN_CATEGORIES, EXCEL_LAB_MAIN_CATEGORIES
from derobertis_cv.pldata.courses.fin_model import get_fin_model_course
from derobertis_cv.pldata.universities import UF, VCU


def get_courses() -> List[CourseModel]:
    return [
        get_fin_model_course(),
        CourseModel(
            title='Debt and Money Markets',
            description="A fixed income course focusing on debt analysis and debt portfolio management, also covering "
                        "the use of derivatives for risk management in fixed income portfolios.",
            highlight_description='fixed income course',
            evaluation_score=4.8,
            periods_taught=['Fall 2016', 'Spring 2018'],
            university=UF,
            topics=DEBT_COURSE_MAIN_CATEGORIES,
            course_id='FIN 4243',
        ),
        CourseModel(
            title='Financial Management Lab',
            description="A lab taught as part of a financial management course which focuses on using "
                        "Excel to solve case problems.",
            highlight_description='Excel skills course',
            periods_taught=['Spring 2014'],
            university=VCU,
            topics=EXCEL_LAB_MAIN_CATEGORIES,
            course_id='FIRE 311',
        ),
    ]