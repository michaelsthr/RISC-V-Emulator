import pprint
from typing import Dict, List, Tuple
from loguru import logger
from colorama import Fore
import re

LABEL_REGEX: str = re.compile(
    r"^[a-zA-Z_.][a-zA-Z0-9_]*:$"  # (sum:, end:, ...)
)

INSTRUCTION_REGEX: str = re.compile(
    r"^\s*"  # Begin, optional space
    r"([a-z]+)"  # Opcode (addi, beq, ...)
    r"\s+"  # Space
    r"(?:([x]\d+|\S+))?"  # 1. operand (optional)
    r"(?:\s*,\s*([x]\d+|\S+))?"  # 2. operand (optional)
    r"(?:\s*,\s*([x]\d+|\S+))?"  # 3. operand (optional)
    r"\s*(?:#.*)?$"  # comment (optional)
)


class Assembler:

    STEP_AMOUNT = 4

    def __init__(self):
        # {label, adress}

        # {OriginalLine, Label, Adress}
        self.symbol_table: Dict[int, Tuple[str, int]] = {}

        # {OriginalLine, Instruction, Adress}
        self.instructions: Dict[int, Tuple[List[str], int]] = {}

    def parse_symbol_table(self, programm: List[str]) -> Dict[int, Tuple[str, int]]:
        adr = 0
        logger.info(f"{Fore.CYAN}PARSE LABELS{Fore.RESET}")
        for idx, line in enumerate(programm):
            line = line.strip()
            if re.match(LABEL_REGEX, line):
                line = line.removesuffix(":")
                if any(line == label for (label, _) in self.symbol_table.values()):
                    raise ValueError(
                        f"The labels {line} already exists in the symbol_table '{line}:{self.symbol_table.get(line)}'"
                    )
                self.symbol_table[idx] = (line, adr)
                logger.info(f"  LABEL: {idx}:({line},{adr})")
                continue
            adr += self.STEP_AMOUNT
        logger.info("\n")
        return self.symbol_table

    def parse_instructions(self, programm: List[str]) -> Dict[List[str], int]:
        adr = 0
        logger.info(f"{Fore.CYAN}PARSE INSTRUCIONS{Fore.RESET}")
        for idx, line in enumerate(programm):
            line = line.strip()
            if re.match(LABEL_REGEX, line):
                continue
            logger.info(f"  BEFORE: {idx}-->{line}")

            match = re.match(INSTRUCTION_REGEX, line)
            if not match:
                raise ValueError(
                    f"PARSING OF PROGRAMM FAILED\n"
                    f"  >> line {idx}:{line}\n"
                    f"  >> It should match LABELREGEX {LABEL_REGEX}\n"
                    f"  >> Or should match INSTRUCTION_REGEX {INSTRUCTION_REGEX}\n" 
                )

            temp_table = {value[0]: value[1] for _, value in self.symbol_table.items()}
            logger.info(f"  {temp_table}")
            logger.info(f"  GROUPS:{match.groups()}")
            instruction: List[str] = [
                temp_table.get(group, group) for group in match.groups() if group is not None
            ]
            self.instructions[idx] = (instruction, adr)
            adr += self.STEP_AMOUNT
            logger.info(f"  AFTER: {idx}-->{self.instructions[idx]}")
            logger.info("\n")
        return self.instructions

    def parse_programm(
        self, programm:  Dict[int, str]
    ) -> Tuple[Dict[int, Tuple[str, int]], Dict[int, Tuple[List[str], int]]]:
        """Returns symbol_table: Dict[str, int] and instructions: Dict[int, List[str]]"""
        try:
            lines = [value for (_, value) in programm.items()]
            return self.parse_symbol_table(lines), self.parse_instructions(lines)
        except Exception as ex:
            logger.info(f"\n{Fore.LIGHTRED_EX}{ex}{Fore.RESET}\n")
