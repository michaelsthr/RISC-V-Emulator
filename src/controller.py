import time
import sys
from typing import Dict
from colorama import Fore
from loguru import logger
from threading import Thread
from traceback import format_exc  # Added for error logging
from PySide6.QtCore import QObject, Signal  # Added

from .model.cpu import CPU
from .view.main_window import Window


class Controller(QObject):
    update_ui_signal = Signal(object)
    execution_finished_signal = Signal()
    log_message_to_terminal_signal = Signal(str)

    def __init__(self):
        super().__init__()

        self.log_message_to_terminal_signal.connect(self._write_log_to_terminal)

        self._init_model()
        self._init_view()
        self._connect_view()
        self.__init_logger()

        # Connect other signals
        self.update_ui_signal.connect(self.update_ui)
        self.execution_finished_signal.connect(self._handle_execution_finished)
        self._execution_thread = None

    def _write_log_to_terminal(self, message: str):
        if (
            self.window
            and hasattr(self.window, "terminal")
            and hasattr(self.window.terminal, "append_text")
        ):
            self.window.terminal.append_text(message)
        else:
            print(f"UI_LOG_FALLBACK: {message}", file=sys.stderr)

    def __init_logger(self):
        logger.remove()  # Remove default logger configuration
        logger.add(sys.stdout, format="{message}", level="INFO")
        # Send log messages to the UI via Qt signal
        logger.add(
            lambda message: self.log_message_to_terminal_signal.emit(message),
            format="{message}",
            level="INFO",
        )

    def _init_model(self):
        self.cpu = CPU()

    def _init_view(self):
        self.window = Window()
        self.window._init_ui(register_set=self.cpu._register_set, ram=self.cpu.ram)
        self.window.show()

    def _connect_view(self):
        self.window.run_programm.triggered.connect(self.load_programm)
        self.window.editor.exec_step_button.pressed.connect(self.exec_step)
        self.window.editor.exec_all_button.pressed.connect(self.exec_all)

    def load_programm(self):
        if self._execution_thread and self._execution_thread.is_alive():
            logger.info(
                f"{Fore.YELLOW}Cannot load program while execution is in progress.{Fore.RESET}"
            )
            return

        self.cpu.reset()
        self.window.reset()
        self.window.editor.set_header_buttons_visible(True)

        # I know, the nested types are horrendous ...
        # I'm sorry for this :(
        # Either way: load programm to cpu
        # Maps: original_line number and the value
        programm: Dict[int, str] = self.window.get_programm()
        if all(line.strip() == "" for line in programm.values()):
            logger.info(
                f"{Fore.CYAN}Empty program. Nothing to execute.{Fore.RESET}\\n"
                f"  -> You can load a file, load an example or code your own program :)"
            )
            self.window.editor.set_header_buttons_visible(False)
            self.window.editor.exec_step_button.setEnabled(True)
            self.window.editor.exec_all_button.setEnabled(True)
            return
        self.cpu.load_programm(programm)

        origin_line_number = self.cpu.get_current_origin_line_number()

        if self.end_reached(origin_line_number):
            self.finish_process()
            self.window.editor.exec_step_button.setEnabled(True)
            self.window.editor.exec_all_button.setEnabled(True)
            return

        self.update_ui(origin_line_number)
        self.window.editor.exec_step_button.setEnabled(True)
        self.window.editor.exec_all_button.setEnabled(True)

    def exec_step(self):
        if self._execution_thread and self._execution_thread.is_alive():
            logger.info(
                f"{Fore.YELLOW}Cannot step while full execution is in progress.{Fore.RESET}"
            )
            return

        self.cpu.run_next_instruction()
        origin_line_number = self.cpu.get_current_origin_line_number()

        if self.end_reached(origin_line_number):
            self.finish_process()
            return

        self.update_ui(origin_line_number)

    def exec_all(self):
        if self._execution_thread and self._execution_thread.is_alive():
            logger.info(f"{Fore.YELLOW}Execution is already in progress.{Fore.RESET}")
            return

        self.window.editor.exec_step_button.setEnabled(False)
        self.window.editor.exec_all_button.setEnabled(False)
        self.window.run_programm.setEnabled(False)

        self._execution_thread = Thread(
            target=self._run_all_instructions_thread, daemon=True
        )
        self._execution_thread.start()

    def _run_all_instructions_thread(self):
        try:
            origin_line_number = self.cpu.get_current_origin_line_number()

            if self.end_reached(origin_line_number):
                self.update_ui_signal.emit(origin_line_number)
                return

            while not self.end_reached(origin_line_number):
                self.cpu.run_next_instruction()
                origin_line_number = self.cpu.get_current_origin_line_number()

                self.update_ui_signal.emit(origin_line_number)

                if self.end_reached(origin_line_number):
                    break

                time.sleep(0.1)

        except Exception as e:
            logger.error(
                f"{Fore.RED}Error during threaded execution: {e}\\\\n{format_exc()}{Fore.RESET}"
            )
        finally:
            self.execution_finished_signal.emit()

    def _handle_execution_finished(self):  #
        self.finish_process()
        self.window.editor.exec_step_button.setEnabled(True)
        self.window.editor.exec_all_button.setEnabled(True)
        self.window.run_programm.setEnabled(True)
        self._execution_thread = None

    def end_reached(self, line):
        if line == "END":
            return True
        return False

    def finish_process(self):
        logger.info(
            f"\\n{Fore.GREEN}END OF FILE REACHED | FINISHING DEBUGGING{Fore.RESET}"
        )
        logger.info(f"\n{Fore.CYAN}PERFORMANCE REVIEW{Fore.RESET}")
        logger.info(f"  -> CLOCK CYCLES = {self.cpu.get_clock()}")
        logger.info(f"  -> AVG CPI = {self.cpu.get_avg_cpi()}")
        logger.info(f"  -> RUNNING TIME = {self.cpu.running_time}")
        logger.info(f"  -> PERFORMANCE = {self.cpu.performance}")
        self.window.finish_debug_cursor()
        self.window.update_registers(registers=self.cpu.register_set, ram=self.cpu.ram)
        self.window.editor.set_header_buttons_visible(False)

    def update_ui(self, line_number):
        if line_number != "END":
            self.window.move_debug_cursor(line_number=line_number)
        self.window.update_registers(registers=self.cpu.register_set, ram=self.cpu.ram)
