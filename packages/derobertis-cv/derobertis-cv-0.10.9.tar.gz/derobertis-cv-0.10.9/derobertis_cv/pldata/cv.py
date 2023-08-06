from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import List, Sequence, Optional, Union, Dict, Callable

import pyexlatex as pl
import pyexlatex.resume as lr
import pyexlatex.graphics as lg
from pyexlatex.models.format.text.linespacing import LineSpacing
from pyexlatex.models.item import ItemBase
from pyexlatex.models.lists.item import ListItem
from pyexlatex.models.page.header import remove_header
from pyexlatex.models.page.style import PageStyle, ThisPageStyle
from pyexlatex.typing import PyexlatexItems, PyexlatexItem

from derobertis_cv.plbuild.paths import images_path, DOCUMENTS_BUILD_PATH
from derobertis_cv.pldata.constants.contact import STYLED_SITE, NAME, EMAIL, PHONE
from derobertis_cv.pldata.cover_letters.models import ApplicationFocus, SpecificApplicationFocus
from derobertis_cv.pldata.employment_model import JobIDs
from derobertis_cv.pldata.jobs import (
    get_professional_jobs,
    get_academic_jobs, CV_JOB_MODIFIERS, CV_EXCLUDED_COMPANIES
)
from derobertis_cv.pldata.education import get_education
from derobertis_cv.pldata.papers import (
    get_working_papers,
    get_works_in_progress, ResearchProjectModel
)
from derobertis_cv.pldata.skills import get_skills, get_skills_str_list, CV_RENAME_SKILLS, CV_EXCLUDE_SKILLS, \
    CV_SKILL_SECTION_ORDER
from derobertis_cv.pldata.software import get_software_projects
from derobertis_cv.pldata.awards import get_awards
from derobertis_cv.pldata.interests import get_research_interests
from derobertis_cv.pldata.references import get_references
from derobertis_cv.pldata.constants import contact
from derobertis_cv.pldata.software.config import ACADEMIC_INCLUDED_SOFTWARE_PROJECTS, EXCLUDED_SOFTWARE_PROJECTS, \
    PROFESSIONAL_SOFTWARE_PROJECT_ORDER
from derobertis_cv.pltemplates.application_info import ApplicationInfoSection
from derobertis_cv.pltemplates.skills.section import SkillsSection
from derobertis_cv.pltemplates.software.section import SoftwareSection


class ResumeSection(Enum):
    RESEARCH_INTERESTS = 'research interests'
    EDUCATION = 'education'
    ACADEMIC_EXPERIENCE = 'academic experience'
    PROFESSIONAL_EXPERIENCE = 'professional experience'
    COMBINED_EXPERIENCE = 'combined experience'
    WORKING_PAPERS = 'working papers'
    WORKS_IN_PROGRESS = 'works in progress'
    AWARDS_GRANTS = 'awards and grants'
    SOFTWARE_PROJECTS = 'software projects'
    REFERENCES = 'references'
    SKILLS = 'skills'
    OVERVIEW = 'overview'
    SELF_IMAGE = 'self image'
    COMPACT_PROJECTS = 'compact projects'
    CONTINUED = 'continued'
    APPLICATION_INFO = 'application info'


