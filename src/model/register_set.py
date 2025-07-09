from loguru import logger
from .word import Word


class RegisterSet:
    def __init__(self, size: int):
        self.size = size
        self._register_set: list[Word] = [Word(dez=0)] * self.size
        self.register_präfix = "x"

    def __repr__(self):
        return f"Registers(registers={self._register_set}, size={self.size}, register_präfix={self.register_präfix})"

    def __str__(self):
        return "\n".join(
            [f"x{idx} \t{register}" for idx, register in enumerate(self._register_set)]
        )

    def __getitem__(self, key: int) -> Word:
        if key >= self.size or key < 0:
            logger.error(f"Index {key} out of bounds for registers of size {self.size}")
            return
        return self._register_set[key]

    def __setitem__(self, key: int, value: Word):
        if key == 0:
            # x0 is hardwired to zero in RISC-V, silently ignore writes
            logger.error("Attempted write to x0 register (hardwired to zero)")
            return
        self._register_set[key] = value

    def __len__(self):
        return len(self._register_set)

    @property
    def registers(self) -> list[Word]:
        return self._register_set
