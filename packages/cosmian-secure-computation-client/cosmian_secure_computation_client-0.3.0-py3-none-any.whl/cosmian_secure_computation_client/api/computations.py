"""cosmian_secure_computation_client.api.computations module."""

from dataclasses import dataclass
from typing import Optional, Dict, Union, List, Tuple
from enum import Enum
from datetime import datetime
import inspect

class Role(Enum):
    ComputationOwner = 'ComputationOwner'
    CodeProvider = 'CodeProvider'
    DataProvider = 'DataProvider'
    ResultConsumer = 'ResultConsumer'

    def __str__(self) -> str:
        return f"{self.name}"


@dataclass(frozen=True)
class PublicKey:
    fingerprint: bytes
    content: str
    uploaded_at: str

    @staticmethod
    def from_json_dict(json):
        return construct_dataclass(PublicKey, json)

@dataclass(frozen=True)
class Owner:
    uuid: str
    email: str
    public_key: PublicKey
    manifest_signature: Optional[str]

    @staticmethod
    def from_json_dict(json):
        json['public_key'] = PublicKey.from_json_dict(json['public_key'])

        return construct_dataclass(Owner, json)

@dataclass(frozen=True)
class CodeProvider:
    uuid: str
    email: str
    public_key: Optional[PublicKey]
    code_uploaded_at: Optional[str]
    symmetric_key_uploaded_at: Optional[str]

    @staticmethod
    def from_json_dict(json):
        json['public_key'] = None if json['public_key'] is None else PublicKey.from_json_dict(json['public_key'])

        return construct_dataclass(CodeProvider, json)

@dataclass(frozen=True)
class DataProvider:
    uuid: str
    email: str
    public_key: Optional[PublicKey]
    starting_uploading_at: Optional[str]
    done_uploading_at: Optional[str]
    symmetric_key_uploaded_at: Optional[str]

    @staticmethod
    def from_json_dict(json):
        json['public_key'] = None if json['public_key'] is None else PublicKey.from_json_dict(json['public_key'])

        return construct_dataclass(DataProvider, json)

@dataclass(frozen=True)
class ResultConsumer:
    uuid: str
    email: str
    public_key: Optional[PublicKey]
    symmetric_key_uploaded_at: Optional[str]
    result_downloaded_at: Optional[str]

    @staticmethod
    def from_json_dict(json):
        json['public_key'] = None if json['public_key'] is None else PublicKey.from_json_dict(json['public_key'])

        return construct_dataclass(ResultConsumer, json)

@dataclass(frozen=True)
class EnclaveIdentity:
    public_key: bytes
    manifest: Optional[str]  # Some endpoints omit the manifest in the response for performance reasons, please call `get_computation()` to fetch it
    quote: str

    @staticmethod
    def from_json_dict(json):
        json['public_key'] = bytes(json['public_key'])

        return construct_dataclass(EnclaveIdentity, json)

@dataclass(frozen=True)
class Enclave:
    identity: Optional[EnclaveIdentity]

    @staticmethod
    def from_json_dict(json):
        json['identity'] = None if json['identity'] is None else EnclaveIdentity.from_json_dict(json['identity'])

        return construct_dataclass(Enclave, json)

@dataclass(frozen=True)
class CurrentRun:
    created_at: str

    @staticmethod
    def from_json_dict(json):
        return construct_dataclass(CurrentRun, json)

@dataclass(frozen=True)
class PreviousRun:
    created_at: str
    ended_at: str
    exit_code: int
    stdout: str
    stderr: str
    results_fetches_datetimes_by_result_consumers_uuid: Dict[str, str]

    @staticmethod
    def from_json_dict(json):
        return construct_dataclass(PreviousRun, json)


@dataclass(frozen=True)
class Runs:
    current: Optional[CurrentRun]
    previous: List[PreviousRun]

    @staticmethod
    def from_json_dict(json):
        json['current'] = None if json['current'] is None else CurrentRun.from_json_dict(json['current'])
        json['previous'] = list(map(PreviousRun.from_json_dict, json['previous']))

        return construct_dataclass(Runs, json)


@dataclass(frozen=True)
class Computation:
    uuid: str
    name: str
    owner: Owner
    code_provider: CodeProvider
    data_providers: List[DataProvider]
    result_consumers: List[ResultConsumer]
    enclave: Enclave
    runs: Runs
    my_roles: List[Role]
    created_at: str

    @staticmethod
    def from_json_dict(json):
        json['owner'] = Owner.from_json_dict(json['owner'])
        json['code_provider'] = CodeProvider.from_json_dict(json['code_provider'])
        json['data_providers'] = list(map(DataProvider.from_json_dict, json['data_providers']))
        json['result_consumers'] = list(map(ResultConsumer.from_json_dict, json['result_consumers']))
        json['enclave'] = Enclave.from_json_dict(json['enclave'])
        json['runs'] = Runs.from_json_dict(json['runs'])
        json['my_roles'] = list(map(Role, json['my_roles']))

        return construct_dataclass(Computation, json)


def construct_dataclass(dataclass, json):
    sig = inspect.signature(dataclass)
    filter_keys = [param.name for param in sig.parameters.values() if param.kind == param.POSITIONAL_OR_KEYWORD]
    filtered_dict = {filter_key:json.get(filter_key, None) for filter_key in filter_keys}
    return dataclass(**filtered_dict)
