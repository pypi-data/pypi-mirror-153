""" Provides typing for Lazy Loaded Service Class """
from __future__ import annotations

from kubernetes import client


class MCLIK8sService(client.V1Service):

    @property
    def metadata(self) -> client.V1ObjectMeta:
        if self._metadata is None:
            self._metadata = client.V1ObjectMeta()
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: client.V1ObjectMeta) -> None:
        self._metadata = metadata
