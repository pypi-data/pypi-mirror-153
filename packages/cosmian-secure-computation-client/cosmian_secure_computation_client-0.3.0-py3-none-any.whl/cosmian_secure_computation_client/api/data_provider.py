"""cosmian_secure_computation_client.api.data_provider module."""

from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple

import requests

from cosmian_secure_computation_client.api.side import Side
from cosmian_secure_computation_client.api.common import CommonAPI
from cosmian_secure_computation_client.api.computations import Computation

from cosmian_secure_computation_client.crypto.helper import encrypt

class DataProviderAPI(CommonAPI):
    def __init__(self, token: str) -> None:
        super().__init__(Side.DataProvider, token)

    def push_data(self, computation_uuid: str, symmetric_key: bytes, data_name: str, data: bytes) -> Computation:
        encrypted_data: bytes = encrypt(data, symmetric_key)

        resp: requests.Response = self.session.post(
            url=f"{self.url}/computations/{computation_uuid}/data",
            files={
                "file": (f"{data_name}.enc", encrypted_data, "application/octet-stream", {
                    "Expires": "0"
                })
            },
            timeout=None,
            headers={
                "Authorization": f"Bearer {self.access_token()}",
            },
        )

        if not resp.ok:
            raise Exception(
                f"Unexpected response ({resp.status_code}): {resp.content}"
            )

        return Computation.from_json_dict(resp.json())


    def push_files(self, computation_uuid: str, symmetric_key: bytes, paths: Iterable[Path]) -> Computation:
        for path in paths:
            if not path.is_file():
                raise FileNotFoundError

            resp = self.push_data(computation_uuid, symmetric_key, path.name, path.read_bytes())

        return resp

    def done(self, computation_uuid: str) -> Computation:
        resp: requests.Response = self.session.post(
            url=f"{self.url}/computations/{computation_uuid}/data/done",
            timeout=None,
            headers={
                "Authorization": f"Bearer {self.access_token()}",
            },
        )

        if not resp.ok:
            raise Exception(
                f"Unexpected response ({resp.status_code}): {resp.content}"
            )

        return Computation.from_json_dict(resp.json())

    def reset(self, computation_uuid: str) -> Computation:
        """Remove all data already uploaded by you."""

        resp: requests.Response = self.session.delete(
            url=f"{self.url}/computations/{computation_uuid}/data",
            timeout=None,
            headers={
                "Authorization": f"Bearer {self.access_token()}",
            },
        )

        if not resp.ok:
            raise Exception(
                f"Unexpected response ({resp.status_code}): {resp.content}"
            )

        return Computation.from_json_dict(resp.json())

