from typing import Optional, Sequence
from derobertis_cv.pldata.software.yaml_.load import get_modified_projects_from_yaml_config


def get_software_projects(include_projects: Optional[Sequence[str]] = None,
                          exclude_projects: Optional[Sequence[str]] = None,
                          order: Optional[Sequence[str]] = None):
    return get_modified_projects_from_yaml_config(
        include_projects=include_projects,
        exclude_projects=exclude_projects,
        order=order,
    )
