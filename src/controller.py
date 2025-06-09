import sys
from typing import Dict
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
        self.cpu.reset()
        self.window.reset()

        # I know, the nested types are horrendous ...
        # I'm sorry for this :(
        # Either way: load programm to cpu
        # Maps: original_line number and the value
        programm: Dict[int, str] = self.window.get_programm()
        self.cpu.load_programm(programm)

        origin_line_number = self.cpu.get_current_origin_line_number()

        if self.end_reached(origin_line_number):
            self.finish_process()
            return

        self.update_ui(origin_line_number)

    def run_next_instruction(self): 
        self.cpu.run_next_instruction()
        origin_line_number = self.cpu.get_current_origin_line_number()

        if self.end_reached(origin_line_number):
            self.finish_process()
            return

        self.update_ui(origin_line_number)

    def end_reached(self, line):
        if line == "END":
            return True
        return False
    
    def finish_process(self):
        logger.info(f"\n{Fore.GREEN}END OF FILE REACHED | FINISHING DEBUGGING{Fore.RESET}")
        logger.info(f"\n{Fore.CYAN}PERFORMANCE REVIEW{Fore.RESET}")
        logger.info(f"  -> CLOCK CYCLES = {self.cpu.get_clock()}")
        logger.info(f"  -> AVG CPI = {self.cpu.get_avg_cpi()}")
        logger.info(f"  -> RUNNING TIME = {self.cpu.running_time}")
        logger.info(f"  -> PERFORMANCE = {self.cpu.performance}")
        self.window.finish_debug_cursor()
        self.window.update_registers(registers=self.cpu.register_set, ram=self.cpu.ram)

    def update_ui(self, line_number):
        self.window.move_debug_cursor(line_number=line_number)
        self.window.update_registers(registers=self.cpu.register_set, ram=self.cpu.ram)
