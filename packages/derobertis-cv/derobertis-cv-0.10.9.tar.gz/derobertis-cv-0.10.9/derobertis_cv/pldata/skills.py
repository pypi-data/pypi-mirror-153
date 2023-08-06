import operator
from copy import deepcopy
from typing import Sequence, Optional, List, Dict, cast, Set, Union, Final

from pyexlatex.logic.format.and_join import join_with_commas_and_and_output_list

from derobertis_cv.models.skill import SkillModel
from derobertis_cv.models.cased import first_word_untouched_rest_capitalized, \
    first_word_untouched_rest_lower, first_word_untouched_rest_title
from derobertis_cv.models.skill_experience import SkillExperience
from derobertis_cv.models.skill_experiences import SkillExperiences
from derobertis_cv.pldata.cover_letters.models import SkillFocusPriority, SpecificApplicationFocus, ApplicationFocus

PROGRAMMING_BEGIN_DATE: Final[str] = "9/1/2012"
CF_BEGIN_DATE: Final[str] = "8/1/2016"
CARBON_BEGIN_DATE: Final[str] = "4/12/2021"
GRAPHQL_BEGIN_DATE: Final[str] = "12/20/2021"


def _recursive_sort_skills(skills: List[SkillModel], **sort_kwargs):
    skills.sort(**sort_kwargs)
    for skill in skills:
        _recursive_sort_skills(skill.children, **sort_kwargs)

# Pure categories
SOFT_SKILLS = SkillModel('Soft Skills', 5)
OTHER = SkillModel('Other', 3)

# Skills
PROGRAMMING_SKILL = SkillModel(
    'Programming', 5, experience=SkillExperience(PROGRAMMING_BEGIN_DATE, hours_per_week=30), priority=SkillFocusPriority(5)
)
PRESENTATION_SKILL = SkillModel('presentation', 4, priority=SkillFocusPriority(3))
COMMUNICATION_SKILL = SkillModel('Communication', 5, parents=(SOFT_SKILLS,))
CRITICAL_THINKING_SKILL = SkillModel('critical thinking', 5, parents=(SOFT_SKILLS,), priority=SkillFocusPriority(2))
LEADERSHIP_SKILL = SkillModel('leadership', 4, parents=(SOFT_SKILLS,), priority=SkillFocusPriority(2))
MULTITASKING_SKILL = SkillModel('multitasking', 5, parents=(SOFT_SKILLS,), priority=SkillFocusPriority(1))
ORGANIZATION_SKILL = SkillModel('organization', 4, parents=(SOFT_SKILLS,), priority=SkillFocusPriority(1))
WORK_ETHIC_SKILL = SkillModel('work ethic', 5, parents=(SOFT_SKILLS,), priority=SkillFocusPriority(1))
TEACHING_SKILL = SkillModel(
    'teaching', 5, parents=(SOFT_SKILLS,), priority=SkillFocusPriority(2, {ApplicationFocus.ACADEMIC: 5})
)
ATTENTION_TO_DETAIL_SKILL = SkillModel('attention to detail', 5, parents=(SOFT_SKILLS,))
SOFTWARE_ARCHITECTURE_SKILL = SkillModel(
    'software architecture', 4, primary_category=PROGRAMMING_SKILL,
    experience=SkillExperiences([
        SkillExperience(PROGRAMMING_BEGIN_DATE, hours_per_week=4, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=8),
    ]),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5})
)
OS_SKILL = SkillModel('operating systems', 3, primary_category=OTHER, priority=SkillFocusPriority(1))
HARDWARE_SKILL = SkillModel('computer hardware', 3, primary_category=OTHER, priority=SkillFocusPriority(1))
SOFTWARE_DEVELOPMENT_SKILL = SkillModel(
    'software development', 5, parents=(PROGRAMMING_SKILL,),
    experience=SkillExperiences([
        SkillExperience(PROGRAMMING_BEGIN_DATE, hours_per_week=20, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=30),
    ]),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5})
)
FRONTEND_SKILL = SkillModel(
    'Front-end Development', 4, parents=(SOFTWARE_DEVELOPMENT_SKILL, SOFTWARE_ARCHITECTURE_SKILL),
    primary_category=PROGRAMMING_SKILL,
    experience=SkillExperiences([
        SkillExperience(CF_BEGIN_DATE, hours_per_week=5, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=10),
    ]),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
)
BACKEND_SKILL = SkillModel(
    'Back-end Development', 5, parents=(SOFTWARE_DEVELOPMENT_SKILL, SOFTWARE_ARCHITECTURE_SKILL),
    primary_category=PROGRAMMING_SKILL,
    experience=SkillExperiences([
        SkillExperience(PROGRAMMING_BEGIN_DATE, hours_per_week=10, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=20),
    ]),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
)
CLI_SKILL = SkillModel(
    'CLI Development',
    3,
    parents=(SOFTWARE_DEVELOPMENT_SKILL, SOFTWARE_ARCHITECTURE_SKILL),
    case_capitalize_func=first_word_untouched_rest_capitalized,
    case_lower_func=first_word_untouched_rest_lower,
    case_title_func=first_word_untouched_rest_title,
    primary_category=PROGRAMMING_SKILL,
    experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=1),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 4})
)
DATABASE_SKILL = SkillModel(
    'Databases', 4, parents=(PROGRAMMING_SKILL,), experience=SkillExperience('4/1/2013', hours_per_week=2),
    priority=SkillFocusPriority(5)
)
DEV_OPS_SKILL = SkillModel(
    'Dev-Ops', 4, parents=(PROGRAMMING_SKILL,), primary_category='self',
    experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=2),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
)
REMOTE_DEVELOPMENT_SKILL = SkillModel(
    'Remote development', 3, parents=(PROGRAMMING_SKILL,),
    experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=0.5),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 4})
)
SECURITY_SKILL = SkillModel(
    'Security', 3, parents=(PROGRAMMING_SKILL, SOFTWARE_ARCHITECTURE_SKILL),
    experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=2),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 5})
)
WEB_DEVELOPMENT_SKILL = SkillModel(
    'Web Development',
    4,
    parents=(SOFTWARE_DEVELOPMENT_SKILL, SOFTWARE_ARCHITECTURE_SKILL, REMOTE_DEVELOPMENT_SKILL, SECURITY_SKILL),
    primary_category=PROGRAMMING_SKILL,
    experience=SkillExperiences([
        SkillExperience(CF_BEGIN_DATE, hours_per_week=10, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=15),
    ]),
    priority=SkillFocusPriority(4, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 5})
)
MOBILE_DEVELOPMENT_SKILL = SkillModel(
    "Mobile Development",
    3,
    parents=(SOFTWARE_DEVELOPMENT_SKILL, SOFTWARE_ARCHITECTURE_SKILL, REMOTE_DEVELOPMENT_SKILL, SECURITY_SKILL),
    primary_category=PROGRAMMING_SKILL,
    experience=SkillExperience(CARBON_BEGIN_DATE, hours_per_week=15),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 4})
)
CSS_SKILL = SkillModel(
    'CSS', 4, parents=(WEB_DEVELOPMENT_SKILL, FRONTEND_SKILL), flexible_case=False, primary_category=PRESENTATION_SKILL,
    experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=1),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
)
FRAMEWORK_SKILL = SkillModel('Frameworks', 5, parents=(PROGRAMMING_SKILL,))
DEBUGGING_SKILL = SkillModel(
    'Debugging', 4, parents=(PROGRAMMING_SKILL,),
    experience=SkillExperience(PROGRAMMING_BEGIN_DATE, hours_per_week=2),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
)
TESTING_SKILL = SkillModel(
    'Automated testing', 4, parents=(PROGRAMMING_SKILL,),
    experience=SkillExperiences([
        SkillExperience('1/1/2018', hours_per_week=2, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=10),
    ]),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
)
PARALLELISM_SKILL = SkillModel(
    'Parallelism', 4, parents=(PROGRAMMING_SKILL,),
    experience=SkillExperience('9/1/2015', hours_per_week=0.5),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 5})
)
CRYPTOGRAPHY_SKILL = SkillModel(
    'Cryptography', 3, parents=(PROGRAMMING_SKILL, SECURITY_SKILL),
    experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=0.15),
    priority=SkillFocusPriority(
        2,
        {
            SpecificApplicationFocus.TECH_COMPANY: 5,
            SpecificApplicationFocus.DATA_SCIENCE: 4,
            ApplicationFocus.ACADEMIC: 3
        }
    )
)
ASYNC_SKILL = SkillModel(
    'Asynchronous Programming', 4, parents=(PROGRAMMING_SKILL,),
    experience=SkillExperiences([
        SkillExperience('6/1/2017', hours_per_week=1.5, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=5)
    ]),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
)
DISTRIBUTED_SKILL = SkillModel(
    'Distributed Computing', 4, parents=(REMOTE_DEVELOPMENT_SKILL,), primary_category=PROGRAMMING_SKILL,
    experience=SkillExperience('9/1/2015', hours_per_week=0.5),
    priority=SkillFocusPriority(4, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.ASSET_MANAGER: 3})
)
EXCEL_SKILL = SkillModel(
    'Excel', 4, flexible_case=False, primary_category=OTHER,
    experience=SkillExperience('9/1/2005', hours_per_week=1),
)
AUTOMATION_SKILL = SkillModel(
    'automation', 5, parents=(PROGRAMMING_SKILL,),
    experience=SkillExperience(PROGRAMMING_BEGIN_DATE, hours_per_week=2),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 4})
)
SERVER_ADMIN_SKILL = SkillModel(
    'server administration', 4, parents=(DEV_OPS_SKILL, WEB_DEVELOPMENT_SKILL),
    experience=SkillExperiences([
        SkillExperience(CF_BEGIN_DATE, hours_per_week=0.5, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.1),
    ]),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 4})
)
NETWORKING_SKILL = SkillModel(
    'networking', 3, parents=(DEV_OPS_SKILL,),
    experience=SkillExperiences([
        SkillExperience(CF_BEGIN_DATE, hours_per_week=0.25, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.05),
    ]),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 3})
)
MONITORING_SKILL = SkillModel(
    'application monitoring', 2, parents=(DEV_OPS_SKILL,),
    experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=0.25),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 3})
)
CI_SKILL = SkillModel(
    'CI/CD', 4, parents=(DEV_OPS_SKILL,), flexible_case=False,
    experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=1),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
)
SEO_SKILL = SkillModel(
    'SEO', 2, parents=(WEB_DEVELOPMENT_SKILL,), flexible_case=False, primary_category=PROGRAMMING_SKILL,
    experience=SkillExperience('1/1/2018', hours_per_week=0.5, end_date_inp=CARBON_BEGIN_DATE),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 4})
)
CMS_SKILL = SkillModel(
    'CMS', 4, parents=(WEB_DEVELOPMENT_SKILL,), flexible_case=False, primary_category=PROGRAMMING_SKILL,
    experience=SkillExperiences([
        SkillExperience('1/1/2018', hours_per_week=0.5, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.05),
    ]),
    priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 2})
)
MIGRATIONS_SKILL = SkillModel(
    'migrations', 5, parents=(DATABASE_SKILL,), primary_category=PROGRAMMING_SKILL,
    experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=0.5),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
)
IDE_SKILL = SkillModel(
    'IDEs', 4, parents=(PROGRAMMING_SKILL,), flexible_case=False,
    experience=SkillExperiences([
        SkillExperience('1/1/2016', hours_per_week=20, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=35),
    ]),
    priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 2})
)