@dataclass
class CVModel:
    sections: List[Union[ResumeSection, ItemBase]]
    font_scale: Optional[float] = None
    line_spacing: Optional[float] = None
    include_website_in_contact_lines: bool = False
    file_name: str = 'Nick DeRobertis CV'
    included_software_projects: Optional[Sequence[str]] = None
    excluded_software_projects: Optional[Sequence[str]] = None
    software_project_order: Optional[Sequence[str]] = None
    excluded_companies: Optional[Sequence[str]] = None
    exclude_skills: Optional[Sequence[str]] = None
    exclude_skill_children: bool = False
    skill_order: Optional[Sequence[str]] = None
    skill_section_order: Optional[Sequence[str]] = None
    rename_skills: Optional[Dict[str, str]] = None
    skill_font_scale: Optional[float] = 0.85
    skills_per_row: int = 4
    exclude_skill_sections: Optional[Sequence[str]] = None
    reassign_skill_sections: Optional[Dict[str, str]] = None
    skill_sort_attr: str = 'experience_level'
    skill_sort_reverse: bool = True
    professional_section_name: str = 'Professional Experience'
    overview_text: str = (
        'A PhD finance researcher, full-stack web engineer and architect, data scientist, '
        'project manager, and entrepreneur with a track record of building, deploying, and managing open- and '
        'closed-source applications and research projects.'
    )
    include_private_jobs: bool = False
    include_working_paper_descriptions: bool = True
    include_wip_descriptions: bool = False
    modify_job_descriptions: Optional[Dict[JobIDs, Callable[[Sequence[str]], Sequence[str]]]] = None
    application_info: Optional[Dict[str, str]] = None
    custom_research_interests: Optional[List[str]] = None
    include_hours_per_week: bool = False
    minimum_skill_priority: int = 1
    application_focus: Optional[ApplicationFocus] = None
    specific_application_focus: Optional[SpecificApplicationFocus] = None
    custom_contact_lines_func: Optional[Callable[[bool], PyexlatexItems]] = None
    include_footer: bool = True

    def __post_init__(self):
        if self.software_project_order is None and self.included_software_projects is not None:
            self.software_project_order = self.included_software_projects
        self._validate()

    def _validate(self):
        if self.included_software_projects is not None and self.excluded_software_projects is not None:
            raise ValueError('cannot have both included and excluded software projects')

    @property
    def focus(self) -> Optional[Union[ApplicationFocus, SpecificApplicationFocus]]:
        if self.specific_application_focus is not None:
            return self.specific_application_focus
        if self.application_focus is not None:
            return self.application_focus
        return None

    @property
    def contact_lines_func(self) -> Callable[[bool], PyexlatexItems]:
        if self.custom_contact_lines_func is not None:
            return self.custom_contact_lines_func
        return get_cv_contact_lines

    def to_pyexlatex_resume(self) -> lr.Resume:
        contents = get_cv_contents(self)
        resume = lr.Resume(
            contents,
            contact_lines=self.contact_lines_func(self.include_website_in_contact_lines),
            packages=get_cv_packages(font_scale=self.font_scale, line_spacing=self.line_spacing),
            pre_env_contents=get_cv_pre_env_contents(font_scale=self.font_scale, include_footer=self.include_footer),
            authors=['Nick DeRobertis'],
        )
        return resume

    def output(self, outfolder: str = DOCUMENTS_BUILD_PATH) -> lr.Resume:
        resume = self.to_pyexlatex_resume()
        resume.to_pdf(outfolder, outname=self.file_name)
        return resume


