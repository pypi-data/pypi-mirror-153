""" GraphQL Update Project Query """
from __future__ import annotations

from typing import TYPE_CHECKING

from mcli.api.engine.engine import run_graphql_success_query
from mcli.api.schema.project import get_project_schema
from mcli.api.schema.query import named_success_query
from mcli.api.types import GraphQLQueryVariable, GraphQLVariableType
from mcli.models.project import ProjectModel

if TYPE_CHECKING:
    from mcli.models import ProjectConfig


def update_project(project: ProjectConfig,) -> bool:
    """Runs a GraphQL query to update a project from a ProjectConfig

    Args:
        project (ProjectConfig): The :type ProjectConfig: to update

    Returns:
        Returns true if successful
    """
    query_function = 'updateProject'
    variable_data_name = '$updateProjectData'
    variables = {
        variable_data_name: project.to_update_project_data(),
    }
    graphql_variable: GraphQLQueryVariable = GraphQLQueryVariable(
        variableName='updateProjectData',
        variableDataName=variable_data_name,
        variableType=GraphQLVariableType.UPDATE_PROJECT_INPUT,
    )

    query = named_success_query(
        query_name='UpdateProject',
        query_function=query_function,
        query_item=get_project_schema(include_runs=False,),
        variables=[graphql_variable],
        is_mutation=True,
    )

    r = run_graphql_success_query(
        query=query,
        queryFunction=query_function,
        return_model_type=ProjectModel,
        variables=variables,
    )
    return r.success