LINUX_SKILL = SkillModel(
    'Linux', 4, parents=(OS_SKILL,), flexible_case=False, primary_category=OTHER,
    experience=SkillExperiences([
        SkillExperience('1/1/2004', hours_per_week=20, end_date_inp='1/1/2008'),
        SkillExperience('6/1/2020', hours_per_week=40, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=5),
    ]),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 3})
)
WINDOWS_SKILL = SkillModel(
    'Windows', 4, parents=(OS_SKILL,), flexible_case=False, primary_category=OTHER,
    experience=SkillExperiences([
        SkillExperience('1/1/2000', hours_per_week=30, end_date_inp='6/1/2020'),
        SkillExperience('6/1/2020', hours_per_week=5),
    ]),
    priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 2})
)
MAC_SKILL = SkillModel(
    'Mac', 3, parents=(OS_SKILL,), flexible_case=False, primary_category=OTHER,
    experience=SkillExperience(CARBON_BEGIN_DATE, hours_per_week=40),
    priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 3})
)

TYPE_SETTING_SKILL = SkillModel('Typesetting', 4, parents=(PRESENTATION_SKILL,), priority=SkillFocusPriority(2))
WRITING_SKILL = SkillModel('Writing', 4, parents=(PRESENTATION_SKILL, SOFT_SKILLS), priority=SkillFocusPriority(2))
RESEARCH_SKILL = SkillModel('Research', 5, priority=SkillFocusPriority(4))
DATA_SCIENCE_SKILL = SkillModel(
    'Data Science',
    5,
    parents=(PROGRAMMING_SKILL, RESEARCH_SKILL),
    primary_category='self', priority=SkillFocusPriority(5)
)
STATISTICS_SKILL = SkillModel(
    'Statistics', 5, parents=(DATA_SCIENCE_SKILL,),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.ECONOMIST: 4, SpecificApplicationFocus.DATA_SCIENCE: 4})
)
MODELING_SKILL = SkillModel(
    'Modeling', 4, parents=(DATA_SCIENCE_SKILL,),
    priority=SkillFocusPriority(
        4,
        {
            SpecificApplicationFocus.ECONOMIST: 5,
            SpecificApplicationFocus.DATA_SCIENCE: 5,
            SpecificApplicationFocus.TECH_COMPANY: 5,
        }
    )
)
VERSION_CONTORL_SKILL = SkillModel(
    'Version Control', 4, parents=(PROGRAMMING_SKILL,),
    experience=SkillExperience('3/1/2016', hours_per_week=1),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
)
COLLABORATION_SKILL = SkillModel('Collaboration', 5, parents=(SOFT_SKILLS,), priority=SkillFocusPriority(1))
ENTREPRENEURSHIP_SKILL = SkillModel('Entrepreneurship', 5, parents=(SOFT_SKILLS,), priority=SkillFocusPriority(2))
PARSING_SKILL = SkillModel(
    'Parsing', 4, parents=(PROGRAMMING_SKILL,),
    experience=SkillExperience('3/1/2015', hours_per_week=1),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 4, SpecificApplicationFocus.DATA_SCIENCE: 3})
)
TIME_SERIES_SKILL = SkillModel(
    'Time-Series', 3, parents=(STATISTICS_SKILL,), primary_category=DATA_SCIENCE_SKILL,
    experience=SkillExperience('9/1/2013', hours_per_week=1),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.ECONOMIST: 5, SpecificApplicationFocus.DATA_SCIENCE: 5})
)
FORECASTING_SKILL = SkillModel(
    'Forecasting', 3, parents=(TIME_SERIES_SKILL,), primary_category=DATA_SCIENCE_SKILL,
    experience=SkillExperience('9/1/2013', hours_per_week=1),
    priority=SkillFocusPriority(
        4,
        {
            ApplicationFocus.ACADEMIC: 2,
            SpecificApplicationFocus.ASSET_MANAGER: 3
        }
    )
)
WEB_SCRAPING_SKILL = SkillModel(
    'Web-scraping', 4, parents=(PROGRAMMING_SKILL, AUTOMATION_SKILL),
    experience=SkillExperience('8/1/2015', hours_per_week=1),
    priority=SkillFocusPriority(5, {SpecificApplicationFocus.TECH_COMPANY: 4})
)
DOCUMENTATION_SKILL = SkillModel(
    'documentation', 4, parents=(PROGRAMMING_SKILL, PRESENTATION_SKILL, TYPE_SETTING_SKILL),
    experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=1),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 4})
)
TEMPLATING_SKILL = SkillModel(
    'templating', 5, parents=(PROGRAMMING_SKILL, PRESENTATION_SKILL, TYPE_SETTING_SKILL),
    experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=1),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 4, SpecificApplicationFocus.DATA_SCIENCE: 3})
)


