""" Delete the DB """
from mcli.api.engine.engine import run_graphql_request
from mcli.api.engine.utils import dedent_indent


def nuke_db() -> bool:
    """Runs a GraphQL query to wipe the DB

    Returns:
        Returns true if successful
    """

    query = dedent_indent("""
    mutation Mutation {
        nukeEverything
    }
    """)
    r = run_graphql_request(query=query,)
    success = r.get('data', {}).get('nukeEverything', False)
    return success
