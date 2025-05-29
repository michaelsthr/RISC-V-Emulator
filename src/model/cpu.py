from loguru import logger
import re

from .word import Word
from .register import Registers


class CPU:
    def __init__(self, registers_size=32):
        self.registers = Registers(size=registers_size)

    def run_instruction(self, instruction: str):
        parts = re.findall(r"[a-zA-Z0-9_]+", instruction)
        function: str = parts[0]
        args: list[str] = parts[1:]

        try:
            # run specific function
            getattr(self, f"_{function}")(*args)
        except AttributeError:
            logger.error("Instruction is not defined")
        except TypeError as e:
            logger.error(f"Invalid arguments for instruction: {e}")
        except Exception as ex:
            logger.error(ex)

    def get_register_index(self, r: str):
        try:
            return int(r.removeprefix("x"))
        except ValueError:
            raise ValueError(
                f"You can't run instruction with following values: {r}. This is the preferred scheme: 'x1'"
            )

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

        logger.info(
            f"Set register x{rd} to: {self.registers[rd].dez} = {self.registers[rs1].dez} + {self.registers[rs2].dez}"
        )

    def _sub(self, rd: str, rs1: str, rs2: str):
        logger.info(f"Run sub with rd={rd}, rs1={rs1}, rs2={rs2}")
        rd = self.get_register_index(rd)
        rs1 = self.get_register_index(rs1)
        rs2 = self.get_register_index(rs2)

        self.registers[rd] = self.registers[rs1] - self.registers[rs2]

        logger.info(
            f"Set register x{rd} to: {self.registers[rd].dez} = {self.registers[rs1].dez} + {self.registers[rs2].dez}"
        )

    def _and(self, rd: str, rs1: str, rs2: str):
        logger.info(f"Run and with rd={rd}, rs1={rs1}, rs2={rs2}")
        rd = self.get_register_index(rd)
        rs1 = self.get_register_index(rs1)
        rs2 = self.get_register_index(rs2)

        self.registers[rd] = self.registers[rs1] & self.registers[rs2]

        logger.info(
            f"Set register x{rd} to: {self.registers[rd].dez} = {self.registers[rs1].dez} + {self.registers[rs2].dez}"
        )

    def _or(self, rd: str, rs1: str, rs2: str):
        logger.info(f"Run or with rd={rd}, rs1={rs1}, rs2={rs2}")
        rd = self.get_register_index(rd)
        rs1 = self.get_register_index(rs1)
        rs2 = self.get_register_index(rs2)

        self.registers[rd] = self.registers[rs1] | self.registers[rs2]

        logger.info(
            f"Set register x{rd} to: {self.registers[rd].dez} = {self.registers[rs1].dez} + {self.registers[rs2].dez}"
        )

    def _xor(self):
        logger.info("Run xor")

    def _li(self, rd: str, imm: str):
        logger.info(f"Run li with rd={rd}, imm={imm}")
        rd = self.get_register_index(rd)
        imm = self.get_imm(imm)
        self.registers[rd] = Word(imm)

        logger.info(f"Set register x{rd} to: x{rd} = {imm}")


if __name__ == "__main__":
    cpu = CPU()
    instruction: str = "add x3, x1, x2"
    cpu.run_instruction(instruction)
    # print(cpu.registers)
    # print(cpu.registers[0].dez)
