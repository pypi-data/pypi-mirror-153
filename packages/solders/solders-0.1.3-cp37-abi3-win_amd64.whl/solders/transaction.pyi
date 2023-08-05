from typing import Sequence, Union, List, Optional, Tuple
from solders.keypair import Keypair
from solders.presigner import Presigner
from solders.message import Message
from solders.signature import Signature
from solders.instruction import Instruction, CompiledInstruction
from solders.pubkey import Pubkey
from solders.hash import Hash

class Transaction:
    def __init__(
        self,
        from_keypairs: Sequence[Union[Presigner, Keypair]],
        message: Message,
        recent_blockhash: Hash,
    ) -> None: ...
    @property
    def signatures(self) -> List[Signature]: ...
    @property
    def message(self) -> Message: ...
    @staticmethod
    def new_unsigned(message: Message) -> "Transaction": ...
    @staticmethod
    def new_with_payer(
        instructions: Sequence[Instruction],
        payer: Optional[Pubkey] = None,
    ) -> "Transaction": ...
    @staticmethod
    def new_signed_with_payer(
        instructions: Sequence[Instruction],
        payer: Optional[Pubkey],
        signing_keypairs: Sequence[Union[Presigner, Keypair]],
        recent_blockhash: Hash,
    ) -> "Transaction": ...
    @staticmethod
    def new_with_compiled_instructions(
        from_keypairs: Sequence[Union[Presigner, Keypair]],
        keys: Sequence[Pubkey],
        recent_blockhash: Hash,
        program_ids: Sequence[Pubkey],
        instructions: Sequence[CompiledInstruction],
    ) -> "Transaction": ...
    @staticmethod
    def populate(
        message: Message, signatures: Sequence[Signature]
    ) -> "Transaction": ...
    def data(self, instruction_index: int) -> bytes: ...
    def key(self, instruction_index: int, accounts_index: int) -> Optional[Pubkey]: ...
    def signer_key(
        self, instruction_index: int, accounts_index: int
    ) -> Optional[Pubkey]: ...
    def message_data(self) -> bytes: ...
    def sign(
        self, keypairs: Sequence[Union[Presigner, Keypair]], recent_blockhash: Hash
    ) -> None: ...
    def partial_sign(
        self,
        keypairs: Sequence[Union[Presigner, Keypair]],
        recent_blockhash: Hash,
    ) -> None: ...
    def verify(self) -> None: ...
    def verify_and_hash_message(self) -> Hash: ...
    def verify_with_results(self) -> List[bool]: ...
    def get_signing_keypair_positions(
        self,
        pubkeys: Sequence[Pubkey],
    ) -> List[Optional[int]]: ...
    def replace_signatures(self, signers: Sequence[Tuple[Pubkey, Signature]]) -> None:
        """_summary_

        Args:
            signers (Sequence[Tuple[Pubkey, Signature]]): _description_
        """
    def is_signed(self) -> bool: ...
    def uses_durable_nonce(self) -> Optional[CompiledInstruction]: ...
    def sanitize(self) -> None: ...
    def __bytes__(self) -> bytes: ...
    @staticmethod
    def default() -> "Transaction": ...
    @staticmethod
    def from_bytes(data: bytes) -> "Transaction": ...
    def __richcmp__(self, other: "Transaction", op: int) -> bool: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def get_nonce_pubkey_from_instruction(
        self, ix: CompiledInstruction
    ) -> Optional[Pubkey]: ...

class SanitizeError(Exception): ...
class TransactionError(Exception): ...
