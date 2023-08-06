from typing import (
    List,
    Tuple,
)


def exclude_projects_combinations(
    projects_combinations: List[Tuple['ProjectEnum', ...]],
    excluded_projects_combinations: List[Tuple['ProjectEnum', ...]],
):
    """
    Исключает комбинации проектов, если в них присутствуют исключаемые комбинации
    """
    temp_projects_combinations = []

    for projects_combination in projects_combinations:
        excluded = False

        for excluded_project_combination in excluded_projects_combinations:
            if all(epc in projects_combination for epc in excluded_project_combination):
                excluded = True
                break

        if not excluded:
            temp_projects_combinations.append(projects_combination)

    return temp_projects_combinations