def get_cv_contents(model: CVModel, include_self_image: bool = True) -> List[ItemBase]:
    prof_jobs = get_professional_jobs(
        excluded_companies=model.excluded_companies,
        include_private=model.include_private_jobs,
        modify_descriptions=model.modify_job_descriptions,
    )
    academic_jobs = get_academic_jobs(
        excluded_companies=model.excluded_companies,
        modify_descriptions=model.modify_job_descriptions,
    )
    all_jobs = prof_jobs + academic_jobs  # type: ignore
    all_jobs.sort(key=lambda job: job.begin_date, reverse=True)

    lr_prof_jobs = [
        job.to_pyexlatex_employment(include_hours_per_week=model.include_hours_per_week) for job in prof_jobs
    ]
    lr_academic_jobs = [
        job.to_pyexlatex_employment(include_hours_per_week=model.include_hours_per_week) for job in academic_jobs
    ]
    lr_all_jobs = [
        job.to_pyexlatex_employment(include_hours_per_week=model.include_hours_per_week) for job in all_jobs
    ]
    lr_education = [edu.to_pyexlatex() for edu in get_education()]

    software_projects = get_software_projects(
        include_projects=model.included_software_projects,
        exclude_projects=model.excluded_software_projects,
        order=model.software_project_order,
    )
    working_papers = get_working_papers()
    wip = get_works_in_progress()
    all_research = working_papers + wip

    research_interests = get_research_interests(interests=model.custom_research_interests)

    all_contents = {
        ResumeSection.RESEARCH_INTERESTS: pl.Section(
            research_interests,
            title='Research Interests'
        ),
        ResumeSection.EDUCATION: lr.SpacedSection(
            lr_education,
            title='Education'
        ),
        ResumeSection.ACADEMIC_EXPERIENCE: pl.Section(
            [pl.VSpace(0.2)] + lr_academic_jobs,
            title='Academic Experience'
        ),
        ResumeSection.PROFESSIONAL_EXPERIENCE: pl.Section(
            [pl.VSpace(0.2)] + lr_prof_jobs,
            title=model.professional_section_name
        ),
        ResumeSection.COMBINED_EXPERIENCE: pl.Section(
            [pl.VSpace(0.2)] + lr_all_jobs,
            title=model.professional_section_name
        ),
        ResumeSection.WORKING_PAPERS: lr.SpacedSection(
            ResearchProjectModel.list_to_pyexlatex_publication_list(
                get_working_papers(),
                include_descriptions=model.include_working_paper_descriptions,
            ),
            title='Working Papers'
        ),
        ResumeSection.WORKS_IN_PROGRESS: lr.SpacedSection(
            ResearchProjectModel.list_to_pyexlatex_publication_list(
                get_works_in_progress(),
                include_descriptions=model.include_wip_descriptions,
            ),
            title='Works in Progress'
        ),
        ResumeSection.AWARDS_GRANTS: lr.SpacedSection(
            [award.to_pyexlatex_award() for award in get_awards()],
            title='Awards and Grants'
        ),
        ResumeSection.SOFTWARE_PROJECTS: SoftwareSection(
            software_projects,
            title='Software Projects',
            compact=True
        ),
        ResumeSection.REFERENCES: lr.SpacedSection(
            [
                pl.TextSize(-1),
                get_references(),
            ],
            title='References',
            num_cols=2
        ),
        ResumeSection.SKILLS: SkillsSection(
            get_skills(
                exclude_skills=model.exclude_skills,
                exclude_skill_children=model.exclude_skill_children,
                order=model.skill_order,
                rename_skills=model.rename_skills,
                minimum_skill_priority=model.minimum_skill_priority,
                focus=model.focus,
                sort_attr=model.skill_sort_attr,
                sort_reverse=model.skill_sort_reverse,
            ),
            section_order=model.skill_section_order,
            font_scale=model.skill_font_scale,
            skills_per_row=model.skills_per_row,
            exclude_sections=model.exclude_skill_sections,
            reassign_sections=model.reassign_skill_sections,
        ),
        ResumeSection.OVERVIEW: pl.Section(
            model.overview_text,
            title='Overview'
        ),
        ResumeSection.SELF_IMAGE: [
            pl.Raw(r'\vspace*{-3cm}\vbox{\hspace{13.9cm} \href{https://nickderobertis.com}{\includegraphics[width=3.85cm, height=4cm]{' + images_path('nick-derobertis.png') + '}}}'),
            pl.Raw(r'\hspace{13.3cm} \parbox[r]{5cm}{\centering See more at ' + STYLED_SITE + '}'),
            pl.VSpace(-0.6),
        ],
        ResumeSection.COMPACT_PROJECTS: pl.Section(
            [
                [
                    pl.Bold(f'{len(software_projects)} open-source software projects'),
                    pl.Hyperlink(
                        contact.SOFTWARE_URL,
                        pl.Bold(
                            pl.TextColor(
                                f'({contact.SOFTWARE_URL})',
                                color='darkblue'
                            )
                        )
                    ),
                    pl.Raw(r'\begin{list}{$\cdot$}{\leftmargin=1em} \itemsep -0.5em \vspace{-0.5em}'),
                    ListItem(
                        'I create primarily Python packages which automate workflows for empirical researchers '
                        'and financial modelers including data collection and pipelines, management and '
                        'presentation of results, and high-level analyses',
                    ),
                    pl.Raw(r'\end{list}'),
                ],
                pl.VSpace(-0.15),
                [
                    pl.Bold(f'{len(all_research)} research projects'),
                    pl.Hyperlink(
                        contact.RESEARCH_URL,
                        pl.Bold(
                            pl.TextColor(
                                f'({contact.RESEARCH_URL})',
                                color='darkblue'
                            )
                        )
                    ),
                    pl.Raw(r'\begin{list}{$\cdot$}{\leftmargin=1em} \itemsep -0.5em \vspace{-0.5em}'),
                    ListItem([
                        [f'Research areas:', research_interests]
                    ]),
                    pl.Raw(r'\end{list}'),
                ],
            ],
            title='Other Project Experience'
        ),
        ResumeSection.CONTINUED: [
            pl.VFill(),
            pl.Center('(continued on next page)'),
            pl.VFill(),
        ]
    }

    if model.application_info is not None:
        all_contents[ResumeSection.APPLICATION_INFO] = ApplicationInfoSection(model.application_info)
    else:
        all_contents[ResumeSection.APPLICATION_INFO] = None

    selected_contents = [
        ThisPageStyle('empty'),
    ]

    for section in model.sections:
        if isinstance(section, ResumeSection):
            cont = all_contents[section]
            if cont is not None:
                selected_contents.append(cont)
        else:
            selected_contents.append(section)

    return selected_contents


