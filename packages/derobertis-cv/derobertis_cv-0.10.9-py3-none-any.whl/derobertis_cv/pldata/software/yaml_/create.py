import os
import warnings
from typing import Sequence, Optional

import requests
from projectreport import JavaScriptPackageFinder
from projectreport.analyzer.project import Project
from projectreport.finder.combine import CombinedFinder
from projectreport.finder.git import GitFinder
from projectreport.finder.python import PythonPackageFinder
from projectreport.report.project import ProjectReport
from projectreport.report.report import Report

from derobertis_cv.logger import logger
from derobertis_cv.pldata.software.yaml_.config import PROJECT_DIRECTORIES, IGNORE_DIRECTORIES, YAML_OUT_PATH


def create_report(search_dirs: Sequence[str] = PROJECT_DIRECTORIES,
                  ignore_dirs: Sequence[str] = IGNORE_DIRECTORIES) -> Report:
    finder = CombinedFinder([
        GitFinder(),
        PythonPackageFinder(),
        JavaScriptPackageFinder(),
    ], recursive=False)
    project_paths = finder.find_all(search_dirs, ignore_paths=ignore_dirs)
    logger.debug(f'Found project paths {project_paths}')
    projects = [Project(path, included_types=('py', 'js', 'ts'), ignore_paths=ignore_dirs) for path in project_paths]
    logger.info(f'Created {len(projects)} individual projects')
    report = Report(projects, depth=1)
    _add_generated_data_to_report(report)
    logger.info(f'Report containing {len(projects)} projects created successfully')
    return report


def create_yaml(search_dirs: Sequence[str] = PROJECT_DIRECTORIES,
                ignore_dirs: Sequence[str] = IGNORE_DIRECTORIES, out_path: Optional[str] = YAML_OUT_PATH):
    if out_path is None:
        folder = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(folder, 'projects.yaml')

    report = create_report(search_dirs, ignore_dirs)
    with open(out_path, 'w') as f:
        f.write(report.yaml)


def _add_generated_data_to_report(report: Report):
    num_projects = len(report.project_reports)
    logger.info(f'Adding generated data to {num_projects} projects')
    for i, project_report in enumerate(report.project_reports):
        name = project_report.data.get("name")
        logger.debug(f'Adding generated data to {name} ({i + 1}/{num_projects})')
        _add_generated_data_to_project_report(project_report)


def _add_generated_data_to_project_report(report: ProjectReport):
    if report.data['subprojects']:
        try:
            _add_data_from_subprojects(report)
        except MultipleProjectDescriptionsException as e:
            logger.warning(str(e))

    # Handle pulling url from array
    report.data['github_url'] = report.data['urls'][0] if report.data['urls'] is not None else None

    title = report.data['name']
    url = report.data.get('github_url')
    package_directory = report.data.get('package_directory')
    if url is not None:
        docs_url = f'https://nickderobertis.github.io/{title}/'
        response = requests.get(docs_url)
        if response.status_code == 200:
            report.data['docs_url'] = docs_url
    if package_directory is not None:
        potential_logo_url = f'https://nickderobertis.github.io/derobertis-project-logo/_images/{package_directory}.svg'
        response = requests.get(potential_logo_url)
        if response.status_code == 200:
            report.data['logo_url'] = potential_logo_url
            report.data['logo_svg_text'] = response.content.decode('utf8')


def _add_data_from_subprojects(report: ProjectReport):
    subproject_descriptions_map = {
        subproject['docstring']: sp_path for sp_path, subproject in report.data['subprojects'].items()
    }
    subproject_descriptions = [spd for spd in subproject_descriptions_map.keys() if spd is not None]
    if len(subproject_descriptions) > 1:
        raise MultipleProjectDescriptionsException(f'main project {report.data["name"]} does not have a docstring,'
                                                   f'so tried to get from subprojects, but there are multiple'
                                                   f'subprojects with docstrings.')
    if subproject_descriptions:
        report.data['description'] = subproject_descriptions[0]

        # Set package directory
        subproject_path = subproject_descriptions_map[subproject_descriptions[0]]
        report.data['package_directory'] = subproject_path.split(os.sep)[-1]


class MultipleProjectDescriptionsException(Exception):
    pass


if __name__ == '__main__':
    create_yaml()
