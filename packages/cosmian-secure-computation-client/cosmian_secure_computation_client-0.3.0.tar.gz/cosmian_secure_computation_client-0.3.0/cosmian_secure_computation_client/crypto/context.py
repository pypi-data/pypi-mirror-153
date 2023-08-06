"""cosmian_secure_computation_client.crypto.context module."""

from pathlib import Path
from typing import Optional, List

from cosmian_secure_computation_client.crypto.helper import (ed25519_keygen,
                                                             ed25519_seed_keygen,
                                                             ed25519_to_x25519_keypair,
                                                             encrypt,
                                                             decrypt,
                                                             encrypt_file,
                                                             decrypt_file,
                                                             encrypt_directory,
                                                             decrypt_directory,
                                                             random_symkey,
                                                             pubkey_fingerprint,
                                                             seal,
                                                             sign)


class CryptoContext:
    def __init__(self, seed: Optional[bytes] = None):
        self.ed25519_pk, self.ed25519_seed, self.ed25519_sk = (
            ed25519_keygen() if seed is None else
            ed25519_seed_keygen(seed)
        )  # type: bytes, bytes, bytes
        self.x25519_pk, self.x25519_sk = ed25519_to_x25519_keypair(
            self.ed25519_pk,
            self.ed25519_seed
        )  # type: bytes, bytes
        self.fingerprint: bytes = pubkey_fingerprint(self.ed25519_pk)
        self.ed25519_remote_pk: Optional[bytes] = None
        self.x25519_remote_pk: Optional[bytes] = None
        self._symkey: bytes = random_symkey()

    def set_keypair(self, public_key: bytes, private_key: bytes) -> None:
        self.ed25519_pk = public_key
        self.ed25519_sk = private_key
        self.x25519_pk, self.x25519_sk = ed25519_to_x25519_keypair(
            self.ed25519_pk,
            self.ed25519_seed
        )
        self.fingerprint = pubkey_fingerprint(self.ed25519_pk)

    def set_symkey(self, symkey: bytes) -> None:
        self._symkey = symkey

    @classmethod
    def from_path(cls, private_key_path: Path):
        pass

    @classmethod
    def from_pem(cls, private_key: str):
        pass

    def encrypt(self, data: bytes) -> bytes:
        return encrypt(data, self._symkey)

    def encrypt_file(self, path: Path) -> Path:
        return encrypt_file(path, self._symkey)

    def encrypt_directory(self, dir_path: Path, patterns: List[str],
                          exceptions: List[str], dir_exceptions: List[str],
                          out_dir_path: Path) -> bool:
        return encrypt_directory(dir_path, patterns, self._symkey,
                                 exceptions, dir_exceptions, out_dir_path)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        return decrypt(encrypted_data, self._symkey)

    def decrypt_file(self, path: Path) -> Path:
        return decrypt_file(path, self._symkey)

    def decrypt_directory(self, dir_path: Path) -> bool:
        return decrypt_directory(dir_path, self._symkey)

    def sign(self, data: bytes) -> bytes:
        return sign(data, self.ed25519_seed)

    def seal_symkey(self) -> bytes:
        if self.ed25519_remote_pk is None:
            raise Exception("Remote public key must be setup first!")

        return seal(self._symkey, self.ed25519_remote_pk)
