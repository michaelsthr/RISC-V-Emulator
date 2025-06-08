from traceback import format_exc
from typing import Dict, List, Tuple
from loguru import logger
from colorama import Fore
import re


from .word import Word
from .register import Registers
from .assembler import Assembler
from .instruction_exec import InstructionExec


class CPU:
    def __init__(self, registers_size=32):
        self.assembler = Assembler()
        self._registers = Registers(size=registers_size)

        # I know, the programm counter is normally in the Register
        # Fortunately i`m creating only a simulator :)
        # And i also know, the programm counter increments by four,
        # because the instructions are four bytes long
        # We increment by one ;)
        self.pc: int = 0

        self.instructions: Dict[int, Tuple[List[str], int]] = {}
        self.instruction_exec = InstructionExec(self)

    def reset(self):
        self.assembler = Assembler()
        self.pc = 0
        self.instructions = {}

        registers_size = len(self._registers)
        self._registers = Registers(size=registers_size)

    def load_programm(
        self, programm: Dict[int, str]
    ) -> List[Tuple[int, Tuple[List[str], int]]]:
        symbol_table, self.instructions = self.assembler.parse_programm(programm)
        self.pc = 0

        logger.info(f"{Fore.CYAN}SYMBOL TABLE{Fore.RESET}")
        for item in symbol_table.items():
            logger.info(f"  {item}")

        logger.info("\n")
        logger.info(f"{Fore.CYAN}INSTRUCTIONS{Fore.RESET}")
        for item in self.instructions.items():
            logger.info(f"  {item}")

        parsed_programm = [
            (key, (value[0].split(), value[1])) for key, value in symbol_table.items()
        ]
        parsed_programm.extend(
            [(key, value) for key, value in self.instructions.items()]
        )
        parsed_programm.sort(key=lambda item: item[0])

        logger.info("\n")
        logger.info(f"{Fore.CYAN}PROGRAMM LOADED | PARSED PROGRAMM{Fore.RESET}")
        for line in parsed_programm:
            logger.info(f"  {line}")
        return parsed_programm

    def get_programm_len(self):
        return len(self.instructions)

    def run_next_instruction(self):
        instruction = {value[1]: value[0] for _, value in self.instructions.items()}
        function: str = instruction[self.pc][0]
        args: List[str] = instruction[self.pc][1:]

        try:
            logger.info(f"\n{Fore.MAGENTA}> RUN INSTRUCTION{Fore.RESET}")
            logger.info(f"  >> OLD PC={self.get_pc()}")
            logger.info(f"  >> {function}{args}")

            # run specific function
            method = getattr(self.instruction_exec, f"_{function}")
            method(*args)

            logger.info(f"  >> NEW PC={self.get_pc()}")
        except AttributeError as e:
            logger.error(f"Instruction is not defined: {e}, {format_exc()}")
        except TypeError as e:
            logger.error(f"Invalid arguments for instruction: {e}, {format_exc()}")
        except Exception as ex:
            logger.error(f"{ex}, {format_exc()}")

    def get_register_index(self, r: str):
        try:
            return int(r.removeprefix("x"))
        except ValueError:
            raise ValueError(
                f"You can't run instruction with following values: {r}. This is the preferred scheme: 'x1'"
            )

    def get_registers(self) -> Registers:
        return self._registers

    def get_pc(self) -> int:
        return self.pc

    def get_current_origin_line_number(self):
        # reversed() is important!
        # Label and instruction have the same adr! We need the instruction!
        for origin_line_number, (_, pc) in reversed(list(self.instructions.items())):
            if pc == self.pc:
                return origin_line_number
        return "END"

    def increment_pc(self, amount: int = 4):
        self.pc += amount

    def set_pc(self, value: int):
        self.pc = value

    def get_imm(self, imm: str):
        try:
            return int(imm)
        except ValueError:
            raise ValueError(f"You can't get imm with following value: {imm}")
        
    def get_base_offset(self, base_offset: str) -> Tuple[int, int]:
        match = re.match(r"(-?\d+)\(([xX]\d+)\)", base_offset)
        if not match:
            return None
        offset = int(match.group(1))
        base = int(match.group(2).removeprefix("x"))
        return base, offset

    @property
    def registers(self) -> list[Word]:
        return self._registers
