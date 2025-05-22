from loguru import logger


class Registers:
    def __init__(self, size: int):
        self.size = size
        self.registers: list = ["0" * self.size] * self.size
        self.register_präfix = "x"

    def print_registers(self):
        for idx, register in enumerate(self.registers):
            print(f"x{idx} \t{register}")

    def get_register(self, idx: int) -> str:
        try:
            return register.get(idx)
        except Exception as ex:
            logger.error(f"Failed to get register: {idx}. Exception: {ex}")

    def set_register(self, idx: int, value: str):
        try:
            if len(value) != self.size:
                raise Exception(
                    f"The value length should be 32. The current value is: {value} with lenght: {len(value)}"
                )
            if idx >= self.size - 1 or idx <= 0:
                raise Exception(
                    f"The index should be between {0} and {self.size - 1}. It is: {idx}"
                )
            self.registers[idx] = value
            logger.info(f"Register[{idx}] set to {value}")
        except Exception as ex:
            logger.error(
                f"Failed to set register: {idx} with value: {value}. Exception: {ex}"
            )

    def get_registers(self) -> list:
        return self.registers


if __name__ == "__main__":
    register = Registers(size=32)
    register.set_register(2, "000000000000000")
    register.set_register(49, "0" * 32)
    register.set_register(-1, "0" * 32)
    register.set_register(4, "0" * 32)
    register.set_register(8, "01" * 16)
    register.set_register(20, "1" * 32)
    register.set_register(20, "" * 32)
    register.print_registers()
