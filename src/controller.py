from pprint import pprint
import sys
from typing import List
from PySide6.QtWidgets import QApplication
import qdarktheme
from loguru import logger

from .model.cpu import CPU
from .view.main_window import MainWindow


class Controller:
    def __init__(self):
        self._init_model()
        self._init_view()
        self._connect_view()

    def _init_view(self):
        self.window = MainWindow()
        self.window.show()

    def _init_model(self):
        self.cpu = CPU()

    def _connect_view(self):
        self.window.run_programm.triggered.connect(self.start_programm)
        self.window.next_instruction.triggered.connect(self.run_next_instruction)

    def start_programm(self):
        logger.info("Run Programm")

        # load programm to cpu
        programm = self.window.get_programm()
        parsed_programm = self.cpu.load_programm(programm)
        pprint(parsed_programm)

        pc = self.cpu.get_pc()
        registers = self.cpu.get_registers()

        print(parsed_programm)
        lines = [" ".join((i if isinstance(i, str) else str(i)) for i in value) for key, value in parsed_programm]
        self.window.editor.update_editor(lines)
        offset = 0
        block: str = self.window.editor.get_block()
        print("block", block)
        while block.endswith("e q u a l l"):
            offset += 1
            print("offsetted")
        self.window.editor.move_cursor(pc + offset)
        

    def run_next_instruction(self):
        self.cpu.run_next_instruction()
        pc = self.cpu.get_pc()
        registers = self.cpu.get_registers()
        self.window.editor.move_cursor(pc)

        offset = 0
        block: str = self.window.editor.get_block()
        print("block", block)
        while block.endswith("<label>"):
            offset += 1
            self.window.editor.move_cursor(pc + offset)
            block: str = self.window.editor.get_block()
            print("offsetted")
         # self.window.editor.move_cursor(pc + offset)
