from tempfile import TemporaryDirectory
from typing import Optional, Tuple, Any

from .rust_pyspec_glue import lib, ffi

class DB:
    def __init__(self, path: Optional[str]) -> None:
        if path is None:
            self.db = lib.open_in_memory()
        else:
            self.db = lib.open(ffi.from_buffer(path.encode("ascii")), len(path))
        self.tx = None

    def __del__(self) -> None:
        if self.tx is not None:
            lib.rollback_mutable(self.tx)
            self.tx = None
        if self.db is not None:
            lib.drop_db(self.db)
            self.db = None

    def close(self) -> None:
        if self.tx is not None:
            self.rollback_mutable()
        if self.db is None:
            raise Exception("Already closed")
        lib.drop_db(self.db)
        self.db = None

    def begin_mutable(self) -> None:
        if self.tx is not None:
            raise Exception("Transaction already in progress")
        self.tx = lib.begin_mutable(self.db)

    def rollback_mutable(self) -> None:
        if self.tx is None:
            raise Exception("No transaction in progress")
        lib.rollback_mutable(self.tx)
        self.tx = None

    def commit_mutable(self) -> None:
        if self.tx is None:
            raise Exception("No transaction in progress")
        lib.commit_mutable(self.tx)
        self.tx = None

    def set_metadata(self, key: bytes, value: bytes) -> None:
        if self.tx is None:
            raise Exception("No transaction in progress")
        lib.set_metadata(
            self.tx, ffi.from_buffer(key), len(key), ffi.from_buffer(value), len(value)
        )

    def get_metadata(self, key: bytes) -> Optional[bytes]:
        if self.tx is None:
            raise Exception("No transaction in progress")
        metadata = lib.get_metadata(self.tx, ffi.from_buffer(key), len(key))
        if not metadata.exists:
            return None
        else:
            return bytes(ffi.buffer(metadata.value, metadata.value_len))

    def state_root(self) -> bytes:
        if self.tx is None:
            raise Exception("No transaction in progress")
        return bytes(ffi.buffer(lib.state_root(self.tx), 32))

    def storage_root(self, address: bytes) -> bytes:
        if self.tx is None:
            raise Exception("No transaction in progress")
        assert len(address) == 20
        return bytes(ffi.buffer(lib.storage_root(self.tx, ffi.from_buffer(address)), 32))

    def set_account(self, address: bytes, account: Optional[Any]) -> None:
        if self.tx is None:
            raise Exception("No transaction in progress")
        assert len(address) == 20
        if account is None:
            lib.set_account_none(self.tx, ffi.from_buffer(address))
        else:
            lib.set_account_some(
                self.tx,
                ffi.from_buffer(address),
                account.nonce,
                ffi.from_buffer(account.balance.to_bytes(32, "big")),
                ffi.from_buffer(account.code),
                len(account.code),
            )

    def get_account_optional(self, address: bytes) -> Optional[Tuple[int, int, bytes]]:
        if self.tx is None:
            raise Exception("No transaction in progress")
        assert len(address) == 20
        account = lib.get_account_optional(self.tx, ffi.from_buffer(address))
        if not account.exists:
            return None
        else:
            return (
                account.nonce,
                int.from_bytes(ffi.buffer(account.balance, 32), "big"),
                bytes(ffi.buffer(account.code, account.code_len)),
            )

    def set_storage(self, address: bytes, key: bytes, value: int) -> None:
        if self.tx is None:
            raise Exception("No transaction in progress")
            assert len(address) == 20
            assert len(key) == 32
        lib.set_storage(
            self.tx,
            ffi.from_buffer(address),
            ffi.from_buffer(key),
            ffi.from_buffer(value.to_bytes(32, "big")),
        )

    def get_storage(self, address: bytes, key: bytes) -> int:
        if self.tx is None:
            raise Exception("No transaction in progress")
        assert len(address) == 20
        assert len(key) == 32
        return int.from_bytes(
            ffi.buffer(
                lib.get_storage(
                    self.tx, ffi.from_buffer(address), ffi.from_buffer(key)
                ),
                32,
            ),
            "big",
        )

    def destroy_storage(self, address: bytes) -> None:
        if self.tx is None:
            raise Exception("No transaction in progress")
        lib.destroy_storage(self.tx, ffi.from_buffer(address))

    def debug_dump(self) -> None:
        if self.tx is None:
            raise Exception("No transaction in progress")
        lib.debug_dump(self.tx)
