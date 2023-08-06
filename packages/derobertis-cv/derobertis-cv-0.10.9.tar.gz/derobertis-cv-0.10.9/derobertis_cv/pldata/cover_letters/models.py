from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence, List, Optional, Union, Dict, Callable, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from derobertis_cv.pldata.cv import CVModel, CVTypes

import inflect
from pyexlatex.logic.builder import build
from pyexlatex.logic.format.and_join import join_with_commas_and_and
from pyexlatex.models.format.text.linespacing import LineSpacing
from pyexlatex.typing import PyexlatexItems, PyexlatexItem
import pyexlatex as pl

from derobertis_cv.models.organization import Organization, OrganizationCharacteristics
from derobertis_cv.plbuild.paths import DOCUMENTS_BUILD_PATH, images_path
from derobertis_cv.pldata.authors import Author, AUTHORS
from derobertis_cv.pldata.constants.authors import ANDY, NIMAL, BAOLIAN
from derobertis_cv.pldata.constants.contact import SITE_URL, EMAIL, PHONE, ADDRESS_LINES, NAME, FIRST_NAME
from derobertis_cv.pldata.courses.fin_model import get_fin_model_course


class ApplicationComponents(str, Enum):
    CV = 'CV'
    JOB_MARKET_PAPER = 'Job market paper'
    GOVERNMENT_INTERVENTION_PAPER = 'Government intervention paper'
    INVESTOR_ATTENTION_PAPER = 'Investor attention paper'
    OPIN_PAPER = 'OPIN paper'
    OTHER_RESEARCH = 'Other research work'
    RESEARCH_STATEMENT = 'Research statement'
    RESEARCH_LIST = 'List of research'
    TEACHING_STATEMENT = 'Teaching statement'
    COURSE_OUTLINES = 'Course outlines'
    TRANSCRIPTS = 'Graduate transcripts'
    EVALUATIONS = 'Teaching evaluations'
    DIVERSITY = 'Diversity statement'
    COVER_LETTER = 'Cover Letter'
    REFERENCES = 'References'
    ALL = 'all'
    EMAIL_BODY = 'email body'
    COVER_LETTER_AS_EMAIL = 'cover letter email'
    PERSONAL_WEBSITE = 'Personal Website'
    JMP_VIDEO = 'Job market paper video'
    APPLICATION = 'Application form'
    CODING_SAMPLE = 'Coding sample'
    SKILLS_LIST = 'Skills list'
    RESEARCH_COVER = 'Research cover'
    TEACHING_COVER = 'Teaching cover'
    TEACHING_EXPERIENCE_OVERVIEW = 'Teaching overview'
    PASSPORT_PHOTO = 'Photo of passport'

    @staticmethod
    def aggregate(components: Sequence['ApplicationComponents'],
                  exclude_components: Optional[Sequence['ApplicationComponents']] = None) -> List['ApplicationComponents']:
        if exclude_components is None:
            exclude_components = (
                ApplicationComponents.REFERENCES,
                ApplicationComponents.PERSONAL_WEBSITE,
                ApplicationComponents.SKILLS_LIST,
                ApplicationComponents.RESEARCH_COVER,
                ApplicationComponents.TEACHING_COVER,
            )

        out_comps: List['ApplicationComponents'] = []
        for comp in components:
            if comp in OTHER_RESEARCH_COMPONENTS:
                if ApplicationComponents.OTHER_RESEARCH not in out_comps:
                    out_comps.append(ApplicationComponents.OTHER_RESEARCH)
            elif comp in exclude_components:
                continue
            else:
                out_comps.append(comp)
        return out_comps


OTHER_RESEARCH_COMPONENTS = [
    ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER,
    ApplicationComponents.OPIN_PAPER,
    ApplicationComponents.INVESTOR_ATTENTION_PAPER
]

RESEARCH_COMPONENTS = [
    ApplicationComponents.JOB_MARKET_PAPER,
    *OTHER_RESEARCH_COMPONENTS,
]

BLUE = pl.RGB(50, 82, 209, color_name="darkblue")


class ApplicationFocus(str, Enum):
    ACADEMIC = 'academic'
    GOVERNMENT = 'government'
    SEMI_ACADEMIC = 'semi-academic'
    INDUSTRY = 'industry'


