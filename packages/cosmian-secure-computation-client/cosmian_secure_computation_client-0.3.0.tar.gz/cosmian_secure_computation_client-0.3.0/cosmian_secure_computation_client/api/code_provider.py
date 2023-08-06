"""cosmian_secure_computation_client.api.code_provider module."""

from pathlib import Path
import tempfile
from typing import Optional, Dict, List, Tuple

import requests

from cosmian_secure_computation_client.util.fs import tar
from cosmian_secure_computation_client.api.side import Side
from cosmian_secure_computation_client.api.common import CommonAPI
from cosmian_secure_computation_client.crypto.helper import encrypt_directory
from cosmian_secure_computation_client.api.computations import Computation


class CodeProviderAPI(CommonAPI):
    def __init__(self, token: str) -> None:
        super().__init__(Side.CodeProvider, token)

    def upload_tar(self, computation_uuid: str, tar_path: Path, keep: bool = True) -> Dict[str, str]:
        if not tar_path.exists():
            raise FileNotFoundError("Can't find tar file!")

        with tar_path.open("rb") as fp:
            resp: requests.Response = self.session.post(
                url=f"{self.url}/computations/{computation_uuid}/code",
                files={
                    "file": (tar_path.name, fp, "application/tar", {
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

        if not keep:
            tar_path.unlink()

        return resp.json()

    def upload(self, computation_uuid: str, symmetric_key: bytes, directory_path: Path, patterns: List[str] = ["*"], files_exceptions: List[str] = [], directories_exceptions: List[str] = [".git"]):
        # TODO rename files_exceptions and directories_exceptions to better reflect it's encryption exceptions and not upload exceptions

        entrypoint = directory_path / "run.py"
        if not entrypoint.exists():
            raise FileNotFoundError(f"Can't upload {directory_path.resolve()} as code because `run.py` is missing.")

        encrypted_directory_path: Path = Path(tempfile.gettempdir()) / f"cosmian_{computation_uuid}" / directory_path.name
        encrypt_directory(
            dir_path = directory_path,
            key = symmetric_key,
            patterns = patterns,
            exceptions = files_exceptions + ["run.py"],
            dir_exceptions = directories_exceptions,
            out_dir_path = encrypted_directory_path
        )
        tar_path = tar(encrypted_directory_path, encrypted_directory_path / f"{encrypted_directory_path.name}.tar")

        return self.upload_tar(computation_uuid, tar_path, keep=False)

    def reset(self, computation_uuid: str) -> Computation:
        """Remove the uploaded code. This will reset the enclave identity so every participants will need to send their symetric keys again sealed with the new enclave public key. The data can be left untouch if the data providers resend the same symetric key."""

        resp: requests.Response = self.session.delete(
            url=f"{self.url}/computations/{computation_uuid}/code",
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