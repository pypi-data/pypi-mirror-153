from typing import List, Optional, Sequence
import os
import yaml
from derobertis_cv.pltemplates.software.project import SoftwareProject
from derobertis_cv.pldata.software.yaml_.modify import apply_modifications_to_projects


def get_project_dict_list(file_path: Optional[str] = None) -> List[dict]:
    if file_path is None:
        folder = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(folder, 'projects.yaml')

    with open(file_path, 'r') as f:
        pr_dict_list = yaml.safe_load(f)

    return pr_dict_list


def get_projects_from_yaml_config(file_path: Optional[str] = None, use_full_loc: bool = True,
                                  include_projects: Optional[Sequence[str]] = None,
                                  exclude_projects: Optional[Sequence[str]] = None) -> List[SoftwareProject]:
    pr_dict_list = get_project_dict_list(file_path)
    include_projects = _get_include_projects(pr_dict_list, include_projects, exclude_projects)
    if include_projects:
        pr_dict_list = [project for project in pr_dict_list if project['name'] in include_projects]
    return SoftwareProject.list_from_project_report_dict_list(pr_dict_list, use_full_loc=use_full_loc)


def get_modified_projects_from_yaml_config(file_path: Optional[str] = None, use_full_loc: bool = True,
                                           include_projects: Optional[Sequence[str]] = None,
                                           exclude_projects: Optional[Sequence[str]] = None,
                                           order: Optional[Sequence[str]] = None) -> List[SoftwareProject]:
    projects = get_projects_from_yaml_config(
        file_path,
        use_full_loc=use_full_loc,
        include_projects=include_projects,
        exclude_projects=exclude_projects,
    )
    projects = apply_modifications_to_projects(projects, order=order)
    return projects


def _get_include_projects(project_dicts: List[dict], include_projects: Optional[Sequence[str]] = None,
                          exclude_projects: Optional[Sequence[str]] = None) -> Optional[List[str]]:
    if include_projects is not None and exclude_projects is not None:
        raise ValueError('cannot pass both include and exclude projects')
    if include_projects is not None:
        return list(include_projects)
    if exclude_projects is not None:
        project_names = [project['name'] for project in project_dicts]
        return [name for name in project_names if name not in exclude_projects]

    return None