class SpecificApplicationFocus(str, Enum):
    BANKING_REGULATOR = 'banking regulator'
    OTHER_FINANCIAL_REGULATOR = 'other financial regulator'
    TECH_COMPANY = 'tech company'
    ASSET_MANAGER = 'asset management company'
    DATA_SCIENCE = 'data science'
    BANK = 'bank'
    ECONOMIST = 'economist'

    @classmethod
    def get_specific_resume_types(cls) -> Sequence['SpecificApplicationFocus']:
        return cls.TECH_COMPANY, cls.ASSET_MANAGER, cls.DATA_SCIENCE, cls.BANK, cls.ECONOMIST

    @classmethod
    def get_resume_type(cls, focus: 'SpecificApplicationFocus') -> 'CVTypes':
        from derobertis_cv.pldata.cv import CVTypes
        type_map: Dict['SpecificApplicationFocus', CVTypes] = {
            cls.TECH_COMPANY: CVTypes.PROFESSIONAL_RESUME_TECH_COMPANY,
            cls.ASSET_MANAGER: CVTypes.PROFESSIONAL_RESUME_ASSET_MANAGER,
            cls.DATA_SCIENCE: CVTypes.PROFESSIONAL_RESUME_DATA_SCIENCE,
            cls.BANK: CVTypes.PROFESSIONAL_RESUME_BANK,
            cls.ECONOMIST: CVTypes.PROFESSIONAL_RESUME_ECONOMIST,
        }
        try:
            return type_map[focus]
        except AttributeError:
            raise ValueError(f'specific focus {focus} does not have a corresponding CVType')

    @classmethod
    def get_resume_modifier_func(cls, focus: 'SpecificApplicationFocus') -> Optional[Callable[['CVModel'], 'CVModel']]:
        def set_skill_priority_to_4(model: 'CVModel') -> 'CVModel':
            model.minimum_skill_priority = 4
            return model

        # TODO [#52]: find better location for general cv modifier funcs
        def tech_company_resume(model: 'CVModel') -> 'CVModel':
            model.minimum_skill_priority = 5
            model.font_scale = 0.9
            model.line_spacing = 1.025
            return model

        func_map: Dict['SpecificApplicationFocus', Callable[['CVModel'], 'CVModel']] = {
            cls.TECH_COMPANY: tech_company_resume,
            cls.DATA_SCIENCE: set_skill_priority_to_4,
            cls.ECONOMIST: set_skill_priority_to_4,
        }
        return func_map.get(focus, None)


@dataclass
class SkillFocusPriority:
    default_level: int
    specific_levels: Dict[Union[SpecificApplicationFocus, ApplicationFocus], int] = field(default_factory=lambda: {})

    @property
    def levels(self) -> Dict[Union[SpecificApplicationFocus, ApplicationFocus], int]:
        return {focus: self.get_level(focus) for focus in [*SpecificApplicationFocus, *ApplicationFocus]}

    def get_level(self, focus: Optional[Union[SpecificApplicationFocus, ApplicationFocus]] = None):
        if focus is None:
            return self.default_level
        return self.specific_levels.get(focus, self.default_level)

    def __eq__(self, other):
        try:
            return all([
                self.default_level == other.default_level,
                self.specific_levels == other.specific_levels
            ])
        except AttributeError:
            return False

    def __hash__(self):
        level_tups = tuple(self.specific_levels.items())
        all_tup = (
            self.default_level,
            level_tups
        )
        return hash(all_tup)


class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


@dataclass
class HiringManager:
    last_name: str
    first_name: Optional[str] = None
    gender: Optional[Gender] = None
    title: Optional[str] = None
    is_doctor: bool = False
    married: bool = False
    is_person: bool = True
    
    @property
    def prefix(self) -> str:
        if not self.is_person:
            return ''
        if self.is_doctor:
            return 'Dr. '
        if self.gender == Gender.MALE:
            return f'Mr. '
        if self.gender == Gender.FEMALE:
            if self.married:
                return f'Mrs. '
            else:
                return f'Ms. '
        return ''

    @property
    def salutation_name(self) -> str:
        if not self.prefix:
            return self.full_name
        else:
            return f'{self.prefix}{self.last_name}'

    @property
    def full_name_with_prefix(self) -> str:
        return f'{self.prefix}{self.full_name}'

    @property
    def full_name_prefix_only_for_doctor(self) -> str:
        if self.is_doctor:
            return f'{self.prefix}{self.full_name}'
        return self.full_name
    
    @property
    def full_name(self) -> str:
        if self.first_name is None:
            return self.last_name
        else:
            return f'{self.first_name} {self.last_name}'


@dataclass
class ApplicationTarget:
    organization: Organization
    position_name: str
    person: Optional[HiringManager] = None
    custom_app_name: Optional[str] = None

    def __post_init__(self):
        if self.person is None:
            self.person = HiringManager(
                f'{self.organization.abbreviation} Hiring Committee',
                is_person=False
            )

    @property
    def app_name(self):
        if self.custom_app_name is None:
            return self.organization.abbreviation
        return self.custom_app_name


