""" Project Schema """
from mcli.api.engine.utils import dedent_indent


def get_project_schema(
    include_runs: bool = False,
    indentation: int = 2,
):
    """ Get the GraphQL schema for a :type ProjectModel:

    Args:
        include_runs (boolean): Whether to include the runs nested in the project or not
        indentation (int): Optional[int] for the indentation of the block
        nil:

    Returns:
        Returns a GraphQL string with all the fields needed to initialize a
        :type ProjectModel:
    """
    del include_runs
    return dedent_indent(
        """
projectName
image
createdBy
wandbScratch
cluster
wandbProject
instance
model
branch
repo
lastUpdatedTimestamp
creationTimestamp
        """, indentation)