def get_cv_pre_env_contents(font_scale: Optional[float] = None, include_footer: bool = True) -> PyexlatexItems:
    pe_contents: List[PyexlatexItem] = [
        pl.Raw(r'\definecolor{darkblue}{RGB}{50,82,209}'),
        PageStyle("fancyplain"),
        remove_header,
        pl.CenterFooter(''),
    ]

    if include_footer:
        diamond = pl.Raw(r' $\diamond$ ')
        footer_parts = [NAME, EMAIL, PHONE, STYLED_SITE]
        footer = str(diamond).join([str(p) for p in footer_parts])
        pe_contents.extend([
            pl.LeftFooter(footer),
            pl.RightFooter(pl.ThisPageNumber()),
            pl.FooterLine()
        ])

    if font_scale is not None:
        font_str = (
                r'\setmainfont{Latin Modern Roman}[Scale =' +
                str(font_scale) +
                ',Ligatures = {Common, TeX}]'
        )
        font_resize = pl.Raw(font_str)
        pe_contents.append(font_resize)
        return pe_contents


def get_cv_packages(font_scale: Optional[float] = None, line_spacing: Optional[float] = None) -> PyexlatexItems:
    packages: List[PyexlatexItem] = [
        'graphicx', 'fancyhdr', 'xcolor', 'fontspec', pl.Package('hyperref', modifier_str='hidelinks')
    ]

    if line_spacing is not None:
        packages.extend([
            'setspace',
            LineSpacing(line_spacing)
        ])

    return packages


def get_cv_contact_lines(include_website: bool = False) -> PyexlatexItems:
    line_2: List[PyexlatexItem] = [contact.PHONE]
    if include_website:
        line_2.append(STYLED_SITE)
    lines = [[contact.EMAIL], line_2]
    return lines


class CVTypes(str, Enum):
    ACADEMIC = 'academic'
    HYBRID = 'hybrid'
    PROFESSIONAL = 'professional'
    PROFESSIONAL_RESUME = 'professional resume'
    PROFESSIONAL_RESUME_TECH_COMPANY = 'professional resume tech company'
    PROFESSIONAL_RESUME_ASSET_MANAGER = 'professional resume asset manager'
    PROFESSIONAL_RESUME_DATA_SCIENCE = 'professional resume data science'
    PROFESSIONAL_RESUME_BANK = 'professional resume bank'
    PROFESSIONAL_RESUME_ECONOMIST = 'professional resume economist'

