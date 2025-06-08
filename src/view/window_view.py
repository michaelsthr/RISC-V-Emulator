from typing import Dict
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QMenuBar,
    QToolBar,
    QFontComboBox,
    QHBoxLayout,
)
from PySide6.QtGui import QAction

from src.model.register import Registers
from .editor_view import Editor
from .register_view import RegisterView
from .file_loader_view import FileLoader
from .terminal_view import Terminal


class Window(QMainWindow):
    WINDOW_TITLE = "RISC-V-Emulator"
    MENU_FILE = "File"
    MENU_OPEN_FILE = "Open File"
    RUN_PROGRAMM = "Run programm"
    NEXT_INSTRUCTION = "Run instruction"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.file_loader = FileLoader(self)

    def _init_ui(self, registers: Registers):
        ### Menu Bar ###
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu(self.MENU_FILE)

        self.load_action = QAction(self.MENU_OPEN_FILE, self)
        file_menu.addAction(self.load_action)
        self.load_action.triggered.connect(self.open_file)

        ### Tool Bar ###
        tool_bar = QToolBar(self)

        self.run_programm = QAction(self.RUN_PROGRAMM, self)
        tool_bar.addAction(self.run_programm)

        tool_bar.addSeparator()

        self.next_instruction = QAction(self.NEXT_INSTRUCTION, self)
        tool_bar.addAction(self.next_instruction)

        self.addToolBar(tool_bar)
        self.setMenuBar(menu_bar)

        ### Main Layout
        self.editor = Editor()
        self.register = RegisterView(registers=registers)
        self.terminal = Terminal()
        main_layout = QGridLayout()
        main_layout.addWidget(self.editor, 0, 0, 2, 1)
        main_layout.addWidget(self.register, 0, 1)
        main_layout.addWidget(self.terminal, 1, 1)
        main_layout.setColumnStretch(0, 10)
        main_layout.setColumnStretch(1, 8)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def open_file(self):
        for line in self.file_loader.import_from_dialog():
            self.editor.append_html(line)

    def open_from_filename(self, filename: str):
        for line in self.file_loader.read_file(filename):
            self.editor.append_html(line)

    def get_programm(self) -> Dict[int, str]:
        return {idx: line for idx, line in enumerate(self.editor.get_text())}

    def move_debug_cursor(self, line_number):
        self.editor.move_cursor(line_number)

    def update_registers(self, registers: Registers):
        self.register.update_registers(registers=registers)

    def finish_debug_cursor(self):
        self.editor.finish_debug_cursor()

    def reset(self):
        self.terminal.clear()
        self.editor.finish_debug_cursor()
