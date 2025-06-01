import pprint
from typing import Dict, List, Tuple
import re

LABEL_REGEX: str = re.compile(
    r"^[a-zA-Z_][a-zA-Z0-9_]*:$"  # (sum:, end:, ...)
)

INSTRUCTION_REGEX: str = re.compile(
    r"^\s*"  # Begin, optional space
    r"([a-z]+)"  # Opcode (addi, beq, ...)
    r"\s+"  # Space
    r"([x]\d+|\w+)"  # 1. operand
    r"(?:\s*,\s*([x]\d+|\w+))?"  # 2. operand (optional)
    r"(?:\s*,\s*([x]\d+|\w+))?"  # 3. operand (optional)
    r"\s*(?:#.*)?$"  # comment (optional)
)


class Assembler:
    def __init__(self):
        # {label, adress}
        self.symbol_table: Dict[str, int] = {}

        # {instruction string, adress}
        # Only one adress for each instruction
        self.instructions: Dict[int, List[str]] = {}

    def parse_symbol_table(self, programm: List[str]) -> Dict[str, int]:
        adr = 0
        for _, line in enumerate(programm):
            line = line.strip()
            if re.match(LABEL_REGEX, line):
                line = line.removesuffix(":")
                if line in self.symbol_table:
                    raise ValueError(
                        f"The labels {line} already exists in the symbol_table '{line}:{self.symbol_table.get(line)}'"
                    )
                self.symbol_table[line] = adr
                continue
            adr += 1
        return self.symbol_table

    def parse_instructions(self, programm: List[str]) -> Dict[List[str], int]:
        adr = 0
        for idx, line in enumerate(programm):
            line = line.strip()
            if re.match(LABEL_REGEX, line):
                continue

            match = re.match(INSTRUCTION_REGEX, line)
            if not match:
                raise ValueError(
                    f"Parsing of programm failed in line {idx}: {line}"
                    f"It should match {LABEL_REGEX} or {INSTRUCTION_REGEX}"
                )

            instruction: List[str] = [
                self.symbol_table.get(group, group) for group in match.groups()
            ]
            self.instructions[adr] = instruction
            adr += 1
        return self.instructions

    def parse_programm(
        self, programm: List[str]
    ) -> Tuple[Dict[str, int], Dict[int, List[str]]]:
        """Returns symbol_table: Dict[str, int] and instructions: Dict[int, List[str]]"""
        return self.parse_symbol_table(programm), self.parse_instructions(programm)
