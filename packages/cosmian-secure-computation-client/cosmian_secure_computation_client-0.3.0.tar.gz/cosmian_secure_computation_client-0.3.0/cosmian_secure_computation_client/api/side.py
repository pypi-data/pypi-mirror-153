"""cosmian_secure_computation_client.api.side module."""

from enum import Enum


class Side(Enum):
    Owner = 0
    Enclave = 1
    CodeProvider = 2
    DataProvider = 3
    ResultConsumer = 4

    def __str__(self) -> str:
        return f"{self.name}"
