from typing import List, Tuple

from derobertis_cv.pldata.software import get_software_projects
from derobertis_cv.pldata.software.config import EXCLUDED_SOFTWARE_PROJECTS
from derobertis_cv.pltemplates.software.project import SoftwareProject


def test_that_all_software_projects_have_required_info():
    for project in get_software_projects(
        exclude_projects=EXCLUDED_SOFTWARE_PROJECTS,
    ):
        _assert_software_project_has_required_info(project)


def _assert_software_project_has_required_info(project: SoftwareProject):
    checks: List[Tuple[str, bool]] = [
        ("title", project.title is not None),
        ("description", project.description is not None),
        ("display_title", project.display_title is not None),
        ("loc", project.loc is not None),
        ("github_url", project.github_url is not None),
    ]
    failed_checks = [check for check, result in checks if not result]
    if failed_checks:
        raise ValueError(f"Project {project} is missing required info: {failed_checks}")
