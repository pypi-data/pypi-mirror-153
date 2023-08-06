""" GraphQL GetProject Query """
from typing import List, Optional

import fire

from mcli.api.engine.engine import run_graphql_success_query
from mcli.api.schema.project import get_project_schema
from mcli.api.schema.query import named_success_query
from mcli.api.types import GraphQLQueryVariable, GraphQLVariableType
from mcli.models.project import ProjectModel


def get_project(
    project_name: str,
    include_runs: bool = False,
) -> Optional[ProjectModel]:
    """Runs a GraphQL query to get a project by name

    Args:
        project_name (str): Name of the project to get

    Returns:
        Returns a project object
    """
    query_function = 'getProject'
    variable_data_name = '$projectNameInput'
    variables = {
        variable_data_name: project_name,
    }
    graphql_variable: GraphQLQueryVariable = GraphQLQueryVariable(
        variableName='projectName',
        variableDataName=variable_data_name,
        variableType=GraphQLVariableType.STRING_REQUIRED,
    )

    query = named_success_query(
        query_name='GetProjectExists',
        query_function=query_function,
        query_item=get_project_schema(include_runs=include_runs,),
        variables=[graphql_variable],
    )

    r = run_graphql_success_query(
        query=query,
        queryFunction=query_function,
        return_model_type=ProjectModel,
        variables=variables,
    )
    if r.success and r.item:
        return r.item
    print(f'Project with name: {project_name} not found')
    return None


def check_if_project_exists(project_name: str) -> bool:
    """Runs a GraphQL query to check if a named project already exists

    Args:
        project_name (str): Name of the project to check if it exists

    Returns:
        Returns a bool if it exists
    """
    project = get_project(project_name=project_name)
    return project is not None


def get_all_projects(include_runs: bool = False) -> List[ProjectModel]:
    """Runs a GraphQL query to get all projects

    Args:
        include_runs: Whether to include nested run objects in the query or not

    Returns:
        Returns a list of all Deserialized Project objects
    """
    query_function = 'getAllProjects'
    query = named_success_query(
        query_name='GetAllProjects',
        query_function=query_function,
        query_items=get_project_schema(include_runs=include_runs,),
    )

    r = run_graphql_success_query(
        query=query,
        queryFunction=query_function,
        return_model_type=ProjectModel,
    )
    return r.items if r.items else []


if __name__ == '__main__':
    fire.Fire({
        'get_all_projects': get_all_projects,
        'get_project': check_if_project_exists,
    })