OPEN_SOURCE_SKILL = SkillModel(
    'Open-Source Development', 5, parents=(PROGRAMMING_SKILL, COLLABORATION_SKILL),
    experience=SkillExperience('9/1/2015', hours_per_week=2),
    priority=SkillFocusPriority(4, {ApplicationFocus.ACADEMIC: 3})
)

MACHINE_LEARNING_SKILL = SkillModel(
    'machine learning', 3, parents=(DATA_SCIENCE_SKILL,),
    experience=SkillExperience('1/1/2016', hours_per_week=0.5),
    priority=SkillFocusPriority(5)
)
DATA_MUNGING_SKILL = SkillModel(
    'data munging', 5, parents=(DATA_SCIENCE_SKILL,),
    experience=SkillExperience('4/1/2013', hours_per_week=3),
    priority=SkillFocusPriority(4, {SpecificApplicationFocus.ECONOMIST: 5, SpecificApplicationFocus.DATA_SCIENCE: 5})
)
DATA_ANALYSIS_SKILL = SkillModel(
    'Data Analysis', 5, parents=(DATA_SCIENCE_SKILL,),
    experience=SkillExperience('5/1/2011', hours_per_week=2),
    priority=SkillFocusPriority(4, {SpecificApplicationFocus.ECONOMIST: 5, SpecificApplicationFocus.DATA_SCIENCE: 5})
)
VISUALIZATION_SKILL = SkillModel(
    'visualization', 4, parents=(DATA_SCIENCE_SKILL, PRESENTATION_SKILL),
    experience=SkillExperience('5/1/2011', hours_per_week=0.5),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.ECONOMIST: 4, SpecificApplicationFocus.DATA_SCIENCE: 4})
)
GEOVISUALIZATION_SKILL = SkillModel(
    'geovisualization', 3, parents=(VISUALIZATION_SKILL,), primary_category=DATA_SCIENCE_SKILL,
    experience=SkillExperience('3/1/2020', hours_per_week=0.2, one_time_hours=50),
    priority=SkillFocusPriority(2, {SpecificApplicationFocus.ECONOMIST: 3, SpecificApplicationFocus.DATA_SCIENCE: 4})
)
PLOTTING_SKILL = SkillModel(
    'plotting', 4, parents=(PROGRAMMING_SKILL, PRESENTATION_SKILL, VISUALIZATION_SKILL),
    primary_category=PRESENTATION_SKILL,
    experience=SkillExperience('5/1/2011', hours_per_week=0.5),
    priority=SkillFocusPriority(1, {SpecificApplicationFocus.ECONOMIST: 2, SpecificApplicationFocus.DATA_SCIENCE: 2})
)


PYTHON_SKILL = SkillModel(
    'Python', 5, parents=(PROGRAMMING_SKILL,), flexible_case=False,
    experience=SkillExperiences([
        SkillExperience('3/1/2015', hours_per_week=25, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=5),
    ]),
    priority=SkillFocusPriority(5)
)
JS_SKILL = SkillModel(
    'JavaScript', 4, parents=(PROGRAMMING_SKILL,), flexible_case=False,
    experience=SkillExperiences([
        SkillExperience(CF_BEGIN_DATE, hours_per_week=4, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=15),
    ]),
    priority=SkillFocusPriority(5)
)
TS_SKILL = SkillModel(
    'TypeScript', 4, parents=(JS_SKILL,), flexible_case=False, primary_category=PROGRAMMING_SKILL,
    experience=SkillExperiences([
        SkillExperience(CF_BEGIN_DATE, hours_per_week=4, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=15),
    ]),
    priority=SkillFocusPriority(5)
)
JAVA_SKILL = SkillModel(
    "Java", 2, parents=(PROGRAMMING_SKILL,), flexible_case=False, primary_category=PROGRAMMING_SKILL,
    experience=SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.5),
    priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 4}),
)
SCALA_SKILL = SkillModel(
    "Scala", 4, parents=(PROGRAMMING_SKILL, JAVA_SKILL), flexible_case=False, primary_category=PROGRAMMING_SKILL,
    experience=SkillExperiences([
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=10, end_date_inp=GRAPHQL_BEGIN_DATE),
        SkillExperience(GRAPHQL_BEGIN_DATE, hours_per_week=5),
    ]),
    priority=SkillFocusPriority(5),
)
KOTLIN_SKILL = SkillModel(
    "Kotlin", 3, parents=(PROGRAMMING_SKILL, JAVA_SKILL), flexible_case=False, primary_category=PROGRAMMING_SKILL,
    experience=SkillExperiences([
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.5, end_date_inp=GRAPHQL_BEGIN_DATE),
        SkillExperience(GRAPHQL_BEGIN_DATE, hours_per_week=5),
    ]),
    priority=SkillFocusPriority(3),
)
AWS_SKILL = SkillModel(
    'AWS', 3, parents=(DEV_OPS_SKILL, WEB_DEVELOPMENT_SKILL, REMOTE_DEVELOPMENT_SKILL), flexible_case=False,
    experience=SkillExperiences([
        SkillExperience(CF_BEGIN_DATE, hours_per_week=1, end_date_inp=CARBON_BEGIN_DATE),
        SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.2),
    ]),
    priority=SkillFocusPriority(4, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 5})
)

DS_FRAMEWORK_SKILLS = (FRAMEWORK_SKILL, PYTHON_SKILL, DATA_SCIENCE_SKILL)
BE_PYTHON_WEB_FRAMEWORK_SKILLS = (FRAMEWORK_SKILL, PYTHON_SKILL, WEB_DEVELOPMENT_SKILL, BACKEND_SKILL)
BE_JAVA_WEB_FRAMEWORK_SKILLS = (FRAMEWORK_SKILL, JAVA_SKILL, WEB_DEVELOPMENT_SKILL, BACKEND_SKILL)
FE_TS_WEB_FRAMEWORK_SKILLS = (FRAMEWORK_SKILL, TS_SKILL, WEB_DEVELOPMENT_SKILL, FRONTEND_SKILL)
FULL_STACK_WEB_PYTHON_FRAMEWORK_SKILLS = BE_PYTHON_WEB_FRAMEWORK_SKILLS + (FRONTEND_SKILL,)
WEB_SCRAPING_FRAMEWORK_SKILLS = (FRAMEWORK_SKILL, WEB_SCRAPING_SKILL, PYTHON_SKILL)
PARSING_FRAMEWORK_SKILLS = (FRAMEWORK_SKILL, PARSING_SKILL, PYTHON_SKILL)
ASYNC_FRAMEWORK_SKILLS = (FRAMEWORK_SKILL, PYTHON_SKILL, ASYNC_SKILL)


