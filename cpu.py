from loguru import logger
import re

class CPU():
    def __init__(self):
        pass

    def run_instruction(self, instruction: str):
        parts = re.findall(r"[a-zA-Z0-9_]+", instruction)
        function = parts[0]
        args = parts[1:]

        try:
            getattr(self, f"_{function}")(*args)
        except AttributeError:
            logger.warning("Instruction is not defined")
        except TypeError as e:
            logger.warning(f"Invalid arguments for instruction: {e}")

    def _mov(self, x1, x2, x3):
        logger.info(f"Run mov with args: {x1}, {x2}, {x3}")

    def _add(self):
        logger.info("Run add")

    def _sub(self):
        logger.info("Run sub")

    def _and(self):
        logger.info("Run and")

    def _or(self):
        logger.info("Run or")

    def _xor(self):
        logger.info("Run xor")