ACADEMIC_SECTIONS = [
    ResumeSection.SELF_IMAGE,
    ResumeSection.APPLICATION_INFO,
    ResumeSection.RESEARCH_INTERESTS,
    pl.VSpace(0.2),
    ResumeSection.EDUCATION,
    pl.VSpace(0.2),
    ResumeSection.ACADEMIC_EXPERIENCE,
    ResumeSection.PROFESSIONAL_EXPERIENCE,
    ResumeSection.WORKING_PAPERS,
    pl.VSpace(0.2),
    ResumeSection.WORKS_IN_PROGRESS,
    pl.VSpace(0.2),
    ResumeSection.AWARDS_GRANTS,
    pl.VSpace(0.4),
    ResumeSection.SOFTWARE_PROJECTS,
    ResumeSection.REFERENCES
]

HYBRID_SECTIONS = [
    ResumeSection.APPLICATION_INFO,
    ResumeSection.RESEARCH_INTERESTS,
    pl.VSpace(0.2),
    ResumeSection.EDUCATION,
    pl.VSpace(0.2),
    ResumeSection.ACADEMIC_EXPERIENCE,
    ResumeSection.PROFESSIONAL_EXPERIENCE,
    pl.VSpace(0.2),
    ResumeSection.AWARDS_GRANTS,
    ResumeSection.CONTINUED,
    pl.PageBreak(),
    ResumeSection.SKILLS,
    pl.PageBreak(),
    ResumeSection.WORKING_PAPERS,
    pl.VSpace(0.2),
    ResumeSection.WORKS_IN_PROGRESS,
    pl.VSpace(0.2),
    ResumeSection.SOFTWARE_PROJECTS,
    ResumeSection.REFERENCES,
]

PROFESSIONAL_SECTIONS = [
    ResumeSection.APPLICATION_INFO,
    ResumeSection.OVERVIEW,
    pl.VSpace(0.2),
    ResumeSection.EDUCATION,
    pl.VSpace(0.2),
    ResumeSection.PROFESSIONAL_EXPERIENCE,
    ResumeSection.ACADEMIC_EXPERIENCE,
    pl.PageBreak(),
    ResumeSection.SKILLS,
    pl.PageBreak(),
    ResumeSection.WORKING_PAPERS,
    pl.VSpace(0.2),
    ResumeSection.WORKS_IN_PROGRESS,
    pl.VSpace(0.2),
    ResumeSection.AWARDS_GRANTS,
    pl.VSpace(0.4),
    ResumeSection.SOFTWARE_PROJECTS,
    ResumeSection.REFERENCES,
]

PROFESSIONAL_RESUME_SECTIONS = [
    ResumeSection.APPLICATION_INFO,
    ResumeSection.OVERVIEW,
    ResumeSection.COMBINED_EXPERIENCE,
    pl.VSpace(-0.25),
    ResumeSection.COMPACT_PROJECTS,
    pl.VSpace(-0.15),
    ResumeSection.EDUCATION,
    pl.VSpace(-0.1),
    ResumeSection.SKILLS,
]