_SKILLS: List[SkillModel] = [
    PROGRAMMING_SKILL,
    DATA_ANALYSIS_SKILL,
    DATA_MUNGING_SKILL,
    SOFTWARE_ARCHITECTURE_SKILL,
    OS_SKILL,
    SOFTWARE_DEVELOPMENT_SKILL,
    FRONTEND_SKILL,
    BACKEND_SKILL,
    CLI_SKILL,
    DATABASE_SKILL,
    DEV_OPS_SKILL,
    REMOTE_DEVELOPMENT_SKILL,
    SECURITY_SKILL,
    WEB_DEVELOPMENT_SKILL,
    MOBILE_DEVELOPMENT_SKILL,
    CSS_SKILL,
    FRAMEWORK_SKILL,
    DEBUGGING_SKILL,
    TESTING_SKILL,
    PARALLELISM_SKILL,
    CRYPTOGRAPHY_SKILL,
    ASYNC_SKILL,
    DISTRIBUTED_SKILL,
    EXCEL_SKILL,
    AUTOMATION_SKILL,
    SERVER_ADMIN_SKILL,
    NETWORKING_SKILL,
    MONITORING_SKILL,
    CI_SKILL,
    LINUX_SKILL,
    WINDOWS_SKILL,
    MAC_SKILL,
    PRESENTATION_SKILL,
    TYPE_SETTING_SKILL,
    COMMUNICATION_SKILL,
    CRITICAL_THINKING_SKILL,
    LEADERSHIP_SKILL,
    MULTITASKING_SKILL,
    ORGANIZATION_SKILL,
    WORK_ETHIC_SKILL,
    TEACHING_SKILL,
    ATTENTION_TO_DETAIL_SKILL,
    WRITING_SKILL,
    RESEARCH_SKILL,
    STATISTICS_SKILL,
    MODELING_SKILL,
    VERSION_CONTORL_SKILL,
    COLLABORATION_SKILL,
    ENTREPRENEURSHIP_SKILL,
    PARSING_SKILL,
    TIME_SERIES_SKILL,
    FORECASTING_SKILL,
    WEB_SCRAPING_SKILL,
    DOCUMENTATION_SKILL,
    TEMPLATING_SKILL,
    PLOTTING_SKILL,
    OPEN_SOURCE_SKILL,
    DATA_SCIENCE_SKILL,
    MACHINE_LEARNING_SKILL,
    PYTHON_SKILL,
    JS_SKILL,
    TS_SKILL,
    SCALA_SKILL,
    KOTLIN_SKILL,
    JAVA_SKILL,
    AWS_SKILL,
    SEO_SKILL,
    CMS_SKILL,
    MIGRATIONS_SKILL,
    HARDWARE_SKILL,
    IDE_SKILL,
    VISUALIZATION_SKILL,
    GEOVISUALIZATION_SKILL,
    SkillModel(
        'SQL', 4, parents=(DATABASE_SKILL,), flexible_case=False, primary_category=PROGRAMMING_SKILL,
        experience=SkillExperience('2/1/2015', hours_per_week=1),
        priority=SkillFocusPriority(5)
    ),
    SkillModel(
        'Redis', 4, parents=(DATABASE_SKILL,), flexible_case=False, primary_category=FRAMEWORK_SKILL,
        experience=SkillExperience('1/1/2018', hours_per_week=0.2),
        priority=SkillFocusPriority(
            2,
            {
                SpecificApplicationFocus.TECH_COMPANY: 5,
                SpecificApplicationFocus.DATA_SCIENCE: 3,
                SpecificApplicationFocus.ECONOMIST: 3
            }
        )
    ),
    SkillModel(
        'Angular', 4, parents=FE_TS_WEB_FRAMEWORK_SKILLS, flexible_case=False, primary_category=FRAMEWORK_SKILL,
        experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=3, end_date_inp=CARBON_BEGIN_DATE),
        priority=SkillFocusPriority(4, {SpecificApplicationFocus.TECH_COMPANY: 5})
    ),
    SkillModel(
        'Compodoc', 3, parents=FE_TS_WEB_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=0.1, end_date_inp=CARBON_BEGIN_DATE),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 2})
    ),
    SkillModel(
        'React', 4, parents=FE_TS_WEB_FRAMEWORK_SKILLS, flexible_case=False, primary_category=FRAMEWORK_SKILL,
        experience=SkillExperiences([
            SkillExperience('5/14/2020', one_time_hours=30, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=10),
        ]),
        priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5})
    ),
    SkillModel(
        'React Native', 4, parents=(FRAMEWORK_SKILL, TS_SKILL, MOBILE_DEVELOPMENT_SKILL, FRONTEND_SKILL),
        flexible_case=False, primary_category=FRAMEWORK_SKILL,
        experience=SkillExperience(CARBON_BEGIN_DATE, hours_per_week=15),
        priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5})
    ),
    SkillModel(
        'Storybook', 3, parents=FE_TS_WEB_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperiences([
            SkillExperience('2/1/2021', one_time_hours=10, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.5),
        ]),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 2})
    ),
    SkillModel(
        'Svelte', 3, parents=FE_TS_WEB_FRAMEWORK_SKILLS, flexible_case=False, primary_category=FRAMEWORK_SKILL,
        experience=SkillExperience('1/15/2021', hours_per_week=0, one_time_hours=40),
        priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5})
    ),
    SkillModel(
        'Webpack', 3, parents=FE_TS_WEB_FRAMEWORK_SKILLS, flexible_case=False, primary_category=FRAMEWORK_SKILL,
        experience=SkillExperience('10/1/2020', hours_per_week=0.1),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 4})
    ),
    SkillModel(
        'Babel', 2, parents=FE_TS_WEB_FRAMEWORK_SKILLS, flexible_case=False, primary_category=FRAMEWORK_SKILL,
        experience=SkillExperience('10/1/2020', hours_per_week=0.01),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3})
    ),
    SkillModel(
        'Jest', 4, parents=FE_TS_WEB_FRAMEWORK_SKILLS, flexible_case=False, primary_category=FRAMEWORK_SKILL,
        experience=SkillExperience(CARBON_BEGIN_DATE, hours_per_week=5),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3})
    ),
    SkillModel(
        'ESLint', 3, parents=FE_TS_WEB_FRAMEWORK_SKILLS, flexible_case=False, primary_category=FRAMEWORK_SKILL,
        experience=SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.1),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3})
    ),
    SkillModel(
        'Qt', 2, parents=(FRAMEWORK_SKILL, FRONTEND_SKILL), flexible_case=False, primary_category=FRAMEWORK_SKILL,
        experience=SkillExperience('2/12/2021', hours_per_week=0, one_time_hours=10),
        priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5})
    ),
    SkillModel(
        'Docker', 4, parents=(DEV_OPS_SKILL,), flexible_case=False,
        experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=2),
        priority=SkillFocusPriority(5)
    ),
    SkillModel(
        'LaTeX', 4, parents=(TYPE_SETTING_SKILL, RESEARCH_SKILL), flexible_case=False,
        primary_category=PRESENTATION_SKILL,
        experience=SkillExperience('2/1/2015', hours_per_week=1),
        priority=SkillFocusPriority(5)
    ),
    SkillModel(
        'SAS', 3, parents=(PROGRAMMING_SKILL,), flexible_case=False,
        experience=SkillExperience('2/1/2015', hours_per_week=0, one_time_hours=400),
        priority=SkillFocusPriority(5)
    ),
    SkillModel(
        'Stata', 4, parents=(PROGRAMMING_SKILL,), flexible_case=False,
        experience=SkillExperience(PROGRAMMING_BEGIN_DATE, hours_per_week=0, one_time_hours=800),
        priority=SkillFocusPriority(5)
    ),
    SkillModel(
        'R', 2, parents=(PROGRAMMING_SKILL,), flexible_case=False,
        experience=SkillExperience('10/1/2015', hours_per_week=0, one_time_hours=30),
        priority=SkillFocusPriority(5)
    ),
    SkillModel(
        'MATLAB', 1, parents=(PROGRAMMING_SKILL,), flexible_case=False,
        experience=SkillExperience('2/1/2013', hours_per_week=0, one_time_hours=20),
        priority=SkillFocusPriority(5)
    ),
    SkillModel(
        'NoSQL', 2, parents=(DATABASE_SKILL,), flexible_case=False, primary_category=PROGRAMMING_SKILL,
        experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=0.25),
        priority=SkillFocusPriority(5)
    ),
    SkillModel(
        'Git', 4, parents=(VERSION_CONTORL_SKILL,), flexible_case=False, primary_category=PROGRAMMING_SKILL,
        experience=SkillExperience('3/1/2016', hours_per_week=1),
        priority=SkillFocusPriority(4, {SpecificApplicationFocus.TECH_COMPANY: 5})
    ),
    SkillModel(
        'Bash', 3, parents=(PROGRAMMING_SKILL,), flexible_case=False,
        experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=0.5),
        priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 4})
    ),
    SkillModel(
        'EC2', 4, parents=(AWS_SKILL, SERVER_ADMIN_SKILL), flexible_case=False, primary_category=DEV_OPS_SKILL,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=0.5, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.1),
        ]),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),
    SkillModel(
        'RDS', 3, parents=(AWS_SKILL, DATABASE_SKILL), flexible_case=False, primary_category=DEV_OPS_SKILL,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=0.25, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.1),
        ]),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),
    SkillModel(
        'VPC', 3, parents=(AWS_SKILL, NETWORKING_SKILL), flexible_case=False, primary_category=DEV_OPS_SKILL,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=0.25, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.1),
        ]),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),
    SkillModel(
        'Route53', 3, parents=(AWS_SKILL, NETWORKING_SKILL), flexible_case=False, primary_category=DEV_OPS_SKILL,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=0.1, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.01),
        ]),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),
    SkillModel(
        'S3', 3, parents=(AWS_SKILL, DATABASE_SKILL), flexible_case=False, primary_category=DEV_OPS_SKILL,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=0.25, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.1),
        ]),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),
    SkillModel(
        'ElastiCache', 3, parents=(AWS_SKILL, DATABASE_SKILL), flexible_case=False, primary_category=DEV_OPS_SKILL,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=0.5, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.05),
        ]),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),
    SkillModel(
        'IAM', 3, parents=(AWS_SKILL, COLLABORATION_SKILL), flexible_case=False, primary_category=DEV_OPS_SKILL,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=0.25, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.01),
        ]),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),
    SkillModel(
        'CloudWatch', 3, parents=(AWS_SKILL, MONITORING_SKILL), flexible_case=False, primary_category=DEV_OPS_SKILL,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=0.25, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.1),
        ]),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),
    SkillModel(
        'CloudFormation', 2, parents=(AWS_SKILL, SERVER_ADMIN_SKILL, NETWORKING_SKILL), flexible_case=False,
        primary_category=DEV_OPS_SKILL,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=0.15, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.05),
        ]),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),
    SkillModel(
        'ECS', 3, parents=(AWS_SKILL, SERVER_ADMIN_SKILL), flexible_case=False, primary_category=DEV_OPS_SKILL,
        experience=SkillExperiences([
            SkillExperience('6/1/2020', hours_per_week=0.25, one_time_hours=20, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.1),
        ]),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),
    SkillModel(
        'CDK', 3, parents=(AWS_SKILL, SERVER_ADMIN_SKILL, NETWORKING_SKILL), flexible_case=False,
        primary_category=DEV_OPS_SKILL,
        experience=SkillExperiences([
            SkillExperience('6/1/2020', hours_per_week=0.1, one_time_hours=30, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.02),
        ]),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),

    SkillModel(
        'Nginx', 3, parents=(SERVER_ADMIN_SKILL,), flexible_case=False, primary_category=DEV_OPS_SKILL,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=0.25, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.05),
        ]),
        priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
    ),

    SkillModel(
        'JIRA', 4, parents=(WEB_DEVELOPMENT_SKILL, COLLABORATION_SKILL), flexible_case=False, primary_category=OTHER,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=2, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.5),
        ]),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 4, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),
    SkillModel(
        'PyCharm', 4, parents=(IDE_SKILL,), flexible_case=False, primary_category=PROGRAMMING_SKILL,
        experience=SkillExperiences([
            SkillExperience('1/1/2016', hours_per_week=20, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=5),
        ]),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 2})
    ),
    SkillModel(
        'VS Code', 4, parents=(IDE_SKILL,), flexible_case=False, primary_category=PROGRAMMING_SKILL,
        experience=SkillExperience('1/1/2019', hours_per_week=10),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 2})
    ),
    SkillModel(
        'IDEA', 4, parents=(IDE_SKILL,), flexible_case=False, primary_category=PROGRAMMING_SKILL,
        experience=SkillExperience(CARBON_BEGIN_DATE, hours_per_week=15),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 3, SpecificApplicationFocus.DATA_SCIENCE: 2})
    ),

    SkillModel(
        'empirical research', 5, parents=(RESEARCH_SKILL, STATISTICS_SKILL, DATA_ANALYSIS_SKILL, DATA_MUNGING_SKILL),
        primary_category=DATA_SCIENCE_SKILL,
        experience=SkillExperiences([
            SkillExperience('4/1/2012', hours_per_week=20, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=5),
        ]),
        priority=SkillFocusPriority(
            4,
            {
                SpecificApplicationFocus.DATA_SCIENCE: 5,
                SpecificApplicationFocus.ECONOMIST: 5,
                SpecificApplicationFocus.ASSET_MANAGER: 5,
                SpecificApplicationFocus.TECH_COMPANY: 5,
            }
        )
    ),

    SkillModel(
        'Github Actions', 4, parents=(CI_SKILL,), flexible_case=False, primary_category=DEV_OPS_SKILL,
        experience=SkillExperience('12/20/2019', hours_per_week=0.5),
        priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
    ),
    SkillModel(
        'Gitlab CI', 3, parents=(CI_SKILL,), flexible_case=False, primary_category=DEV_OPS_SKILL,
        experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=0.5, one_time_hours=75, end_date_inp=CARBON_BEGIN_DATE),
        priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
    ),

    SkillModel(
        'supervised learning', 3, parents=(MACHINE_LEARNING_SKILL,), primary_category=DATA_SCIENCE_SKILL,
        experience=SkillExperience('1/1/2016', hours_per_week=0.3),
        priority=SkillFocusPriority(
            3,
            {
                SpecificApplicationFocus.DATA_SCIENCE: 5,
                SpecificApplicationFocus.ECONOMIST: 4,
                SpecificApplicationFocus.TECH_COMPANY: 4
            }
        )
    ),
    SkillModel(
        'dimensionality reduction', 3, parents=(MACHINE_LEARNING_SKILL,), primary_category=DATA_SCIENCE_SKILL,
        experience=SkillExperience('1/1/2016', hours_per_week=0.1),
        priority=SkillFocusPriority(
            3,
            {
                SpecificApplicationFocus.DATA_SCIENCE: 5,
                SpecificApplicationFocus.ECONOMIST: 4,
                SpecificApplicationFocus.TECH_COMPANY: 4
            }
        )
    ),
    SkillModel(
        'deep learning', 2, parents=(MACHINE_LEARNING_SKILL,), primary_category=DATA_SCIENCE_SKILL,
        experience=SkillExperience('1/1/2016', hours_per_week=0.2),
        priority=SkillFocusPriority(
            3,
            {
                SpecificApplicationFocus.DATA_SCIENCE: 5,
                SpecificApplicationFocus.ECONOMIST: 4,
                SpecificApplicationFocus.TECH_COMPANY: 4
            }
        )
    ),

    SkillModel(
        'econometrics', 4, parents=(STATISTICS_SKILL,), primary_category=DATA_SCIENCE_SKILL,
        experience=SkillExperience(PROGRAMMING_BEGIN_DATE, hours_per_week=2),
        priority=SkillFocusPriority(
            4,
            {
                SpecificApplicationFocus.DATA_SCIENCE: 5,
                SpecificApplicationFocus.ECONOMIST: 5,
                SpecificApplicationFocus.TECH_COMPANY: 5,
            }
        )
    ),
    SkillModel(
        'project management', 4, primary_category=OTHER, priority=SkillFocusPriority(2)
    ),
    SkillModel(
        'Quality assurance', 3, primary_category=OTHER,
        experience=SkillExperiences([
            SkillExperience('2/1/2017', hours_per_week=3, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=1),
        ]),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 4})
    ),
    SkillModel(
        'HTML', 4, parents=(WEB_DEVELOPMENT_SKILL, FRONTEND_SKILL, TYPE_SETTING_SKILL), flexible_case=False,
        primary_category=PRESENTATION_SKILL,
        experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=2),
        priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 5, SpecificApplicationFocus.DATA_SCIENCE: 4})
    ),
    SkillModel(
        'Sass', 3, parents=(CSS_SKILL,), flexible_case=False, primary_category=FRAMEWORK_SKILL,
        experience=SkillExperience('6/1/2020', hours_per_week=1),
        priority=SkillFocusPriority(
            2,
            {
                SpecificApplicationFocus.TECH_COMPANY: 5,
                SpecificApplicationFocus.DATA_SCIENCE: 3
            }
        )
    ),
    SkillModel(
        'Bootstrap', 3, parents=(CSS_SKILL, JS_SKILL, FRAMEWORK_SKILL), flexible_case=False,
        primary_category=FRAMEWORK_SKILL,
        experience=SkillExperience('6/1/2020', hours_per_week=0.2, one_time_hours=60),
        priority=SkillFocusPriority(
            2,
            {
                SpecificApplicationFocus.TECH_COMPANY: 5,
                SpecificApplicationFocus.DATA_SCIENCE: 3
            }
        )
    ),
    SkillModel(
        'Material Design', 2, parents=(CSS_SKILL, JS_SKILL, FRAMEWORK_SKILL), flexible_case=False,
        primary_category=FRAMEWORK_SKILL,
        experience=SkillExperience('6/1/2020', hours_per_week=0.2, one_time_hours=10),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 4, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),
    SkillModel(
        'jQuery', 2, parents=(JS_SKILL, FRAMEWORK_SKILL), flexible_case=False, primary_category=FRAMEWORK_SKILL,
        experience=SkillExperience(CF_BEGIN_DATE, one_time_hours=25),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 4, SpecificApplicationFocus.DATA_SCIENCE: 3})
    ),

    SkillModel(
        'pandas', 5, parents=DS_FRAMEWORK_SKILLS + (DATA_ANALYSIS_SKILL, DATA_MUNGING_SKILL), flexible_case=False,
        experience=SkillExperiences([
            SkillExperience('5/1/2015', hours_per_week=5, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=1),
        ]),
        priority=SkillFocusPriority(
            4,
            {
                SpecificApplicationFocus.TECH_COMPANY: 5,
                SpecificApplicationFocus.DATA_SCIENCE: 5,
                SpecificApplicationFocus.ECONOMIST: 5
            }
        )
    ),
    SkillModel(
        'NumPy', 4, parents=DS_FRAMEWORK_SKILLS + (DATA_ANALYSIS_SKILL, DATA_MUNGING_SKILL), flexible_case=False,
        experience=SkillExperiences([
            SkillExperience('5/1/2015', hours_per_week=1, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.25),
        ]),
        priority=SkillFocusPriority(
            4,
            {
                SpecificApplicationFocus.TECH_COMPANY: 5,
                SpecificApplicationFocus.DATA_SCIENCE: 5,
                SpecificApplicationFocus.ECONOMIST: 5
            }
        )
    ),
    SkillModel(
        'SciPy', 3, parents=DS_FRAMEWORK_SKILLS + (DATA_ANALYSIS_SKILL,), flexible_case=False,
        experience=SkillExperiences([
            SkillExperience('5/1/2015', hours_per_week=0.25, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.05),
        ]),
        priority=SkillFocusPriority(
            4,
            {
                SpecificApplicationFocus.TECH_COMPANY: 4,
                SpecificApplicationFocus.DATA_SCIENCE: 5,
                SpecificApplicationFocus.ECONOMIST: 5
            }
        )
    ),
    SkillModel(
        'SymPy', 4, parents=DS_FRAMEWORK_SKILLS + (DATA_ANALYSIS_SKILL,), flexible_case=False,
        experience=SkillExperience('3/1/2016', hours_per_week=0.25),
        priority=SkillFocusPriority(
            3,
            {
                SpecificApplicationFocus.TECH_COMPANY: 4,
                SpecificApplicationFocus.DATA_SCIENCE: 4,
                SpecificApplicationFocus.ECONOMIST: 4
            }
        )
    ),
    SkillModel(
        'scikit-learn', 3, parents=DS_FRAMEWORK_SKILLS + (MACHINE_LEARNING_SKILL, DATA_ANALYSIS_SKILL),
        flexible_case=False,
        experience=SkillExperience('1/1/2016', hours_per_week=0.25),
        priority=SkillFocusPriority(
            3,
            {
                SpecificApplicationFocus.TECH_COMPANY: 5,
                SpecificApplicationFocus.DATA_SCIENCE: 5,
                SpecificApplicationFocus.ECONOMIST: 5
            }
        )
    ),
    SkillModel(
        'Jupyter', 4, parents=DS_FRAMEWORK_SKILLS + (IDE_SKILL,), flexible_case=False,
        experience=SkillExperience('3/1/2015', hours_per_week=5),
        priority=SkillFocusPriority(
            3,
            {
                SpecificApplicationFocus.TECH_COMPANY: 4,
                SpecificApplicationFocus.DATA_SCIENCE: 5,
                SpecificApplicationFocus.ECONOMIST: 4
            }
        )
    ),
    SkillModel(
        'Matplotlib', 4, parents=DS_FRAMEWORK_SKILLS + (PLOTTING_SKILL,), flexible_case=False,
        experience=SkillExperience('5/1/2015', hours_per_week=0.4),
        priority=SkillFocusPriority(
            3,
            {
                SpecificApplicationFocus.TECH_COMPANY: 4,
                SpecificApplicationFocus.DATA_SCIENCE: 5,
                SpecificApplicationFocus.ECONOMIST: 4
            }
        )
    ),
    SkillModel(
        'HoloViews', 3, parents=DS_FRAMEWORK_SKILLS + (PLOTTING_SKILL,), flexible_case=False,
        experience=SkillExperience('6/1/2019', hours_per_week=0.1),
        priority=SkillFocusPriority(
            2,
            {
                SpecificApplicationFocus.TECH_COMPANY: 3,
                SpecificApplicationFocus.DATA_SCIENCE: 3,
                SpecificApplicationFocus.ECONOMIST: 3
            }
        )
    ),
    SkillModel(
        'Google Charts', 3, parents=DS_FRAMEWORK_SKILLS + (PLOTTING_SKILL,), flexible_case=False,
        experience=SkillExperience('6/1/2020', hours_per_week=0.1, one_time_hours=30),
        priority=SkillFocusPriority(
            2,
            {
                SpecificApplicationFocus.TECH_COMPANY: 3,
                SpecificApplicationFocus.DATA_SCIENCE: 3,
                SpecificApplicationFocus.ECONOMIST: 3
            }
        )
    ),
    SkillModel(
        'Plotly', 3, parents=DS_FRAMEWORK_SKILLS + (PLOTTING_SKILL,), flexible_case=False,
        experience=SkillExperience('6/1/2020', hours_per_week=0.1, one_time_hours=30),
        priority=SkillFocusPriority(
            2,
            {
                SpecificApplicationFocus.TECH_COMPANY: 3,
                SpecificApplicationFocus.DATA_SCIENCE: 3,
                SpecificApplicationFocus.ECONOMIST: 3
            }
        )
    ),
    SkillModel(
        'Google Maps API', 3, parents=DS_FRAMEWORK_SKILLS + (PLOTTING_SKILL, GEOVISUALIZATION_SKILL),
        flexible_case=False,
        experience=SkillExperience('3/1/2020', hours_per_week=0.1, one_time_hours=100),
        priority=SkillFocusPriority(
            2,
            {
                SpecificApplicationFocus.TECH_COMPANY: 3,
                SpecificApplicationFocus.DATA_SCIENCE: 3,
                SpecificApplicationFocus.ECONOMIST: 3
            }
        )
    ),
    SkillModel(
        'GeoPandas', 4, parents=DS_FRAMEWORK_SKILLS + (DATA_ANALYSIS_SKILL, DATA_MUNGING_SKILL, GEOVISUALIZATION_SKILL),
        flexible_case=False,
        experience=SkillExperience('6/1/2020', hours_per_week=0.1, one_time_hours=30),
        priority=SkillFocusPriority(
            2,
            {
                SpecificApplicationFocus.TECH_COMPANY: 3,
                SpecificApplicationFocus.DATA_SCIENCE: 3,
                SpecificApplicationFocus.ECONOMIST: 3
            }
        )
    ),
    SkillModel(
        'Flask', 5, parents=BE_PYTHON_WEB_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=5, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0),
        ]),
        priority=SkillFocusPriority(
            4,
            {
                SpecificApplicationFocus.TECH_COMPANY: 5,
                SpecificApplicationFocus.DATA_SCIENCE: 5,
                SpecificApplicationFocus.ECONOMIST: 5
            }
        )
    ),
    SkillModel(
        'Django', 2, parents=BE_PYTHON_WEB_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=0.1, one_time_hours=20, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0),
        ]),
        priority=SkillFocusPriority(
            3,
            {
                SpecificApplicationFocus.TECH_COMPANY: 4,
                SpecificApplicationFocus.DATA_SCIENCE: 4,
                SpecificApplicationFocus.ECONOMIST: 4
            }
        )
    ),
    SkillModel(
        'SQLAlchemy', 5, parents=BE_PYTHON_WEB_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperiences([
            SkillExperience(CF_BEGIN_DATE, hours_per_week=5, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.5),
        ]),
        priority=SkillFocusPriority(
            4,
            {
                SpecificApplicationFocus.TECH_COMPANY: 5,
                SpecificApplicationFocus.DATA_SCIENCE: 5,
                SpecificApplicationFocus.ECONOMIST: 5
            }
        )
    ),
    SkillModel(
        'pydantic', 5, parents=BE_PYTHON_WEB_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperiences([
            SkillExperience('6/1/2019', hours_per_week=1, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.5),
        ]),
        priority=SkillFocusPriority(
            2,
            {
                SpecificApplicationFocus.TECH_COMPANY: 3,
            }
        )
    ),
    SkillModel(
        'FastAPI', 3, parents=BE_PYTHON_WEB_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperiences([
            SkillExperience('6/1/2020', hours_per_week=3, one_time_hours=30, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.5),
        ]),
        priority=SkillFocusPriority(
            3,
            {
                SpecificApplicationFocus.TECH_COMPANY: 4,
                SpecificApplicationFocus.DATA_SCIENCE: 4,
            }
        )
    ),
    SkillModel(
        'GraphQL', 3,
        parents=BE_PYTHON_WEB_FRAMEWORK_SKILLS + FE_TS_WEB_FRAMEWORK_SKILLS + (KOTLIN_SKILL, JAVA_SKILL),
        flexible_case=False,
        experience=SkillExperience(GRAPHQL_BEGIN_DATE, hours_per_week=10),
        priority=SkillFocusPriority(
            2,
            {
                SpecificApplicationFocus.TECH_COMPANY: 5,
                SpecificApplicationFocus.DATA_SCIENCE: 3,
            }
        )
    ),
    SkillModel(
        'Spring Boot', 2, parents=BE_JAVA_WEB_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperience(GRAPHQL_BEGIN_DATE, hours_per_week=1),
        priority=SkillFocusPriority(
            2,
            {
                SpecificApplicationFocus.TECH_COMPANY: 4,
            }
        )
    ),
    SkillModel(
        'DGS', 3, parents=BE_JAVA_WEB_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperience(GRAPHQL_BEGIN_DATE, hours_per_week=4),
        priority=SkillFocusPriority(
            2,
            {
                SpecificApplicationFocus.TECH_COMPANY: 3,
            }
        )
    ),
    SkillModel(
        'Detekt', 2, parents=(FRAMEWORK_SKILL, KOTLIN_SKILL,), flexible_case=False,
        experience=SkillExperience(GRAPHQL_BEGIN_DATE, hours_per_week=1),
        priority=SkillFocusPriority(
            1,
            {
                SpecificApplicationFocus.TECH_COMPANY: 2,
            }
        )
    ),
    SkillModel(
        'Celery', 4, parents=ASYNC_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperiences([
            SkillExperience('1/1/2018', hours_per_week=2, end_date_inp=CARBON_BEGIN_DATE),
            SkillExperience(CARBON_BEGIN_DATE, hours_per_week=0.2),
        ]),
        priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 4})
    ),
    SkillModel(
        'Uvicorn', 3, parents=BE_PYTHON_WEB_FRAMEWORK_SKILLS + ASYNC_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperience('6/1/2020', hours_per_week=0.1, one_time_hours=10),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3})
    ),

    SkillModel(
        'Requests', 4, parents=WEB_SCRAPING_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=0.5),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3})
    ),
    SkillModel(
        'Selenium', 4, parents=WEB_SCRAPING_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperience('9/1/2015', hours_per_week=1),
        priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 4})
    ),
    SkillModel(
        'Beautiful Soup', 2, parents=PARSING_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperience('9/1/2015', hours_per_week=0.25),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3})
    ),
    SkillModel(
        'lxml', 4, parents=PARSING_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperience('9/1/2015', hours_per_week=0.25),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3})
    ),

    SkillModel(
        'Panel', 4, parents=FULL_STACK_WEB_PYTHON_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperience('6/1/2020', hours_per_week=0.5, one_time_hours=100),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3})
    ),
    SkillModel(
        'Dash', 2, parents=FULL_STACK_WEB_PYTHON_FRAMEWORK_SKILLS, flexible_case=False,
        experience=SkillExperience('12/20/2019', hours_per_week=0, one_time_hours=30),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3})
    ),
    SkillModel(
        'Sphinx', 4, parents=FULL_STACK_WEB_PYTHON_FRAMEWORK_SKILLS + (DOCUMENTATION_SKILL,), flexible_case=False,
        experience=SkillExperience('6/1/2019', hours_per_week=0.5),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3})
    ),

    SkillModel(
        'Pelican', 3, parents=FULL_STACK_WEB_PYTHON_FRAMEWORK_SKILLS + (CMS_SKILL,), flexible_case=False,
        experience=SkillExperience('6/1/2019', hours_per_week=0, one_time_hours=30),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 2})
    ),
    SkillModel(
        'Wagtail', 2, parents=FULL_STACK_WEB_PYTHON_FRAMEWORK_SKILLS + (CMS_SKILL,), flexible_case=False,
        experience=SkillExperience('1/1/2018', hours_per_week=0.2, end_date_inp=CARBON_BEGIN_DATE),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 2})
    ),

    SkillModel(
        'Jinja2', 4, parents=(FRAMEWORK_SKILL, PYTHON_SKILL, TEMPLATING_SKILL), flexible_case=False,
        experience=SkillExperience(CF_BEGIN_DATE, hours_per_week=0.5),
        priority=SkillFocusPriority(2, {SpecificApplicationFocus.TECH_COMPANY: 3})
    ),
    SkillModel(
        'pytest', 4, parents=(FRAMEWORK_SKILL, PYTHON_SKILL, TESTING_SKILL), flexible_case=False,
        experience=SkillExperience('1/1/2018', hours_per_week=1),
        priority=SkillFocusPriority(3, {SpecificApplicationFocus.TECH_COMPANY: 4})
    ),

    SkillModel(
        'Grafana', 2, parents=(FRAMEWORK_SKILL, MONITORING_SKILL), flexible_case=False,
        experience=SkillExperience('1/1/2018', hours_per_week=0.1),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 2})
    ),
    SkillModel(
        'Prometheus', 2, parents=(FRAMEWORK_SKILL, MONITORING_SKILL, DATABASE_SKILL), flexible_case=False,
        experience=SkillExperience('1/1/2018', hours_per_week=0.1),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 2})
    ),

    SkillModel(
        'xlwings', 4, parents=(FRAMEWORK_SKILL, PYTHON_SKILL, EXCEL_SKILL, AUTOMATION_SKILL), flexible_case=False,
        experience=SkillExperience('8/1/2019', hours_per_week=0, one_time_hours=40),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 2, SpecificApplicationFocus.DATA_SCIENCE: 2})
    ),
    SkillModel(
        'fire', 3, parents=(FRAMEWORK_SKILL, PYTHON_SKILL, CLI_SKILL), flexible_case=False,
        experience=SkillExperience('1/1/2018', hours_per_week=0.1, end_date_inp='1/1/2020'),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 2})
    ),
    SkillModel(
        'typer', 3, parents=(FRAMEWORK_SKILL, PYTHON_SKILL, CLI_SKILL), flexible_case=False,
        experience=SkillExperience('1/1/2020', hours_per_week=0.1),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.TECH_COMPANY: 2})
    ),

    SkillModel(
        'Bloomberg terminal',
        2,
        case_capitalize_func=first_word_untouched_rest_capitalized,
        case_lower_func=first_word_untouched_rest_lower,
        case_title_func=first_word_untouched_rest_title,
        primary_category=OTHER,
        experience=SkillExperience('5/1/2011', hours_per_week=0, one_time_hours=40),
        priority=SkillFocusPriority(1, {SpecificApplicationFocus.ASSET_MANAGER: 4, ApplicationFocus.ACADEMIC: 3})
    )
]

