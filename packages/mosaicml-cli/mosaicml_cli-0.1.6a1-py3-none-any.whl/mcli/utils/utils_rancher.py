"""Helper functions for kubeconfig autopop from Rancher"""
import json
from typing import List, NamedTuple, Optional

import requests
import yaml

from mcli.config import MCLI_CONFIG_DIR, MCLI_KUBECONFIG


class ClusterInfo(NamedTuple):
    id: str
    name: str


class ProjectInfo(NamedTuple):
    id: str
    name: str
    cluster: str
    display_name: str


_MESSAGE_401 = 'Unauthorized. Check your Rancher auth token and try again'  # pylint: disable=invalid-name
_MESSAGE_404 = 'Invalid URL. Check your Rancher endpoint and try again'  # pylint: disable=invalid-name
# pylint: disable=invalid-name
_MESSAGE_403 = 'Forbidden. Try creating a new auth token. If the issue persists, notify your cluster administrator.'
# pylint: disable=invalid-name
_MESSAGE_500 = 'Server error. Rancher had an issue processing your request. Please notify your cluster administrator.'


def retrieve_clusters(
    endpoint: str,
    auth_token: str,
) -> List[ClusterInfo]:

    _GET_CLUSTER_MESSAGE = 'Error retrieving cluster info'

    headers = {'Authorization': 'Bearer ' + auth_token}

    resp = requests.request('GET', endpoint + '/v3/clusters', headers=headers)

    if resp.status_code == 401:
        raise RuntimeError(f'{_GET_CLUSTER_MESSAGE}: {_MESSAGE_401}')

    if resp.status_code == 404:
        raise RuntimeError(f'{_GET_CLUSTER_MESSAGE}: {_MESSAGE_404}')

    return [ClusterInfo(item['id'], item['name']) for item in resp.json()['data'] if item['state'] == 'active']


def generate_cluster_config(
    endpoint: str,
    auth_token: str,
    clusters: List[ClusterInfo],
    namespace: Optional[str] = None,
):

    headers = {'Authorization': 'Bearer ' + auth_token}

    MCLI_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if MCLI_KUBECONFIG.exists():
        with open(MCLI_KUBECONFIG, 'r', encoding='utf-8') as f:
            kubeconfig = yaml.safe_load(f)
    else:
        kubeconfig = {
            'apiVersion': 'v1',
            'kind': 'Config',
            'clusters': [],
            'users': [],
            'contexts': [],
        }

    for cluster in clusters:
        updated_cluster = False
        updated_user = False
        updated_context = False

        if cluster.id == 'local':
            continue

        resp = requests.request('POST',
                                endpoint + '/v3/clusters/' + cluster.id + '?action=generateKubeconfig',
                                headers=headers)

        _GET_KUBECONFIG_MESSAGE = f'Error creating kubeconfig for cluster {cluster.name}'
        if resp.status_code == 401:
            raise RuntimeError(f'{_GET_KUBECONFIG_MESSAGE}: {_MESSAGE_404}')

        if resp.status_code == 404:
            raise RuntimeError(f'{_GET_KUBECONFIG_MESSAGE}: {_MESSAGE_404}')

        if resp.status_code == 500:
            raise RuntimeError(f'{_GET_KUBECONFIG_MESSAGE}: {_MESSAGE_500}')

        config = yaml.safe_load(resp.json()['config'])

        if namespace:
            config['contexts'][0]['context']['namespace'] = namespace

        for cl in kubeconfig['clusters']:
            if cl['name'] == config['clusters'][0]['name']:
                cl['cluster'] = config['clusters'][0]['cluster']
                updated_cluster = True
                break
        for cl in kubeconfig['users']:
            if cl['name'] == config['users'][0]['name']:
                cl['user'] = config['users'][0]['user']
                updated_user = True
                break
        for cl in kubeconfig['contexts']:
            if cl['name'] == config['contexts'][0]['name']:
                cl['context'] = config['contexts'][0]['context']
                updated_context = True
                break

        if not updated_cluster:
            kubeconfig['clusters'].append(config['clusters'][0])

        if not updated_user:
            kubeconfig['users'].append(config['users'][0])

        if not updated_context:
            kubeconfig['contexts'].append(config['contexts'][0])

        kubeconfig.setdefault('current-context', kubeconfig['contexts'][0]['name'])

        with open(MCLI_KUBECONFIG, 'w', encoding='utf-8') as f:
            yaml.safe_dump(kubeconfig, f)


def retrieve_projects(
    endpoint: str,
    auth_token: str,
) -> List[ProjectInfo]:

    headers = {'Authorization': 'Bearer ' + auth_token}

    resp = requests.request('GET', endpoint + '/v3/projects', headers=headers)

    _GET_PROJECTS_MESSAGE = 'Error getting available projects'
    if resp.status_code == 401:
        raise RuntimeError(f'{_GET_PROJECTS_MESSAGE}: {_MESSAGE_401}')

    if resp.status_code == 404:
        raise RuntimeError(f'{_GET_PROJECTS_MESSAGE}: {_MESSAGE_404}')

    return [
        ProjectInfo(proj['id'], proj['id'].split(':')[1], proj['id'].split(':')[0], proj['name'])
        for proj in resp.json()['data']
    ]


def configure_namespaces(
    endpoint: str,
    auth_token: str,
    projects: List[ProjectInfo],
    namespace_name: str,
):
    headers = {'Authorization': 'Bearer ' + auth_token}

    for project in projects:
        payload = {
            'type': 'namespace',
            'metadata': {
                'annotations': {
                    'field.cattle.io/containerDefaultResourceLimit': '{}',
                },
                'labels': {},
            },
            'disableOpenApiValidation': False
        }

        payload['metadata']['annotations']['field.cattle.io/projectId'] = project.id
        payload['metadata']['labels']['field.cattle.io/projectId'] = project.name
        payload['metadata']['name'] = namespace_name

        resp = requests.request('POST',
                                endpoint + '/k8s/clusters/' + project.cluster + '/v1/namespaces',
                                headers=headers,
                                data=json.dumps(payload))

        _CREATE_NAMESPACE_MESSAGE = f'Error creating namespace {namespace_name} on cluster {project.cluster}'
        if resp.status_code == 401:
            raise RuntimeError(f'{_CREATE_NAMESPACE_MESSAGE}: {_MESSAGE_401}')

        if resp.status_code == 403:
            raise RuntimeError(f'{_CREATE_NAMESPACE_MESSAGE}: {_MESSAGE_403}')

        if resp.status_code == 404:
            raise RuntimeError(f'{_CREATE_NAMESPACE_MESSAGE}: {_MESSAGE_404}')

        if resp.status_code == 500:
            raise RuntimeError(f'{_CREATE_NAMESPACE_MESSAGE}: {_MESSAGE_500}')
