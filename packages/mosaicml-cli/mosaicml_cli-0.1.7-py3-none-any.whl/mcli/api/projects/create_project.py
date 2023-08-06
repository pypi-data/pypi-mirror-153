""" Create a Project """
from mcli.api.engine.engine import run_graphql_success_query
from mcli.api.schema.project import get_project_schema
from mcli.api.schema.query import named_success_query
from mcli.api.types import GraphQLQueryVariable, GraphQLVariableType
from mcli.models.project import ProjectModel


def create_project(project: ProjectModel,) -> bool:
    """Runs a GraphQL query to create a new project from a ProjectModel

    Args:
        project (ProjectModel): The :type ProjectModel: to persist

    Returns:
        Returns true if successful
    """
    query_function = 'createProject'
    variable_data_name = '$createProjectData'
    variables = {
        variable_data_name: project.to_create_project_data(),
    }
    graphql_variable: GraphQLQueryVariable = GraphQLQueryVariable(
        variableName='createProjectData',
        variableDataName=variable_data_name,
        variableType=GraphQLVariableType.CREATE_PROJECT_INPUT,
    )

    query = named_success_query(
        query_name='CreateProject',
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
