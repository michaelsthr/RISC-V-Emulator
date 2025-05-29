from loguru import logger
import re

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
            logger.warning("Instruction is not defined")
        except TypeError as e:
            logger.warning(f"Invalid arguments for instruction: {e}")

    def _mov(self, x1, x2, x3):
        logger.info(f"Run mov with args: {x1}, {x2}, {x3}")

    def _add(self, rd: str, rs1: str, rs2: str):
        logger.info(f"Run add with rd={rd}, rs1={rs1}, rs2={rs2}")
        rd = rd.removeprefix("x")
        rs1 = rs1.removeprefix("x")
        rs2 = rs2.removeprefix("x")

        try:
            rd = int(rd)
            rs1 = int(rs1)
            rs2 = int(rs2)
        except ValueError:
            logger.error(
                f"You can't run instructions with following values: {rd}, {rs1}, {rs2}. This is the preferred scheme: 'x1'"
            )

        self.registers[rd] = self.registers[rs1] + self.registers[rs2]

        logger.info(
            f"Set register x{rd} to: {self.registers[rd].dez} = {self.registers[rs1].dez} + {self.registers[rs2].dez}"
        )

    def _sub(self):
        logger.info("Run sub")

    def _and(self):
        logger.info("Run and")

    def _or(self):
        logger.info("Run or")

    def _xor(self):
        logger.info("Run xor")


if __name__ == "__main__":
    cpu = CPU()
    instruction: str = "add x3, x1, x2"
    cpu.run_instruction(instruction)
    # print(cpu.registers)
    # print(cpu.registers[0].dez)