@dataclass
class CoverLetter:
    target: ApplicationTarget
    target_specific_content: PyexlatexItems
    included_components: Sequence[ApplicationComponents]
    focus: ApplicationFocus
    specific_focus: Optional[SpecificApplicationFocus] = None
    included_references: Sequence[Author] = (AUTHORS[ANDY], AUTHORS[NIMAL], AUTHORS[BAOLIAN])
    font_scale: float = 1
    line_spacing: float = 1
    as_email: bool = False
    by_email: bool = False
    use_resume: bool = False
    custom_file_renames: Optional[Dict[ApplicationComponents, str]] = None
    combine_files: Optional[Dict[str, Sequence[ApplicationComponents]]] = field(
        default_factory=lambda: {'Nick DeRobertis Application': (ApplicationComponents.ALL,)}
    )  # type: ignore
    add_organization_name_to_address: bool = True
    output_compression_level: Optional[int] = None
    video_output_format: str = 'mkv'
    video_desired_size_mb: Optional[int] = None
    references_are_being_submitted: bool = True
    references_were_previously_submitted: bool = False
    file_locations: Dict[ApplicationComponents, str] = field(default_factory=lambda: {})
    coding_sample_url: str = 'https://github.com/nickderobertis/py-finstmt'
    coding_sample_description: str = """
This is a Python package I developed to ease working with financial statements. It helps load in statement data 
from a variety of sources into a standard data structure, automates common calculations, and allows forecasting 
the statements using a variety of models while also keeping the balance sheet balanced. No such package existed 
and so I created this to support my Financial Modeling class. The main code is in the finstmt folder. The 
(currently minimal) documentation is linked on the Github page.
    """.strip()
    include_general_overview: bool = True
    cv_modifier_func: Optional[Callable[['CVModel'], 'CVModel']] = None

    def to_pyexlatex(self, output: bool = True, out_folder: str = DOCUMENTS_BUILD_PATH) -> pl.LetterDocument:
        contents = [
            self.blue,
            self.intro_paragraph,
            *self.desire_content,
            self.app_package(email=self.as_email),
            self.action_paragraph,
        ]

        packages = [
            pl.Package('geometry', modifier_str='margin=0.75in'),
            pl.Package('hyperref', modifier_str='hidelinks'),
            'graphicx',
        ]

        pre_env_contents = []
        signer_contents = []

        if not self.as_email:
            packages.append('fontspec')
            font_str = (
                r'\setmainfont{Latin Modern Roman}[Scale =' +
                str(self.font_scale) +
                ',Ligatures = {Common, TeX}]'
            )
            pre_env_contents.append(pl.Raw(font_str))
            signer_contents.extend([
                pl.VSpace(-1.6),
                pl.Graphic(images_path('signature.png'), width='5cm'),
                pl.OutputLineBreak(),
                NAME
            ])
        else:
            signer_contents.extend([pl.Raw(r'\HCode{<br>}'), NAME])

        if self.line_spacing != 1:
            packages.extend([
                'setspace',
                LineSpacing(self.line_spacing)
            ])

        saluation = f'Dear {self.target.person.salutation_name if self.target.person else "Sir or Madam"}:'

        full_name_and_address = [NAME, *ADDRESS_LINES]
        if OrganizationCharacteristics.INTERNATIONAL in self.target.organization.characteristics:
            full_name_and_address.append('United States')

        letter = pl.LetterDocument(
            contents,
            contact_info=full_name_and_address,
            to_contact_info=self.to_contact_info,
            signer_name=signer_contents,
            salutation=saluation,
            packages=packages,
            pre_env_contents=pre_env_contents,
            font_size=11,
        )

        if output:
            if self.as_email:
                letter.to_html(out_folder, outname=f'{self.target.organization.abbreviation} Cover Letter')
            else:
                letter.to_pdf(out_folder, outname=f'{self.target.organization.abbreviation} Cover Letter')
            if self.by_email:
                email_contents = [
                    saluation,
                    '',
                    self.separate_email_intro,
                    self.app_package(email=True, include_cover_letter=True),
                    self.separate_email_conclusion,
                    '\n',
                    *self.separate_email_signature,
                ]
                email_doc = pl.Document(email_contents)
                email_doc.to_html(out_folder, outname=f'{self.target.organization.abbreviation} Email Body')

        return letter

    @property
    def file_renames(self) -> Dict[ApplicationComponents, str]:
        if self.custom_file_renames is not None:
            return self.custom_file_renames

        default_renames = {
            ApplicationComponents.CV: f'Nick DeRobertis {self.resume_or_cv_capitalized_str}',
            ApplicationComponents.COVER_LETTER: f'Nick DeRobertis Cover Letter {self.target.app_name}',
        }
        return default_renames

    @property
    def resume_or_cv_str(self) -> str:
        return 'resume' if self.use_resume else 'CV'

    @property
    def resume_or_cv_capitalized_str(self) -> str:
        return 'Resume' if self.use_resume else 'CV'

    @property
    def separate_email_intro(self) -> str:
        p = inflect.engine()
        a_position = p.a(self.target.position_name)

        return f"""
I hope this email finds you well. My name is {NAME} and I would like to submit my application 
to be {a_position} at {self.target.organization.abbreviation}.
""".strip()

    @property
    def separate_email_conclusion(self) -> str:
        if self.references_are_being_submitted:
            ref_str = 'will receive supporting reference letters from'
        elif self.references_were_previously_submitted:
            ref_str = 'should have already received supporting reference letters from'
        elif len(ApplicationComponents.aggregate(self.included_components)) > 1:
            ref_str = f'will find a list of references at the end of my {self.resume_or_cv_str}, including'
        else:
            ref_str = 'will find a list of references at the end, including'

        return f"""
you {ref_str} 
{self.recommenders_str}. Please do not hesitate to reach out to them.
If you have any questions, please do not hesitate to contact me by replying to this email 
or at {PHONE}. 
""".strip()

    @property
    def separate_email_signature(self) -> PyexlatexItems:
        return [
            'Best Regards,',
            '',
            pl.Raw(r'\HCode{<br>}'),
            FIRST_NAME,
        ]

    @property
    def to_contact_info(self) -> List[str]:
        contact_info = [
            self.target.person.full_name_prefix_only_for_doctor if self.target.person else "",
        ]

        if self.add_organization_name_to_address:
            contact_info.append(self.target.organization.title)

        if self.target.organization.address_lines is not None:
            contact_info.extend(self.target.organization.address_lines)

        return contact_info

    @property
    def intro_paragraph(self) -> str:
        p = inflect.engine()
        a_position = p.a(self.target.position_name)
        if self.as_email:
            site_highlight = f' (see more detail at {self.__class__.site_link()}).'
        else:
            site_highlight = f'.{self.site_footnote}'
        i_am = 'I am a Ph.D. candidate in Finance at the University of Florida (graduating in May 2021)'
        if self.focus in (ApplicationFocus.ACADEMIC, ApplicationFocus.GOVERNMENT, ApplicationFocus.SEMI_ACADEMIC):
            pass
        elif self.focus == ApplicationFocus.INDUSTRY:
            i_am += ", and also the CTO of a small software startup"
        else:
            raise NotImplementedError(f'need to implement I am sentence for focus {self.focus}')
        return f"""
I am writing to express my interest and enthusiasm to be {a_position} at 
{self.target.organization.abbreviation} and to submit my supporting application materials.
My name is {NAME} and {i_am}.
During the Ph.D., I produced four working papers, five works 
in progress, developed and taught two courses across six different semesters in person and online with 
up to 4.8/5 evaluations, and created 34 open-source 
software projects that improve the efficiency and reproducibility of empirical research{site_highlight}
In addition to establishing a strong economics and finance foundation
during my Ph.D. studies, I also developed a comprehensive and unique set of analytical and soft
skills---a high competency in programming, econometrics, economic modeling, data science, and
communication. {self.interest_sentence}
        """.strip()

    @property
    def interest_sentence(self) -> str:
        if self.focus == ApplicationFocus.ACADEMIC:
            if self.as_email:
                modeling_course = self.modeling_link('Financial Modeling course')
            else:
                modeling_course = f'Financial Modeling course{self.modeling_footnote}'

            return f"""
I want to bring my strong research and software pipeline, along with 
my high competency for teaching and fully developed {modeling_course} to 
{self.target.organization.abbreviation}.
            """.strip()
        elif self.focus in (ApplicationFocus.GOVERNMENT, ApplicationFocus.SEMI_ACADEMIC):
            return ''
        elif self.focus == ApplicationFocus.INDUSTRY:
            return """
            At the same time, I helped build a software startup, fortifying my skills in full-stack web development, 
            dev-ops, architecture, and product management. 
            """.strip()
        else:
            raise ValueError(f'no handling for focus {self.focus}')

    @property
    def desire_content(self) -> List[PyexlatexItem]:
        contents: List[PyexlatexItem] = []
        if self.include_general_overview:
            if self.focus == ApplicationFocus.ACADEMIC:
                contents.extend([self.research_overview, self.teaching_overview])
            elif self.focus in (ApplicationFocus.GOVERNMENT, ApplicationFocus.INDUSTRY, ApplicationFocus.SEMI_ACADEMIC):
                contents.append(self.general_overview)
            else:
                raise ValueError(f'no handling for focus {self.focus}')

        contents.append(self.target_specific_content)

        return contents

    @property
    def research_overview(self) -> str:
        return """
My research agenda focuses on financial markets: analyzing the role of both fundamental and behavioral
information in price discovery, the effects of government intervention, and the performance of assets. 
My study "Government Equity Capital Market Intervention and Stock Returns" with Andy 
Naranjo and Mahendrarajah Nimalendran informs central bank personnel about the effects of purchasing 
broad-index equity ETFs on asset prices over time, which is valuable information at a time when the 
Federal Reserve is pursuing unprecedented levels of market intervention and even purchasing corporate debt. My job 
market paper, "Valuation without Cash Flows: What are Cryptoasset Fundamentals?" gives cryptocurrency investors 
both a theoretical framework and empirical models to assess the value of these assets, which could increase adoption and 
benefit society through elimination of counterparty risk, increased transparency, and speed of payments. 
My joint work on "OSPIN: Informed Trading in Options and Stock Markets" with
Yong Jin, Mahendrarajah Nimalendran, and Sugata Ray develops a new model to estimate the probability of informed 
trading that is more accurate as it considers the information in both the stock and options markets jointly, 
whereas prior models considered only stock markets,
which should be useful to researchers analyzing the information structure of markets and especially volatility 
information. Finally, my work on
"Are Investors Paying (for) Attention?" furthers the behavioral asset pricing literature focusing on investor attention,
the understanding of which may lead to more efficient prices as investors incorporate these effects into their 
valuation models. Each of my existing studies puts me down a path to do further research in those areas and I have 
a deep pipeline of works in progress.
        """

    @property
    def teaching_overview(self) -> str:
        return """
The common theme across the courses I've created and taught is a focus on preparing students for introductory
finance positions related to the course. I created Financial Modeling and Debt and Money Markets courses
from scratch to emphasize this focus and to de-emphasize institutional details that will be relevant for 
only a few students. I structure my courses to appeal to multiple learning types including auditory, visual, 
and kinesthetic learning and supplement by meeting with students to ensure that all students have an equal
opportunity to succeed. Financial Modeling is a capstone, senior course, which was previously taught using Excel but 
I have restructured it to focus mainly on Python skills. This is the first time a programming language has been taught
in an undergraduate finance course at UF, and one of only a handful of times a Ph.D. student has been allowed to 
teach a capstone course. I was granted this opportunity due to my teaching accolades, 4.8/5 evaluations and the 
Warrington College of Business Ph.D. Student Teaching Award, as well as my forward-thinking and technical skills.
        """

    @property
    def general_overview(self) -> str:
        return """
My research agenda focuses on financial markets: analyzing the role of both fundamental and behavioral
information in price discovery, the effects of government intervention, and the performance of assets. To
support my research agenda, I have developed a technical skill set that allows me to 
uncover novel data sets through 
web-scraping and API access, work with large data sets, and build
machine learning models to make predictions and classifications. 
        """

    def app_package(self, email: bool = False, include_cover_letter: bool = False) -> PyexlatexItems:
        included_components = ApplicationComponents.aggregate(self.included_components)
        components: List[Union[ApplicationComponents, str]]

        extra_begin_content: List[PyexlatexItem] = []
        if ApplicationComponents.CODING_SAMPLE in included_components:
            extra_begin_content.extend([
                self.__class__.link(
                    self.coding_sample_url, 'Please follow this Github link to see the coding sample.',
                ),
                self.coding_sample_description,
                ''
            ])

        if len(included_components) < 4:
            if included_components[0] == ApplicationComponents.CV:
                components = [included_components[0].value]
            else:
                components = [included_components[0].casefold()]
            if len(included_components) > 1:
                components.extend([comp.casefold() for comp in included_components[1:]])
            if email:
                package = 'the application package attached to this email'
            else:
                package = 'this application package'
            if include_cover_letter:
                components.append(ApplicationComponents.COVER_LETTER.casefold())

            if len(included_components) == 1:
                app_package = [
                    f'In addition to my {components[0]}'
                ]
            else:
                app_package = [
                    f'In addition to {package} that includes my',
                    join_with_commas_and_and(components)
                ]
            return extra_begin_content + app_package

        components = list(included_components)

        if email:
            intro = 'Attached to this email'
        else:
            intro = 'Within this application package'

        if include_cover_letter:
            components.append(ApplicationComponents.COVER_LETTER.casefold())

        included_components_bullets = pl.MultiColumn(
            pl.UnorderedList([comp.value if isinstance(comp, ApplicationComponents) else comp for comp in components]),
            3
        )

        return [
            *extra_begin_content,
            f"{intro}, you will find the following components:",
            pl.VSpace(-0.2),
            included_components_bullets,
            pl.VSpace(-0.5),
            'In addition to this application package, '
        ]

    @property
    def action_paragraph(self) -> str:
        if self.references_are_being_submitted:
            ref_str = 'will receive supporting reference letters from'
        elif self.references_were_previously_submitted:
            ref_str = 'should have already received supporting reference letters from'
        elif len(ApplicationComponents.aggregate(self.included_components)) > 1:
            ref_str = f'will find a list of references at the end of my {self.resume_or_cv_str}, including'
        else:
            ref_str = 'will find a list of references at the end, including'

        return f"""
you {ref_str}
{self.recommenders_str}. Please do not hesitate to reach out to them.
{self.application_action_sentence}
If you have any questions, please do not hesitate to contact me. I am especially interested in 
{self.target.organization.abbreviation} given the excellent professional and personal fit. 
Please contact me at {EMAIL} or {PHONE}. 
        """.strip()

    @property
    def application_action_sentence(self) -> str:
        sentence = 'I also have '
        if self.focus == ApplicationFocus.ACADEMIC:
            if self.as_email:
                sentence += f'{self.__class__.site_link("personal")} and {self.modeling_link("Financial Modeling")} websites'
            else:
                sentence += 'personal and Financial Modeling websites'
        elif self.focus in (ApplicationFocus.GOVERNMENT, ApplicationFocus.INDUSTRY, ApplicationFocus.SEMI_ACADEMIC):
            if self.as_email:
                sentence += f'a {self.__class__.site_link("personal website")}'
            else:
                sentence += 'a personal website'
        else:
            raise ValueError(f'no handling for focus {self.focus}')
        if self.as_email:
            sentence += ' linked here'
        else:
            sentence += ' listed in the footnotes'
        sentence += f' and on my {self.resume_or_cv_str} with additional information.'
        return sentence

    @property
    def recommenders_str(self) -> str:
        if self.recommenders_are_dissertation_chairs:
            name_str = join_with_commas_and_and([author.name for author in self.included_references])
            return f'my dissertation committee co-Chairs, Professors {name_str}'

        names = []
        non_dissertation = False
        for author in self.included_references:
            if author not in [AUTHORS[ANDY], AUTHORS[NIMAL], AUTHORS[BAOLIAN]]:
                non_dissertation = True

        if non_dissertation:
            names = [author.name for author in self.included_references]
        else:
            for author in self.included_references:
                if author in [AUTHORS[ANDY], AUTHORS[NIMAL]]:
                    names.append(f'{author.name} (co-Chair)')
                else:
                    names.append(author.name)

        if non_dissertation:
            introduce_str = 'Professors'
        else:
            introduce_str = 'my dissertation committee, Professors'

        name_str = join_with_commas_and_and(names)

        return f'{introduce_str} {name_str}'

    @property
    def recommenders_are_dissertation_chairs(self) -> bool:
        return (
            len(self.included_references) == 2 and
            AUTHORS[ANDY] in self.included_references and
            AUTHORS[NIMAL] in self.included_references
        )

    @staticmethod
    def link(url: str, link_text: Optional[str] = None) -> pl.Hyperlink:
        if link_text is None:
            link_text = url

        return pl.Hyperlink(
            url,
            pl.Bold(
                pl.TextColor(link_text, color=BLUE)
            ),
        )

    @staticmethod
    def site_link(link_text: str = SITE_URL, url_path: Optional[str] = None) -> pl.Hyperlink:
        url = SITE_URL
        if url_path is not None:
            url += f'/{url_path}'

        return pl.Hyperlink(
            url,
            pl.Bold(
                pl.TextColor(link_text, color=BLUE)
            ),
        )

    def modeling_link(self, link_text: Optional[str] = None):
        financial_modeling_url = get_fin_model_course().website_url
        if link_text is None:
            link_text = financial_modeling_url
        modeling_link = pl.Hyperlink(
            financial_modeling_url,
            pl.Bold(
                pl.TextColor(link_text, color=self.blue)
            ),
        )
        return modeling_link

    @property
    def site_footnote(self) -> pl.Footnote:
        site_footnote = pl.Footnote(
            [
                'See more information on all of this at',
                self.__class__.site_link(),
                f'or on my {self.resume_or_cv_str}.'
            ]
        )
        return site_footnote

    @property
    def modeling_footnote(self) -> pl.Footnote:
        modeling_footnote = pl.Footnote(
            ['See the Financial Modeling course content at the course website: ', self.modeling_link()])
        return modeling_footnote

    @property
    def blue(self) -> pl.RGB:
        return pl.RGB(50, 82, 209, color_name="darkblue")


