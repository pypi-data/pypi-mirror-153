""" GraphQL Helper Objects """
from enum import Enum
from typing import NamedTuple

GraphQLVariableName = str
GraphQLVariableDataName = str


class GraphQLVariableType(Enum):
    STRING_REQUIRED = 'String!'
    STRING_OPTIONAL = 'String'
    CREATE_PROJECT_INPUT = 'CreateProjectInput!'
    UPDATE_PROJECT_INPUT = 'UpdateProjectInput!'
    CREATE_RUN_INPUT = 'CreateRunInput!'
    GET_ALL_RUNS_INPUT_OPTIONAL = 'GetAllRunsInput'
    GET_RUN_INPUT = 'GetRunInput!'
    UPDATE_RUN_INPUT = 'UpdateRunInput!'


class GraphQLQueryVariable(NamedTuple):
    variableName: GraphQLVariableName
    variableDataName: GraphQLVariableDataName
    variableType: GraphQLVariableType