_recursive_sort_skills(_SKILLS, key=lambda skill: skill.level, reverse=True)

SKILLS: Dict[str, SkillModel] = {skill.to_lower_case_str(): skill for skill in _SKILLS}

CV_RENAME_SKILLS: Dict[str, str] = {
    'asynchronous programming': 'Async. Programming',
    'open-source development': 'Open-Source',
    'back-end development': 'Back-end dev.',
    'front-end development': 'Front-end dev.',
    'distributed computing': 'Distrib. Computing',
    'application monitoring': 'App Monitoring',
    'dimensionality reduction': 'Dim. Reduction',
}

CV_EXCLUDE_SKILLS: List[str] = [
    'research',
]

CV_SKILL_SECTION_ORDER: List[str] = [
    'Programming',
    'Data Science',
    'Frameworks',
    'Dev-Ops',
    'Presentation',
    'Soft Skills',
    'Other'
]


def get_skills(exclude_skills: Optional[Sequence[str]] = None,
               exclude_skill_children: bool = True,
               order: Optional[Sequence[str]] = None,
               rename_skills: Optional[Dict[str, str]] = None,
               minimum_skill_priority: int = 1,
               focus: Optional[Union[ApplicationFocus, SpecificApplicationFocus]] = None,
               sort_attr: str = 'level', sort_reverse: bool = True) -> List[SkillModel]:
    if exclude_skills is None:
        exclude_skills = []
    if rename_skills is None:
        rename_skills = {}

    skills = [skill for key, skill in SKILLS.items() if key not in exclude_skills]

    # Check validity of sort_attr
    try:
        getattr(skills[0], sort_attr)
    except AttributeError:
        raise ValueError('must provide sort_attr which is a string of an attribute of SkillModel')

    _recursive_sort_skills(skills, key=lambda skill: getattr(skill, sort_attr), reverse=sort_reverse)

    if not exclude_skill_children:
        use_skills = skills
    else:
        child_excluded_skills: Set[SkillModel] = set()
        for skill_name in exclude_skills:
            skill = SKILLS[skill_name]
            children = cast(Set[SkillModel], skill.get_nested_children())
            child_excluded_skills.update(children)
        child_excluded_skill_names = {child.to_lower_case_str() for child in child_excluded_skills}
        use_skills = [skill for skill in skills if skill.to_lower_case_str() not in child_excluded_skill_names]

    if rename_skills:
        new_use_skills: List[SkillModel] = []
        for skill in use_skills:
            if skill.to_lower_case_str() in rename_skills:
                new_skill = deepcopy(skill)
                new_skill.title = rename_skills[skill.to_lower_case_str()]
                new_use_skills.append(new_skill)
            else:
                new_use_skills.append(skill)
        use_skills = new_use_skills

    if order is not None:
        if sort_reverse:
            op = operator.sub
        else:
            op = operator.add
        _recursive_sort_skills(
            use_skills,
            key=lambda skill: order.index(skill.to_lower_case_str())
            if skill.to_lower_case_str() in order else op(100000, getattr(skill, sort_attr))  # type: ignore
        )

    use_skills = [skill for skill in use_skills if skill.priority.get_level(focus) >= minimum_skill_priority]

    return use_skills


def get_skills_str_list(exclude_skills: Optional[Sequence[str]] = None, exclude_skill_children: bool = True,
                   order: Optional[Sequence[str]] = None) -> List[str]:
    skills = get_skills(
        exclude_skills=exclude_skills,
        exclude_skill_children=exclude_skill_children,
        order=order
    )
    formatted_skills = [skills[0].to_capitalized_str()] + [skill.to_lower_case_str() for skill in skills[1:]]
    joined = join_with_commas_and_and_output_list(formatted_skills)
    return joined
