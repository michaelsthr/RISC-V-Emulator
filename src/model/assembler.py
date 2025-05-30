from typing import Dict, List, Tuple
import re

from helper import LABEL_REGEX
from helper import INSTRUCTION_REGEX


class Assembler:
    def __init__(self):
        # {label, adress}
        self.symbol_table: Dict[str, int] = {}

        # {instruction string, adress}
        self.instructions: Dict[str, int] = {}

    def parse_programm(
        self, programm: List[str]
    ) -> Tuple[Dict[str, int], Dict[str, int]]:
        for idx, line in enumerate(programm):
            if re.match(LABEL_REGEX, line):
                if line.strip() in self.labels:
                    raise ValueError(f"The labels already exists: {programm}")
                self.labels |= {line.strip(), idx}
                continue

            elif re.match(INSTRUCTION_REGEX, line):
                self.instructions |= {line.split("x")[0].strip(), idx}
                continue

            else:
                raise ValueError(
                    f"Parsing of programm failed in line {idx}: {line}"
                    f"It should match {LABEL_REGEX} or {INSTRUCTION_REGEX}"
                )

        return self.symbol_table, self.instructions
