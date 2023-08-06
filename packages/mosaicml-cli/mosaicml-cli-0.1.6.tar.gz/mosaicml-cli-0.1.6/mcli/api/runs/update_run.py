""" Update a Run. For example, stop or delete a run. """
from typing import Optional

from mcli.api.engine.engine import run_graphql_success_query
from mcli.api.model.run_model import RunModel, RunStatus, get_run_schema
from mcli.api.schema.query import named_success_query
from mcli.api.types import GraphQLQueryVariable, GraphQLVariableType


def stop_run(run_uid: Optional[str] = None, run_name: Optional[str] = None) -> bool:
    """Runs a GraphQL query to stop a run.

    At least one of `run_uid` or `run_name` must be provided to stop a run.

    Args:
        run_uid (str, optional): The uid of the run to stop
        run_name (str, optional): The name of the run to stop

    Returns:
        Returns true if successful
    """

    if run_uid is None and run_name is None:
        print('Must provide at least one of run_uid or run_name to stop a run.')
        return False

    query_function = 'updateRun'
    update_variable_data_name = '$updateRunInput'
    get_variable_data_name = '$getRunInput'

    variables = {
        update_variable_data_name: {
            'runStatus': RunStatus.STOPPED.value
        },
        get_variable_data_name: {
            'runUid': run_uid,
            'runName': run_name
        }
    }

    update_graphql_variable: GraphQLQueryVariable = GraphQLQueryVariable(
        variableName='updateRunData',
        variableDataName=update_variable_data_name,
        variableType=GraphQLVariableType.UPDATE_RUN_INPUT,
    )
    get_graphql_variable: GraphQLQueryVariable = GraphQLQueryVariable(
        variableName='getRunData',
        variableDataName=get_variable_data_name,
        variableType=GraphQLVariableType.GET_RUN_INPUT,
    )

    query = named_success_query(
        query_name='StopRun',
        query_function=query_function,
        query_item=get_run_schema(),
        variables=[update_graphql_variable, get_graphql_variable],
        is_mutation=True,
    )

    response = run_graphql_success_query(
        query=query,
        queryFunction=query_function,
        return_model_type=RunModel,
        variables=variables,
    )
    return response.success
