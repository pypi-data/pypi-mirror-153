from ...utils import EntitiesType, group_by


def compute_usage_views(usages: EntitiesType) -> EntitiesType:
    """Compute usages views with group by workbook_id"""
    grouped = group_by("workbook_id", usages)
    aggregated = [
        {
            "workbook_id": key,
            "view_counts": sum(x["total_views"] for x in value),
        }
        for key, value in grouped.items()
    ]
    return aggregated
