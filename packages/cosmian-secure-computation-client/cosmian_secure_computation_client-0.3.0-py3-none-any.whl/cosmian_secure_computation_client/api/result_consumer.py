"""cosmian_secure_computation_client.api.result_consumer module."""

from typing import Optional, Tuple

import requests

from cosmian_secure_computation_client.api.side import Side
from cosmian_secure_computation_client.api.common import CommonAPI


class ResultConsumerAPI(CommonAPI):
    def __init__(self, token: str) -> None:
        super().__init__(Side.ResultConsumer, token)

    def fetch_results(self, computation_uuid: str) -> Optional[bytes]:
        resp: requests.Response = self.session.get(
            url=f"{self.url}/computations/{computation_uuid}/results",
            headers={
                "Authorization": f"Bearer {self.access_token()}",
            },
        )

        if resp.status_code == requests.codes.accepted:
            return None

        if not resp.ok:
            raise Exception(
                f"Unexpected response ({resp.status_code}): {resp.content}"
            )

        try:
            # The old version of the API could return a JSON response with the result hex encoded
            # it should never be the case for new computations.
            # This code should be remove in a few days when all the old computations are archived.
            return bytes.fromhex(resp.json()["message"])
        except requests.JSONDecodeError:
            return resp.content