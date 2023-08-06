""" Get runs """
from typing import List, Optional

from mcli.api.engine.engine import run_graphql_success_query
from mcli.api.model.run_model import RunModel, get_run_schema
from mcli.api.schema.query import named_success_query
from mcli.api.types import GraphQLQueryVariable, GraphQLVariableType


def get_runs(include_deleted: bool = False) -> Optional[List[RunModel]]:
    """Runs a GraphQL query to get all runs for the authenticated user.

    Args:
        include_deleted (bool): ``True`` to include deleted runs ``False``
            to not include deleted runs

    Returns:
        List[GraphQLRunType]: The list of runs
    """
    query_function = 'getAllRuns'
    variable_data_name = '$getAllRunsInput'
    variables = {
        variable_data_name: {
            'includeDeleted': include_deleted,
        },
    }
    graphql_variable: GraphQLQueryVariable = GraphQLQueryVariable(
        variableName='getAllRunsData',
        variableDataName=variable_data_name,
        variableType=GraphQLVariableType.GET_ALL_RUNS_INPUT_OPTIONAL,
    )

    query = named_success_query(
        query_name='GetAllRuns',
        query_function=query_function,
        query_items=get_run_schema(),
        variables=[graphql_variable],
        is_mutation=False,
    )

    response = run_graphql_success_query(
        query=query,
        queryFunction=query_function,
        return_model_type=RunModel,
        variables=variables,
    )

    if not response.success or response.items is None:
        print(f'Failed to get runs: {response.message}')
        return None

    return response.items