@dataclass
class CoverLetterDesireSection:
    target: ApplicationTarget
    focus: ApplicationFocus
    specific_focus: Optional[SpecificApplicationFocus] = None
    extra_content: Optional[PyexlatexItems] = None
    extra_professional_content: Optional[PyexlatexItems] = None

    @property
    def default_paragraph(self) -> str:
        return '\n' + self.professional_paragraph + ' ' + self.personal_sentence + '\n'

    @property
    def professional_paragraph(self) -> str:
        if self.target.organization.abbreviation is None:
            raise ValueError('must have organization abbrevation to create desire paragraph professional portion')

        abbrev_posessive = (
            f"{self.target.organization.abbreviation}'s"
            if not self.target.organization.abbreviation.casefold().endswith('s')
            else f"{self.target.organization.abbreviation}'"
        )

        p = inflect.engine()
        a_position = p.a(self.target.position_name)

        para = ''
        if self.focus == ApplicationFocus.ACADEMIC:
            para = f"""
            My multiple lines of research and strong work ethic will contribute to {abbrev_posessive} goal of preeminence in 
            research. Further, I will contribute to the goals of innovation and transformative, accessible education. 
            It may already be apparent that I am not the typical Finance Ph.D. applicant: I have a much
            larger emphasis on creating open-source software. My commitment to open-source is a commitment to inclusion and 
            diversity: I believe everyone should have access to these tools regardless of their economic position, 
            and that anyone should be able to learn from them, regardless of their location in the world or cultural 
            background. I have already built tools for both research and education, and I want to continue innovating
            at a university that encourages such efforts.
            """.strip()
        elif self.focus == ApplicationFocus.GOVERNMENT:
            if self.specific_focus is None:
                raise ValueError('cannot determine auto government paragraph without specific focus')
            elif self.specific_focus in (SpecificApplicationFocus.BANKING_REGULATOR, SpecificApplicationFocus.OTHER_FINANCIAL_REGULATOR):
                if self.specific_focus == SpecificApplicationFocus.BANKING_REGULATOR:
                    regulatory = 'banking supervisory'
                elif self.specific_focus == SpecificApplicationFocus.OTHER_FINANCIAL_REGULATOR:
                    regulatory = 'regulatory'
                else:
                    raise ValueError(f'could not determine desire paragraph for specific focus {self.specific_focus}')
                para = f"""
                I believe I am an ideal fit at {self.target.organization.abbreviation} as {a_position} given my 
                related research in market microstructure, 
                macroeconomics, and economic policy as well as technical skills related to developing economic models and
                communicating insights from large quantities of data. I am familiar with {regulatory} work 
                from both ends: 
                I was an intern in the Credit Risk department at the Federal Reserve Board of Governors and 
                I worked directly with bank examiners in my 
                role as a Portfolio Analyst rebuilding the models for the Allowance for Loan and Lease Losses at 
                Eastern Virginia Bankshares. I also have experience evaluating policy through my research which 
                analyzes the intended and unintended effects of central bank equity market intervention.
                I have a strong interest in regulatory issues in financial
                markets and am equally comfortable being both self-guided and a team player providing 
                high-quality results and recommendations.
                """.strip()
            else:
                raise NotImplementedError(f'have not implemented letter for specific focus {self.specific_focus}')
        elif self.focus == ApplicationFocus.SEMI_ACADEMIC:
            if self.specific_focus is None:
                raise ValueError('cannot determine semi-academic paragraph without specific focus')
            elif self.specific_focus == SpecificApplicationFocus.ASSET_MANAGER:
                para = f"""
                I believe I am an ideal fit at {self.target.organization.abbreviation} as {a_position} given my 
                related research in empirical asset pricing, market microstructure, and behavioral finance
                as well as technical skills related to developing trading strategies and
                communicating insights from large quantities of data. I have worked on asset pricing and 
                microstructure research for a variety of asset classes including stocks, options,
                fixed income, and cryptocurrencies. I have applied machine learning and textual analysis 
                in my research, have given numerous informal seminars to fellow
                Ph.D students on programming topics such as machine learning and Python for research applications, 
                and I am widely viewed in the department as a resource on such topics.
                I have a strong interest in developing asset pricing and allocation models
                and am equally comfortable being both self-guided and a team player providing 
                high-quality results and recommendations.
                """.strip()
            else:
                raise NotImplementedError(f'have not implemented letter for specific focus {self.specific_focus}')
        elif self.focus == ApplicationFocus.INDUSTRY:
            if self.specific_focus is None:
                raise ValueError('cannot determine auto industry paragraph without specific focus')
            elif self.specific_focus == SpecificApplicationFocus.TECH_COMPANY:
                from private_cv.applications import get_tech_company_desire_paragraph
                para = get_tech_company_desire_paragraph(self.target.organization.abbreviation, a_position)
            elif self.specific_focus == SpecificApplicationFocus.DATA_SCIENCE:
                from private_cv.applications import get_data_science_company_desire_paragraph
                para = get_data_science_company_desire_paragraph(self.target.organization.abbreviation, a_position)
            elif self.specific_focus == SpecificApplicationFocus.BANK:
                from private_cv.applications import get_banking_desire_paragraph
                para = get_banking_desire_paragraph(self.target.organization.abbreviation, a_position)
            elif self.specific_focus == SpecificApplicationFocus.ECONOMIST:
                from private_cv.applications import get_economist_desire_paragraph
                para = get_economist_desire_paragraph(self.target.organization.abbreviation, a_position)
            else:
                raise NotImplementedError(f'have not implemented letter for specific focus {self.specific_focus}')
        else:
            raise NotImplementedError(f'need to implement auto desire paragraph for focus {self.focus}')

        if self.extra_professional_content:
            para = build([para, self.extra_professional_content])

        return para

    @property
    def personal_sentence(self) -> str:
        if not self.target.organization.characteristics:
            raise ValueError('must pass characteristics to organization to generate default desire personal sentence')
        if self.target.organization.city is None:
            raise ValueError('must pass city to organization to generate default desire personal sentence')

        personal_sentence = "On a personal level, my wife and I "
        phrases: List[str] = []
        if OrganizationCharacteristics.SMALL_TOWN in self.target.organization.characteristics:
            phrases.append('enjoy outdoor activities')
        elif OrganizationCharacteristics.MID_SIZE_CITY in self.target.organization.characteristics:
            phrases.append('have an affinity for mid-size cities')
        elif OrganizationCharacteristics.LARGE_CITY in self.target.organization.characteristics:
            phrases.append('have an affinity for larger cities')
        elif OrganizationCharacteristics.NOVA in self.target.organization.characteristics:
            phrases.append('are from the Northern Virginia area')
        elif OrganizationCharacteristics.SUBURBAN in self.target.organization.characteristics:
            phrases.append('have been looking to settle down in a quiet suburb')

        char_desc_map: Dict[OrganizationCharacteristics, str] = {
            OrganizationCharacteristics.WEST_COAST: 'the West Coast',
            OrganizationCharacteristics.WARM_WEATHER: 'warm weather',
            OrganizationCharacteristics.FAMILY_CLOSE: 'we have family close by',
        }

        for char, phrase in char_desc_map.items():
            if char in self.target.organization.characteristics:
                phrases.append(phrase)

        personal_sentence += join_with_commas_and_and(phrases)

        location = self.target.organization.city
        seem = 'seems'

        if OrganizationCharacteristics.INTERNATIONAL in self.target.organization.characteristics:
            if self.target.organization.country is None:
                raise ValueError('must pass country to organization when international is passed in characteristics')
            personal_sentence += ', and have been hoping for an opportunity to live abroad from the US,'
            if self.target.organization.country != self.target.organization.city:
                location += f' and {self.target.organization.country}'
                seem = 'seem'

        personal_sentence += f' so {location} {seem} like a good fit'

        if self.target.organization.country == 'Canada':
            personal_sentence += ' (no, I am not a current citizen or permanent resident of Canada)'

        if OrganizationCharacteristics.REMOTE in self.target.organization.characteristics:
            personal_sentence += f', though I also appreciate that {self.target.organization.abbreviation} ' \
                                 f'supports remote work and I have been 100% remote myself since March of 2020'

        if OrganizationCharacteristics.MULTIPLE_LOCATIONS in self.target.organization.characteristics:
            personal_sentence += f', though I would be pleased to work at any ' \
                                 f'potential {self.target.organization.abbreviation} location'

        if OrganizationCharacteristics.SPANISH_SPEAKING in self.target.organization.characteristics:
            personal_sentence += f', and I would be happy to spend my spare time expanding on my existing ' \
                                 f'introductory Spanish knowledge to become fluent'

        if OrganizationCharacteristics.FRENCH_SPEAKING in self.target.organization.characteristics:
            personal_sentence += f', and I would be happy to spend my spare time learning French'

        personal_sentence += '.'
        return personal_sentence

    def to_pyexlatex(self) -> PyexlatexItems:
        if self.extra_content is None:
            return [self.default_paragraph]

        if isinstance(self.extra_content, (list, tuple)):
            return [self.default_paragraph.strip(), *self.extra_content]
        else:
            return [self.default_paragraph.strip(), self.extra_content]
