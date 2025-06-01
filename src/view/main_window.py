import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPlainTextEdit,
    QGridLayout,
    QFileDialog,
    QMenuBar,
    QToolBar,
)
from PySide6.QtGui import QAction

from src.view.editor import Editor
from src.view.register import Register
from .file_loader import FileLoader
from loguru import logger


class MainWindow(QMainWindow):
    WINDOW_TITLE = "RISC-V-Emulator"
    MENU_FILE = "File"
    MENU_OPEN_FILE = "Open File"
    RUN_PROGRAMM = "Run programm"
    NEXT_INSTRUCTION = "Next instruction"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.WINDOW_TITLE)
        self.file_loader = FileLoader(self)

        self._init_ui()

    def _init_ui(self):
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
        self.register = Register(size=32)
        main_layout = QGridLayout()
        main_layout.addWidget(self.editor, 0, 0)
        main_layout.addWidget(self.register, 0, 1)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        # self.run_programm.triggered.connect(self._run)

    def move(self):
        self.global_index += 1
        self.editor.move_cursor(self.global_index)

        instruction = self.editor.get_block()
        line_number = self.editor.get_line_numnber()
        logger.info(f"{line_number}-->{instruction}")

        self.run_instruction(instruction)
        self.global_index = line_number

    def _run(self):
        logger.info("Run Programm")
        # instructions = self.editor.toPlainText().split("\n")

        # self.global_index = -1
        # self.editor.set_read_mode(True)
        # self.move()

    def open_file(self):
        for line in self.file_loader.import_from_dialog():
            self.editor.append_html(line)

    def open_from_filename(self, filename: str):
        for line in self.file_loader.read_file(filename):
            self.editor.append_html(line)

    def get_programm(self):
        return self.editor.get_text()
