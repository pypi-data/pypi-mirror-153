""" GraphQL Query Helpers """
from typing import List, Optional

from mcli.api.engine.utils import dedent_indent
from mcli.api.types import GraphQLQueryVariable


def named_success_query(
    query_name: str,
    query_function: str,
    query_item: Optional[str] = None,
    query_items: Optional[str] = None,
    variables: Optional[List[GraphQLQueryVariable]] = None,
    is_mutation: bool = False,
) -> str:
    """Generates a Success Style Query for GraphQL

    Args:
        query_name: THe name of the query (used for tracking purposes)
        query_function: The function that the GraphQL query should be calling
        query_item: An optional str for the fields needed to return a :type
            DeserializableModel:
        query_items: An optional str for the fields needed to return a list of
            :type DeserializableModel:
        variables: If the query takes variables, include them as a :type
            List[GraphQLQueryVariable]: to be passed to the function
        nil:

    Returns:
        The full GraphQL query string
    """
    success_query = _success_query(
        query_item=query_item,
        query_items=query_items,
    )
    query_function_call = _query_function_call(
        query_resolver_name=query_function,
        query_return_parameters=success_query,
        variables=variables,
    )
    named_query = _named_query(
        query_name=query_name,
        query_function=query_function_call,
        is_mutation=is_mutation,
        variables=variables,
    )
    return named_query


def _named_query(
    query_name: str,
    query_function: str,
    variables: Optional[List[GraphQLQueryVariable]] = None,
    is_mutation: bool = False,
    indentation: int = 0,
) -> str:
    variables_string = ''
    if variables:
        variables_string = '(' + ', '.join([f'{data_name}: {var_type.value}' for _, data_name, var_type in variables
                                           ]) + ')'

    query_type = 'query' if not is_mutation else 'mutation'
    query = dedent_indent(
        f"""
{query_type} {query_name}{variables_string} {{
{query_function}
}}
        """,
        indentation,
    )
    return query


def _query_function_call(
    query_resolver_name: str,
    query_return_parameters,
    variables: Optional[List[GraphQLQueryVariable]] = None,
    indentation: int = 2,
) -> str:
    variables_string = ''
    if variables:
        variables_string = '(' + ', '.join([f'{var_name}: {data_name}' for var_name, data_name, _ in variables]) + ')'

    query = dedent_indent(
        f"""
{query_resolver_name}{variables_string} {{
{query_return_parameters}
}}
        """,
        indentation,
    )
    return query


def _success_query(
    query_item: Optional[str],
    query_items: Optional[str] = None,
    indentation: int = 2,
) -> str:
    query = dedent_indent(
        """
success
message
messageLong""",
        indentation,
    )
    if query_item:
        query += '\n' + dedent_indent(
            f"""
item {{
{query_item}
}}
            """,
            indentation,
        )
    if query_items:
        query += '\n' + dedent_indent(
            f"""
items {{
{query_items}
}}
            """,
            indentation,
        )
    return query
