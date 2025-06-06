from traceback import format_exc
from typing import Dict, List, Tuple
from loguru import logger

from .word import Word
from .register import Registers
from .assembler import Assembler


class CPU:
    def __init__(self, registers_size=32):
        self.assembler = Assembler()
        self.registers = Registers(size=registers_size)

        # I know, the programm counter is normally in the Register
        # Fortunately i`m creating only a simulator :)
        # And i also know, the programm counter increments by four,
        # because the instructions are four bytes long
        # We increment by one ;)
        self.pc: int = 0

        self.instructions: Dict[int, Tuple[List[str], int]] = {}

    def reset(self):
        self.assembler = Assembler()
        self.pc = 0
        self.instructions = {}

        registers_size = len(self.registers)
        self.registers = Registers(size=registers_size)

    def load_programm(
        self, programm: Dict[int, str]
    ) -> List[Tuple[int, Tuple[List[str], int]]]:
        symbol_table, self.instructions = self.assembler.parse_programm(programm)
        self.pc = 0

        parsed_programm = [
            (key, (value[0].split(), value[1])) for key, value in symbol_table.items()
        ]
        parsed_programm.extend(
            [(key, value) for key, value in self.instructions.items()]
        )
        parsed_programm.sort(key=lambda item: item[0])

        return parsed_programm

    def get_programm_len(self):
        return len(self.instructions)

    def run_next_instruction(self):
        instruction = {value[1]: value[0] for _, value in self.instructions.items()}
        function: str = instruction[self.pc][0]
        args: List[str] = instruction[self.pc][1:]

        try:
            logger.info(f"Run instruction: '{self.pc}:{instruction[self.pc]}")
            # run specific function
            getattr(self, f"_{function}")(*args)
            logger.info("\n")
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
        return self.registers

    def get_pc(self) -> int:
        return self.pc

    def get_current_origin_line_number(self):
        # reversed() is important!
        # Label and instruction have the same adr! We need the instruction!
        for origin_line_number, (_, pc) in reversed(list(self.instructions.items())):
            if pc == self.pc:
                return origin_line_number
        return "END"

    def increment_pc(self, amount: int = 1):
        self.pc += amount
        logger.info(f"Instruction count set to: {self.pc}")

    ### INSTRUCTIONS ###

    def get_imm(self, imm: str):
        try:
            return int(imm)
        except ValueError:
            raise ValueError(f"You can't get imm with following value: {imm}")

    def _add(self, rd: str, rs1: str, rs2: str):
        logger.info(f"Run add with rd={rd}, rs1={rs1}, rs2={rs2}")
        rd = self.get_register_index(rd)
        rs1 = self.get_register_index(rs1)
        rs2 = self.get_register_index(rs2)

        self.registers[rd] = self.registers[rs1] + self.registers[rs2]
        self.increment_pc()

        logger.info(
            f"Set register x{rd} to: {self.registers[rd].dez} = {self.registers[rs1].dez} + {self.registers[rs2].dez}"
        )

    def _sub(self, rd: str, rs1: str, rs2: str):
        logger.info(f"Run sub with rd={rd}, rs1={rs1}, rs2={rs2}")
        rd = self.get_register_index(rd)
        rs1 = self.get_register_index(rs1)
        rs2 = self.get_register_index(rs2)

        self.registers[rd] = self.registers[rs1] - self.registers[rs2]
        self.increment_pc()

        logger.info(
            f"Set register x{rd} to: {self.registers[rd].dez} = {self.registers[rs1].dez} + {self.registers[rs2].dez}"
        )

    def _and(self, rd: str, rs1: str, rs2: str):
        logger.info(f"Run and with rd={rd}, rs1={rs1}, rs2={rs2}")
        rd = self.get_register_index(rd)
        rs1 = self.get_register_index(rs1)
        rs2 = self.get_register_index(rs2)

        self.registers[rd] = self.registers[rs1] & self.registers[rs2]
        self.increment_pc()

        logger.info(
            f"Set register x{rd} to: {self.registers[rd].dez} = {self.registers[rs1].dez} + {self.registers[rs2].dez}"
        )

    def _or(self, rd: str, rs1: str, rs2: str):
        logger.info(f"Run or with rd={rd}, rs1={rs1}, rs2={rs2}")
        rd = self.get_register_index(rd)
        rs1 = self.get_register_index(rs1)
        rs2 = self.get_register_index(rs2)

        self.registers[rd] = self.registers[rs1] | self.registers[rs2]
        self.increment_pc()

        logger.info(
            f"Set register x{rd} to: {self.registers[rd].dez} = {self.registers[rs1].dez} + {self.registers[rs2].dez}"
        )

    def _xor(self, rd: str, rs1: str, rs2: str):
        logger.info(f"Run xor with rd={rd}, rs1={rs1}, rs2={rs2}")
        rd = self.get_register_index(rd)
        rs1 = self.get_register_index(rs1)
        rs2 = self.get_register_index(rs2)

        self.registers[rd] = self.registers[rs1] ^ self.registers[rs2]
        self.increment_pc()

        logger.info(
            f"Set register x{rd} to: {self.registers[rd].dez} = {self.registers[rs1].dez} + {self.registers[rs2].dez}"
        )

    def _addi(self, rd: str, rs1: str, imm: str):
        logger.info(f"Run addi with rd={rd}, rs1={rs1}, imm={imm}")
        rd = self.get_register_index(rd)
        rs1 = self.get_register_index(rs1)
        imm = self.get_imm(imm)

        self.registers[rd] = self.registers[rs1] + Word(imm)
        self.increment_pc()

        logger.info(f"Set register x{rd} to: x{rs1} = {imm}")

    def _andi(self, rd: str, rs1: str, imm: str):
        logger.info(f"Run andi with rd={rd}, rs1={rs1}, imm={imm}")
        rd = self.get_register_index(rd)
        rs1 = self.get_register_index(rs1)
        imm = self.get_imm(imm)

        self.registers[rd] = self.registers[rs1] & Word(imm)
        self.increment_pc()

        logger.info(f"Set register x{rd} to: x{rs1} = {imm}")

    def _ori(self, rd: str, rs1: str, imm: str):
        logger.info(f"Run ori with rd={rd}, rs1={rs1}, imm={imm}")
        rd = self.get_register_index(rd)
        rs1 = self.get_register_index(rs1)
        imm = self.get_imm(imm)

        self.registers[rd] = self.registers[rs1] | Word(imm)
        self.increment_pc()

        logger.info(f"Set register x{rd} to: x{rs1} = {imm}")

    def _li(self, rd: str, imm: str):
        logger.info(f"Run li with rd={rd}, imm={imm}")
        rd = self.get_register_index(rd)
        imm = self.get_imm(imm)
        self.registers[rd] = Word(imm)
        self.increment_pc()

        logger.info(f"Set register x{rd} to: x{rd} = {imm}")

    def _beq(self, rs1: str, rs2: str, imm: str):
        logger.info(f"Run beq with rs1={rs1}, rs2={rs2}, imm={imm}")
        rs1 = self.get_register_index(rs1)
        rs2 = self.get_register_index(rs2)
        imm = self.get_imm(imm)

        if self.registers[rs1] == self.registers[rs2]:
            self.pc = imm
        else:
            self.increment_pc()

        logger.info(f"Set pc: {self.pc} to: pc = {imm}")

    def _bne(self, rs1: str, rs2: str, imm: str):
        logger.info(f"Run beq with rs1={rs1}, rs2={rs2}, imm={imm}")
        rs1 = self.get_register_index(rs1)
        rs2 = self.get_register_index(rs2)
        imm = self.get_imm(imm)

        if self.registers[rs1] != self.registers[rs2]:
            self.pc = imm
        else:
            self.increment_pc()

        logger.info(f"Set pc: {self.pc} to: pc = {imm}")


if __name__ == "__main__":
    try:
        cpu = CPU()
        programm: List[str] = [
            "addi x1 , x0 , 7 # x1 = 7",
            "addi x2 , x0 , 7 # x2 = 7",
            "beq x1 , x2 , equal #springe nach 'equal' fallsgleich",
            "addi x3 , x0 , 1 # wird uebersprungen",
            "equal:",
            "addi x3 , x0 , 99 # x3 = 99",
        ]
        cpu.load_programm(programm)

        for i in range(cpu.get_programm_len() - 1):
            cpu.run_next_instruction()
        # print(cpu.registers)
        # print(cpu.registers[0].dez)
    except Exception as ex:
        print(ex, format_exc())
