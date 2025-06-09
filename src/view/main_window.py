from typing import Dict
from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QMenuBar, QToolBar
from PySide6.QtGui import QAction

from paths import EXAMPLE_FILES_DIR

from src.config import EXAMPLE_FILES
from src.model.ram import RAM
from src.model.register_set import RegisterSet

from .editor_view import Editor
from .ram_view import RAMView
from .register_set_view import RegisterSetView
from .file_loader_view import FileLoader
from .terminal_view import Terminal
from .label import Label


class Window(QMainWindow):
    WINDOW_TITLE = "RISC-V-Emulator"
    MENU_FILE = "File"
    MENU_OPEN_FILE = "Open File"
    MENU_EXAMPLES = "Examples"
    RUN_PROGRAMM = "Run and Debug"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.file_loader = FileLoader(self)

    def _init_ui(self, register_set: RegisterSet, ram: RAM):
        ### Menu Bar ###
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu(self.MENU_FILE)

        self.load_action = QAction(self.MENU_OPEN_FILE, self)
        file_menu.addAction(self.load_action)
        self.load_action.triggered.connect(self.open_file)

        examples_menu = menu_bar.addMenu(self.MENU_EXAMPLES)
        for example_file in EXAMPLE_FILES:
            action = QAction(example_file, self)
            action.triggered.connect(
                lambda checked=False, filename=example_file: self._load_example_file(
                    filename
                )
            )
            examples_menu.addAction(action)

        ### Tool Bar ###
        tool_bar = QToolBar(self)

        self.run_programm = QAction(self.RUN_PROGRAMM, self)
        tool_bar.addAction(self.run_programm)

        tool_bar.addSeparator()

        self.addToolBar(tool_bar)
        self.setMenuBar(menu_bar)

        ### Main Layout
        self.editor = Editor()
        self.register_set_view = RegisterSetView(register_set=register_set)
        self.ram_view = RAMView(ram=ram)
        self.terminal = Terminal()

        main_layout = QGridLayout()
        main_layout.addWidget(self.editor, 0, 0)
        main_layout.addWidget(self.terminal, 1, 0)
        main_layout.addWidget(self.register_set_view, 0, 1)
        main_layout.addWidget(self.ram_view, 1, 1)

        main_layout.setColumnStretch(0, 10)
        main_layout.setColumnStretch(1, 8)
        main_layout.setRowStretch(0, 2)
        main_layout.setRowStretch(1, 1)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def open_file(self):
        lines = self.file_loader.import_from_dialog()
        if lines:
            self.editor.reset()
            for line in lines:
                self.editor.append_html(line)

    def open_from_filename(self, filename: str):
        self.editor.reset()  # Reset editor before loading new file
        for line in self.file_loader.read_file(filename):
            self.editor.append_html(line)

    def _load_example_file(self, filename: str):
        full_path = EXAMPLE_FILES_DIR / filename
        self.open_from_filename(full_path)

    def get_programm(self) -> Dict[int, str]:
        return {idx: line for idx, line in enumerate(self.editor.get_text())}

    def move_debug_cursor(self, line_number):
        self.editor.move_cursor(line_number)

    def update_registers(self, registers: RegisterSet, ram: RAM):
        self.register_set_view.update_registers(registers=registers)
        self.ram_view.update_registers(ram=ram)

    def finish_debug_cursor(self):
        self.editor.finish_debug_cursor()

    def reset(self):
        self.terminal.clear()
        self.editor.finish_debug_cursor()
