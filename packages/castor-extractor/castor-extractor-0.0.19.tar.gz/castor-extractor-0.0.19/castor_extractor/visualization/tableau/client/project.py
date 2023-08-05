from typing import Optional

from ....utils import EntitiesType


def _folder_path(
    projects: EntitiesType, project: dict, root: Optional[str] = ""
) -> str:
    """Recursive function to compute folder path with list of projects"""
    path = "/" + str(project["name"]) + (root or "")
    if project["parent_id"] is None:
        return path

    parent_project = next(
        parent_project
        for parent_project in projects
        if parent_project["id"] == project["parent_id"]
    )
    return _folder_path(projects, parent_project, path)


def compute_project_path(projects: EntitiesType) -> EntitiesType:
    """Compute folder path with parent project name"""
    for project in projects:
        project["folder_path"] = _folder_path(projects, project)
    return projects
