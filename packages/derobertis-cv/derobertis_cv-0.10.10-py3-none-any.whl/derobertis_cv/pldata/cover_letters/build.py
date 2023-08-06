import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, List

from PyPDF2 import PdfFileMerger

from derobertis_cv.pdf_compressor import compress_pdf
from derobertis_cv.plbuild.paths import DOCUMENTS_BUILD_PATH, documents_build_path, pdfs_path, APPLICATIONS_OUT_PATH, \
    private_assets_path
from derobertis_cv.pldata.constants.contact import NAME
from derobertis_cv.pldata.cover_letters.letter_config import get_cover_letters
from derobertis_cv.pldata.cover_letters.models import ApplicationComponents, ApplicationFocus, CoverLetter, \
    RESEARCH_COMPONENTS, SpecificApplicationFocus
from derobertis_cv.pldata.cv import CVTypes, get_custom_cv_model
from derobertis_cv.video_converter import convert_video_format, get_video_options


@dataclass
class FileLocations:
    letter: CoverLetter

    def location(self, component: ApplicationComponents) -> Path:
        cover_letter_name = f'{self.letter.target.organization.abbreviation} Cover Letter.pdf'
        cover_letter_email_name = f'{self.letter.target.organization.abbreviation} Cover Letter.html'
        email_body_name = f'{self.letter.target.organization.abbreviation} Email Body.html'

        file_locations: Dict[ApplicationComponents, str] = {
            ApplicationComponents.JOB_MARKET_PAPER: pdfs_path('Job Market Paper - Valuation without Cash Flows.pdf'),
            ApplicationComponents.GOVERNMENT_INTERVENTION_PAPER: pdfs_path('Government Equity Market '
                                                                           'Intervention and the Cross_Section '
                                                                           'of Stock Returns.pdf'),
            ApplicationComponents.INVESTOR_ATTENTION_PAPER: pdfs_path('Are Investors Paying (for) Attention?.pdf'),
            ApplicationComponents.OPIN_PAPER: pdfs_path('OSPIN: Informed Trading in Options and Stock Markets.pdf'),
            ApplicationComponents.RESEARCH_STATEMENT: documents_build_path('Research Statement.pdf'),
            ApplicationComponents.RESEARCH_LIST: documents_build_path('Nick DeRobertis Research List.pdf'),
            ApplicationComponents.TEACHING_STATEMENT: documents_build_path('Teaching Statement.pdf'),
            ApplicationComponents.COURSE_OUTLINES: pdfs_path('Course Outline.pdf'),
            ApplicationComponents.TRANSCRIPTS: pdfs_path('All Transcripts.pdf'),
            ApplicationComponents.EVALUATIONS: pdfs_path('All Evaluations.pdf'),
            ApplicationComponents.COVER_LETTER: documents_build_path(cover_letter_name),
            ApplicationComponents.REFERENCES: documents_build_path(f'{NAME} References.pdf'),
            ApplicationComponents.PERSONAL_WEBSITE: documents_build_path(f'{NAME} Personal Website.pdf'),
            ApplicationComponents.EMAIL_BODY: documents_build_path(email_body_name),
            ApplicationComponents.COVER_LETTER_AS_EMAIL: documents_build_path(cover_letter_email_name),
            ApplicationComponents.JMP_VIDEO: private_assets_path(
                'Job Market Paper - Valuation without Cash Flows - Nick DeRobertis.mkv'
            ),
            ApplicationComponents.SKILLS_LIST: documents_build_path('Nick DeRobertis Skills List.html'),
            ApplicationComponents.RESEARCH_COVER: documents_build_path('Selected Research Works.pdf'),
            ApplicationComponents.TEACHING_COVER: documents_build_path('Teaching Portfolio.pdf'),
            ApplicationComponents.TEACHING_EXPERIENCE_OVERVIEW: documents_build_path('Teaching Experience Overview.pdf'),
            ApplicationComponents.PASSPORT_PHOTO: private_assets_path('Nick DeRobertis Passport.jpg')
        }

        if self.letter.focus == ApplicationFocus.ACADEMIC:
            file_locations[ApplicationComponents.CV] = documents_build_path(f'{NAME} CV.pdf')
            file_locations[ApplicationComponents.DIVERSITY] = documents_build_path('Diversity Statement.pdf')
        elif self.letter.focus in (ApplicationFocus.GOVERNMENT, ApplicationFocus.SEMI_ACADEMIC):
            file_locations[ApplicationComponents.CV] = documents_build_path(f'{NAME} Hybrid CV.pdf')
            file_locations[ApplicationComponents.DIVERSITY] = documents_build_path('Industry Diversity Statement.pdf')
        elif self.letter.focus == ApplicationFocus.INDUSTRY and not self.letter.use_resume:
            file_locations[ApplicationComponents.CV] = documents_build_path(f'{NAME} Professional CV.pdf')
            file_locations[ApplicationComponents.DIVERSITY] = documents_build_path('Industry Diversity Statement.pdf')
        elif self.letter.focus == ApplicationFocus.INDUSTRY:
            # Pick specific resume
            specific_focus_str = ''
            if self.letter.specific_focus is not None:
                specific_focus_str = ' ' + str(self.letter.specific_focus.value).title()
            file_locations[ApplicationComponents.CV] = documents_build_path(
                f'{NAME} Professional Resume{specific_focus_str}.pdf'
            )
            file_locations[ApplicationComponents.DIVERSITY] = documents_build_path('Industry Diversity Statement.pdf')
        else:
            raise NotImplementedError(
                f'need to get correct documents for focus {self.letter.focus}, '
                f'specific focus {self.letter.specific_focus}, '
                f'use resume: {self.letter.use_resume}'
            )

        file_locations.update(self.letter.file_locations)

        try:
            location = file_locations[component]
        except KeyError:
            raise NotImplementedError(f'cannot find location of application component {component}')

        return Path(location)


