from pprint import pprint
import sys
from typing import Dict, List
from PySide6.QtWidgets import QApplication
import qdarktheme
from colorama import Fore
from loguru import logger

from .model.cpu import CPU
from .view.main_window import Window


class Controller:
    def __init__(self):
        self._init_model()
        self._init_view()
        self._connect_view()
        self.__init_logger()

    def __init_logger(self):
        logger.remove()  # Remove default logger configuration
        logger.add(sys.stdout, format="{message}", level="INFO")
        logger.add(self.window.terminal.append_text, format="{message}", level="INFO")

    def _init_model(self):
        self.cpu = CPU()

    def _init_view(self):
        self.window = Window()
        self.window._init_ui(register_set=self.cpu._register_set, ram=self.cpu.ram)
        self.window.show()

    def _connect_view(self):
        self.window.run_programm.triggered.connect(self.start_programm)
        self.window.next_instruction.triggered.connect(self.run_next_instruction)

    def start_programm(self):
        logger.info("Run Programm")
        self.cpu.reset()
        self.window.reset()
        # I know, the nested types are horrendous ...
        # I'm sorry for this :(

        # load programm to cpu
        # Maps: original_line number and the value
        programm: Dict[int, str] = self.window.get_programm()

        self.cpu.load_programm(programm)

        self.update_ui()

    def run_next_instruction(self):
        self.cpu.run_next_instruction()
        self.update_ui()

    def update_ui(self):
        pc = self.cpu.get_pc()
        origin_line_number = self.cpu.get_current_origin_line_number()
        if origin_line_number == "END":
            logger.info(
                f"\n{Fore.GREEN}END OF FILE REACHED | FINISHING DEBUGGING{Fore.RESET}"
            )
            self.window.finish_debug_cursor()
        else:
            self.window.move_debug_cursor(line_number=origin_line_number)

        self.window.update_registers(registers=self.cpu.register_set, ram=self.cpu.ram)
