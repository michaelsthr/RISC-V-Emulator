from typing import Dict
from loguru import logger
from colorama import Fore

from .word import Word

class RAM:
    def __init__(self, max_size: int):
        self._register_set: Dict[int, Word] = {}
        self.max_size = max_size

    def __repr__(self):
        return f"Registers(registers={self._register_set}, size={self.size}"

    def __str__(self):
        return "\n".join(
            [f"x{idx}  {register}" for idx, register in self._register_set.items()]
        )

    def __getitem__(self, key: int) -> Word:
        if key < 0:
            logger.info(f"{Fore.LIGHTRED_EX}Index {key} is smaller than 0")
            raise
        
        if key >= self.size:
            logger.info(f"{Fore.LIGHTRED_EX}Index {key} is greater than {self.size}")
            raise

        return self._register_set[key]

    def __setitem__(self, key: int, value: Word):
        self._register_set[key] = value

    def __len__(self):
        return len(self._register_set)
    
    def get_max_size(self) -> int:
        return self.max_size

    @property
    def registers(self) -> Dict[int, Word]:
        return self._register_set