CV_MODELS: Dict[CVTypes, CVModel] = {
    CVTypes.ACADEMIC: CVModel(
        ACADEMIC_SECTIONS,
        included_software_projects=ACADEMIC_INCLUDED_SOFTWARE_PROJECTS,
        professional_section_name='Other Professional Experience',
        modify_job_descriptions=CV_JOB_MODIFIERS,
        excluded_companies=CV_EXCLUDED_COMPANIES,
        application_focus=ApplicationFocus.ACADEMIC,
    ),
    CVTypes.HYBRID: CVModel(
        HYBRID_SECTIONS,
        file_name='Nick DeRobertis Hybrid CV',
        include_website_in_contact_lines=True,
        excluded_software_projects=EXCLUDED_SOFTWARE_PROJECTS,
        software_project_order=PROFESSIONAL_SOFTWARE_PROJECT_ORDER,
        rename_skills=CV_RENAME_SKILLS,
        exclude_skills=CV_EXCLUDE_SKILLS,
        skill_section_order=CV_SKILL_SECTION_ORDER,
        modify_job_descriptions=CV_JOB_MODIFIERS,
        excluded_companies=CV_EXCLUDED_COMPANIES,
        application_focus=ApplicationFocus.GOVERNMENT,
    ),
    CVTypes.PROFESSIONAL: CVModel(
        PROFESSIONAL_SECTIONS,
        file_name='Nick DeRobertis Professional CV',
        include_website_in_contact_lines=True,
        excluded_software_projects=EXCLUDED_SOFTWARE_PROJECTS,
        software_project_order=PROFESSIONAL_SOFTWARE_PROJECT_ORDER,
        include_private_jobs=True,
        rename_skills=CV_RENAME_SKILLS,
        exclude_skills=CV_EXCLUDE_SKILLS,
        skill_section_order=CV_SKILL_SECTION_ORDER,
        include_working_paper_descriptions=False,
        modify_job_descriptions=CV_JOB_MODIFIERS,
        excluded_companies=CV_EXCLUDED_COMPANIES,
        application_focus=ApplicationFocus.INDUSTRY,
    ),
    CVTypes.PROFESSIONAL_RESUME: CVModel(
        PROFESSIONAL_RESUME_SECTIONS,
        file_name='Nick DeRobertis Professional Resume',
        include_website_in_contact_lines=True,
        font_scale=0.8,
        line_spacing=0.9,
        excluded_software_projects=EXCLUDED_SOFTWARE_PROJECTS,
        software_project_order=PROFESSIONAL_SOFTWARE_PROJECT_ORDER,
        include_private_jobs=True,
        rename_skills=CV_RENAME_SKILLS,
        exclude_skills=CV_EXCLUDE_SKILLS,
        skill_section_order=CV_SKILL_SECTION_ORDER,
        include_working_paper_descriptions=False,
        modify_job_descriptions=CV_JOB_MODIFIERS,
        excluded_companies=CV_EXCLUDED_COMPANIES + [JobIDs.VCU_GA],
        professional_section_name='Selected Experience',
        application_focus=ApplicationFocus.INDUSTRY,
        minimum_skill_priority=3,
        exclude_skill_sections=('Other', 'Soft Skills', 'Presentation'),
        reassign_skill_sections={
            'CSS': 'Programming',
            'LaTeX': 'Programming',
            'HTML': 'Programming',
        },
        include_footer=False,
    )
}
for specific_focus in SpecificApplicationFocus.get_specific_resume_types():
    cv_type = SpecificApplicationFocus.get_resume_type(specific_focus)
    resume = deepcopy(CV_MODELS[CVTypes.PROFESSIONAL_RESUME])
    resume.specific_application_focus = specific_focus
    resume.file_name = f'{resume.file_name} {specific_focus.value.title()}'
    modifier_func = SpecificApplicationFocus.get_resume_modifier_func(specific_focus)
    if modifier_func is not None:
        resume = modifier_func(resume)
    CV_MODELS[cv_type] = resume


CV_MODELS_TUP: Sequence[CVModel] = tuple(CV_MODELS.values())


def get_custom_cv_model(cv_type: CVTypes, modifier_func: Callable[[CVModel], CVModel]) -> CVModel:
    cv_model = deepcopy(CV_MODELS[cv_type])
    modified = modifier_func(cv_model)
    return modified


def build_cvs(cv_models: Sequence[CVModel] = CV_MODELS_TUP, outfolder: str = DOCUMENTS_BUILD_PATH):
    for mod in cv_models:
        print(f'Building {mod.file_name}')
        mod.output(outfolder)


def build_cv_by_cv_type(cv_type: CVTypes, cv_models: Optional[Dict[CVTypes, CVModel]] = None, outfolder: str = DOCUMENTS_BUILD_PATH):
    if cv_models is None:
        cv_models = CV_MODELS

    try:
        mod = cv_models[cv_type]
    except KeyError:
        raise ValueError(f'no such cv type {cv_type}. Pass one of {[t.value for t in CVTypes]}')

    print(f'Building {mod.file_name}')
    mod.output(outfolder)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', required=False, default=None, type=str, help="CVType of CV to build")
    args = parser.parse_args()
    if args.type is not None:
        build_cv_by_cv_type(args.type)
    else:
        build_cvs()