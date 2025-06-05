from loguru import logger
from .word import Word


class Registers:
    def __init__(self, size: int):
        self.size = size
        self._registers: list[Word] = [Word(dez=0)] * self.size
        self.register_präfix = "x"

    def __repr__(self):
        return f"Registers(registers={self._registers}, size={self.size}, register_präfix={self.register_präfix})"

    def __str__(self):
        return "\n".join([f"x{idx} \t{register}" for idx, register in enumerate(self._registers)])

    def __getitem__(self, key: int) -> Word:
        if key >= self.size or key < 0:
            logger.error(f"Index {key} out of bounds for registers of size {self.size}")
            return
        return self._registers[key]

    def __setitem__(self, key: int, value: Word):
        self._registers[key] = value

    def __len__(self):
        return len(self._registers)

    @property
    def registers(self) -> list[Word]:
        return self._registers
