from typing import Iterable, Set, Tuple

from .sdk import Dashboard, LookmlModel


def lookml_explore_names(
    lookmls: Iterable[LookmlModel],
) -> Set[Tuple[str, str]]:
    """
    Explores from the lookml models
    Only valid explores are yielded: with all infos
    """
    model_explores = (
        (model, explore)
        for model in lookmls
        for explore in model.explores or []
    )

    return {
        (model.name, explore.name)
        for model, explore in model_explores
        # accept hidden resources
        if model.name and explore.name
    }


def dashboard_explore_names(
    dashboards: Iterable[Dashboard],
) -> Set[Tuple[str, str]]:
    """Explores that appear in dashboards"""
    elements = (
        element
        for dashboard in dashboards
        for element in dashboard.dashboard_elements or []
    )

    return {
        (element.query.model, element.query.view)
        for element in elements
        if element.query and element.query.model and element.query.view
    }


def explore_names_associated_to_dashboards(
    lookmls: Iterable[LookmlModel], dashboards: Iterable[Dashboard]
):
    """Retrieve only explores that are associated to a looker dashboard"""
    return lookml_explore_names(lookmls).intersection(
        dashboard_explore_names(dashboards)
    )
