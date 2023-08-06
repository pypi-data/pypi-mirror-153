""" Test Platform """
import pytest


@pytest.mark.xfail
@pytest.mark.parametrize('priority_name', ('scavenge', 'standard', 'emergency'))
@pytest.mark.parametrize('platform_name', ('r1z1', 'r6z1'))
def test_get_specs_priority(
    platform_name: str,
    priority_name: str,
):
    """Test that r1z1 platform priorities get set properly within the resulting job spec

    Args:
        platform_name (str): Platform name
        priority_name (str): Priority class name
    """


@pytest.mark.xfail
@pytest.mark.parametrize('platform_name', ('r1z1', 'r6z1'))
def test_get_specs_priority_default(platform_name: str,):
    """Test that r1z1 platform priorities properly handle a priority of None as default

    Args:
        platform_name (str): Platform name
    """


@pytest.mark.xfail
@pytest.mark.parametrize('platform_name', ('aws-research-01', 'gcp'))
def test_get_specs_priority_none(platform_name: str,):
    """Test that a few platforms priorities properly handle a priority of None

    Args:
        platform_name (str): Name of the platform
    """


@pytest.mark.xfail
@pytest.mark.parametrize('platform_name', ('aws-research-01', 'r1z1', 'r6z1', 'gcp'))
def test_get_specs_priority_invalid(platform_name: str,):
    """Test that a few platforms priorities properly handle an incorrect priority name

    Args:
        platform_name (str): Name of the platform
    """


@pytest.mark.xfail
def test_ssh_secrets():
    """Test that SSH secrets are properly mounted
    """


@pytest.mark.xfail
def test_no_ssh_secrets():
    """Test that SSH secrets are not mounted when not requested
    """


@pytest.mark.xfail
def test_image_pull_secrets():
    """Test that image pull secrets are properly added
    """


@pytest.mark.xfail
def test_no_image_pull_secrets():
    """Test that no image pull secret is added if not requested
    """