def build_applications(letter_out_folder: str = DOCUMENTS_BUILD_PATH,
                       application_out_folder: str = APPLICATIONS_OUT_PATH):
    cover_letters = get_cover_letters()
    for letter in cover_letters:
        _build_application(letter, letter_out_folder=letter_out_folder, application_out_folder=application_out_folder)


def build_application(target_abbreviation: str, letter_out_folder: str = DOCUMENTS_BUILD_PATH,
                       application_out_folder: str = APPLICATIONS_OUT_PATH):
    cover_letters = get_cover_letters()
    for letter in cover_letters:
        if letter.target.app_name is None:
            raise ValueError(f'must have organization abbreviation to build for {letter}')

        if letter.target.app_name.casefold() == target_abbreviation.casefold():
            _build_application(
                letter, letter_out_folder=letter_out_folder, application_out_folder=application_out_folder
            )
            return

    possible_abbreviations = [letter.target.app_name for letter in cover_letters]
    raise ValueError(f'could not find cover letter matching abbreviation {target_abbreviation}. '
                     f'Should be one of {possible_abbreviations}')


def _build_application(letter: CoverLetter, letter_out_folder: str = DOCUMENTS_BUILD_PATH,
                       application_out_folder: str = APPLICATIONS_OUT_PATH):
    app_name = letter.target.app_name
    if app_name is None:
        raise ValueError(f'must have organization abbreviation to build for {letter}')

    print(f'Building letter for {app_name}')
    letter.to_pyexlatex(out_folder=letter_out_folder)

    if letter.cv_modifier_func is not None:
        cv_type: CVTypes
        if letter.focus == ApplicationFocus.ACADEMIC:
            cv_type = CVTypes.ACADEMIC
        elif letter.focus in (ApplicationFocus.GOVERNMENT, ApplicationFocus.SEMI_ACADEMIC):
            cv_type = CVTypes.HYBRID
        elif letter.focus == ApplicationFocus.INDUSTRY and not letter.use_resume:
            cv_type = CVTypes.PROFESSIONAL
        elif letter.focus == ApplicationFocus.INDUSTRY:
            if letter.specific_focus is None:
                cv_type = CVTypes.PROFESSIONAL_RESUME
            else:
                cv_type = SpecificApplicationFocus.get_resume_type(letter.specific_focus)
        else:
            raise NotImplementedError(f'need to get correct documents for focus {letter.focus}')
        cv_model = get_custom_cv_model(cv_type, letter.cv_modifier_func)
        abbrev = letter.target.organization.abbreviation
        cv_model.file_name = f'Nick DeRobertis {abbrev} CV'
        letter.file_locations[ApplicationComponents.CV] = documents_build_path(cv_model.file_name + '.pdf')
        print(f'Building custom CV for {abbrev}')
        cv_model.output()


    print(f'Building application for {app_name}')
    file_locs = FileLocations(letter)
    this_out_folder = Path(application_out_folder) / app_name
    if os.path.exists(this_out_folder):
        shutil.rmtree(this_out_folder)
    os.makedirs(this_out_folder)

    pdf_components: List[ApplicationComponents] = []
    html_components: List[ApplicationComponents] = []
    image_components: List[ApplicationComponents] = []
    video_components: List[ApplicationComponents] = []
    if letter.as_email:
        html_components.append(ApplicationComponents.COVER_LETTER_AS_EMAIL)
    else:
        pdf_components.append(ApplicationComponents.COVER_LETTER)
    if letter.by_email:
        html_components.append(ApplicationComponents.EMAIL_BODY)
    pdf_components.extend(letter.included_components)
    if ApplicationComponents.JMP_VIDEO in letter.included_components:
        video_components.append(ApplicationComponents.JMP_VIDEO)
        pdf_components.remove(ApplicationComponents.JMP_VIDEO)
    if ApplicationComponents.CODING_SAMPLE in letter.included_components:
        pdf_components.remove(ApplicationComponents.CODING_SAMPLE)
    if ApplicationComponents.SKILLS_LIST in letter.included_components:
        pdf_components.remove(ApplicationComponents.SKILLS_LIST)
        html_components.append(ApplicationComponents.SKILLS_LIST)
    if ApplicationComponents.PASSPORT_PHOTO in letter.included_components:
        pdf_components.remove(ApplicationComponents.PASSPORT_PHOTO)
        image_components.append(ApplicationComponents.PASSPORT_PHOTO)

    standard_components = [*html_components, *image_components]

    for component in [*pdf_components, *standard_components, *video_components]:
        source = file_locs.location(component)
        if letter.file_renames and component in letter.file_renames:
            out_path = this_out_folder / (letter.file_renames[component] + '.pdf')
        else:
            out_path = this_out_folder / os.path.basename(source)
        if component in video_components:
            base_name, extension = os.path.splitext(os.path.basename(source))
            if extension == f'.{letter.video_output_format}':
                shutil.copy(source, out_path)
            else:
                out_path = this_out_folder / f'{base_name}.{letter.video_output_format}'
                video_options = {}
                if letter.video_desired_size_mb is not None:
                    video_options = get_video_options(component, letter.video_desired_size_mb)
                convert_video_format(source, out_path, letter.video_output_format, video_options=video_options)
        elif letter.output_compression_level is not None and component in pdf_components:
            compress_pdf(str(source), str(out_path), power=letter.output_compression_level)
        else:
            shutil.copy(source, out_path)


    if letter.combine_files is not None:
        for file_name, included_components in letter.combine_files.items():
            if ApplicationComponents.ALL in included_components:
                included_components = pdf_components
            combined_out_path = this_out_folder / f'{file_name}.pdf'
            merger = PdfFileMerger()
            combine_components: List[ApplicationComponents] = []
            for comp in included_components:
                if comp in pdf_components:
                    combine_components.append(comp)
                else:
                    raise ValueError(f'component {comp} was included on combine files but not included in application')

            for component in combine_components:
                source = file_locs.location(component)
                merger.append(str(source))

            if letter.output_compression_level is not None:
                temp_path = this_out_folder / 'temp.pdf'
                merger.write(str(temp_path))
                compress_pdf(str(temp_path), str(combined_out_path), power=letter.output_compression_level)
                os.remove(temp_path)
            else:
                merger.write(str(combined_out_path))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=False, help="Abbreviation of cover letter to build")
    args = parser.parse_args()

    if args.name:
        build_application(args.name)
    else:
        build_applications()
