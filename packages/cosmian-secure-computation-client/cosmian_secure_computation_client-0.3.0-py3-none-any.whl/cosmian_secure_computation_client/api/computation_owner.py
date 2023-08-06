"""cosmian_secure_computation_client.api.computation_owner module."""

from pathlib import Path
import tempfile
from typing import Optional, Dict, List, Tuple

import requests

from cosmian_secure_computation_client.api.side import Side
from cosmian_secure_computation_client.api.common import CommonAPI
from cosmian_secure_computation_client.api.computations import Computation


class ComputationOwnerAPI(CommonAPI):
    def __init__(self, token: str) -> None:
        super().__init__(Side.Owner, token)

    def create_computation(self, name: str, owner_public_key: str, code_provider_email: str, data_providers_emails: List[str], result_consumers_emails: List[str]) -> Computation:
        resp: requests.Response = self.session.post(
            url=f"{self.url}/computations",
            json={
                "name": name,
                "code_provider_email": code_provider_email,
                "data_providers_emails": data_providers_emails,
                "result_consumers_emails": result_consumers_emails,
                "owner_public_key": owner_public_key,
            },
            headers={
                "Authorization": f"Bearer {self.access_token()}",
            },
        )

        if not resp.ok:
            raise Exception(
                f"Unexpected response ({resp.status_code}): {resp.content}"
            )

        return Computation.from_json_dict(resp.json())

    def approve_participants(self, computation_uuid: str, signature: str) -> Computation:
        resp: requests.Response = self.session.post(
            url=f"{self.url}/computations/{computation_uuid}/approve/participants",
            json={
                "signature": signature,
            },
            headers={
                "Authorization": f"Bearer {self.access_token()}",
            },
        )

        if not resp.ok:
            raise Exception(
                f"Unexpected response ({resp.status_code}): {resp.content}"
            )

        return Computation.from_json_dict(resp.json())
