from loguru import logger
from src.model.bits import Bits

class Registers:
    def __init__(self, size: int):
        self.size = size
        self.registers: list[Bits] = [Bits(self.size)] * self.size
        self.register_präfix = "x"

    def print_registers(self):
        for idx, register in enumerate(self.registers):
            print(f"x{idx} \t{register}")

    def get_register(self, idx: int) -> Bits:
        try:
            return self.registers[idx]
        except Exception as ex:
            logger.error(f"Failed to get register: {idx}. Exception: {ex}")

    def set_register(self, idx: int, bits: Bits):
        try:
            self.registers[idx] = bits
            logger.info(f"Register[{idx}] set to {bits}")
        except Exception as ex:
            logger.error(
                f"Failed to set register: {idx} with value: {bits}. Exception: {ex}"
            )

    def get_registers(self) -> list:
        return self.registers


if __name__ == "__main__":
    register = Registers(size=32)
    bits = Bits(32)
    register.set_register(2, bits)
    register.print_registers()
    print("\n\n")
    bits.set_at_index(4, "1")
    register.print_registers()
