""" GraphQL Query Engine """
import json
from typing import Any, Dict, Optional, Type

import requests

from mcli import config
from mcli.api.schema.query_models import SuccessResponse, T_DeserializableModel, UnserializedSuccessResponse


def run_graphql_success_query(
    query: str,
    # pylint: disable-next=invalid-name
    queryFunction: str,
    return_model_type: Optional[Type[T_DeserializableModel]] = None,
    variables: Optional[Dict[str, Any]] = None,
) -> SuccessResponse[T_DeserializableModel]:
    response = run_graphql_request(query=query, variables=variables)
    try:
        data = response['data']
        query_response: Dict[str, Any] = data[queryFunction]
        query_response['model_type'] = return_model_type
        success_query = UnserializedSuccessResponse(**query_response)

        return success_query.deserialize()
    except Exception as e:  # pylint: disable=broad-except
        if 'errors' in response:
            error_message = ''
            for error in response['errors']:
                error_message += error['message'] + '\n'
            if error_message == '':
                error_message = 'Unknown GraphQL Error Message'
            raise Exception(f'GraphQL Exception:\n\n{error_message}') from e
        else:
            print(f'Failed to run query: {queryFunction}')
            raise e


def run_graphql_request(
    query: str,
    variables: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if variables is None:
        variables = {}
    renamed_variables = {}
    for key, value in variables.items():
        renamed_variables[key.replace('$', '')] = value
    variables = renamed_variables
    headers = {
        'Content-Type': 'application/json',
        'authorization': config.MCLIConfig.load_config().MOSAICML_API_KEY,
    }
    payload = json.dumps({'query': query, 'variables': variables})
    response = requests.request(
        'POST',
        config.MOSAICML_API_ENDPOINT,
        headers=headers,
        data=payload,
    )
    return response.json()
