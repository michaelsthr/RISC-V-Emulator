from pprint import pprint
import sys
from typing import Dict, List
from PySide6.QtWidgets import QApplication
import qdarktheme
from loguru import logger

from .model.cpu import CPU
from .view.window import Window


class Controller:
    def __init__(self):
        self._init_model()
        self._init_view()
        self._connect_view()

    def _init_model(self):
        self.cpu = CPU()

    def _init_view(self):
        self.window = Window()
        self.window._init_ui(registers=self.cpu.registers)
        self.window.show()


    def _connect_view(self):
        self.window.run_programm.triggered.connect(self.start_programm)
        self.window.next_instruction.triggered.connect(self.run_next_instruction)

    def start_programm(self):
        logger.info("Run Programm")
        # I know, the nested types are horrendous ...
        # I'm sorry for this :(

        # load programm to cpu
        # Maps: original_line number and the value
        programm: Dict[int, str] = self.window.get_programm()

        parsed_programm = self.cpu.load_programm(programm)
        pprint(parsed_programm)

        self.update_ui()

    def run_next_instruction(self):
        self.cpu.run_next_instruction()
        self.update_ui()

    def update_ui(self):
        pc = self.cpu.get_pc()
        origin_line_number = self.cpu.get_current_origin_line_number()
        self.window.move_debug_cursor(line_number=origin_line_number)

        registers = self.cpu.get_registers()
        self.window.update_registers(registers)
