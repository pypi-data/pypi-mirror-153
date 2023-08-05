from typing import Sequence, Union, List
from solders.pubkey import Pubkey

class AccountMeta:
    def __init__(self, pubkey: Pubkey, is_signer: bool, is_writable: bool) -> None: ...
    @property
    def pubkey(self) -> Pubkey: ...
    @property
    def is_signer(self) -> bool: ...
    @property
    def is_writable(self) -> bool: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __richcmp__(self, other: "AccountMeta", op: int) -> bool: ...

class Instruction:
    def __init__(
        self, program_id: Pubkey, data: bytes, accounts: Sequence[AccountMeta]
    ) -> None: ...
    @property
    def program_id(self) -> Pubkey: ...
    @property
    def data(self) -> bytes: ...
    @property
    def accounts(self) -> List[AccountMeta]: ...
    @accounts.setter
    def accounts(self, accounts: List[AccountMeta]) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "Instruction", op: int) -> bool: ...
    def __bytes__(self) -> bytes: ...
    @staticmethod
    def from_bytes(data: bytes) -> "Instruction": ...

class CompiledInstruction:
    def __init__(self, program_id_index: int, data: bytes, accounts: bytes) -> None: ...
    def program_id(self, program_ids: Sequence[Pubkey]) -> Pubkey: ...
    @property
    def program_id_index(self) -> int: ...
    @property
    def accounts(self) -> bytes: ...
    @accounts.setter
    def accounts(self, accounts: Union[bytes, Sequence[int]]) -> None: ...
    @property
    def data(self) -> bytes: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def __richcmp__(self, other: "CompiledInstruction", op: int) -> bool: ...
    def __bytes__(self) -> bytes: ...
    @staticmethod
    def from_bytes(data: bytes) -> "CompiledInstruction": ...
