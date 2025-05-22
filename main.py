import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QPlainTextEdit,
    QGridLayout,
    QFileDialog,
)
import qdarktheme
from pathlib import Path

from src.view.editor import Editor
from src.view.register import Register
from loguru import logger

from src.view.file_loader import FileLoader
from src.model.cpu import CPU


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RISC-V-Emulator")
        # self.loader = Loader(self)
        self.file_loader = FileLoader(self)
        self.cpu = CPU()
        self.input_arry = []
        self._init_ui()
        self._connect_ui_signals()

    def _init_ui(self):
        main_layout = QGridLayout()

        button_menu = QHBoxLayout()
        self.run_button = QPushButton("Start")
        self.next_button = QPushButton("Next")
        self.load_button = QPushButton("Load File")

        self.editor = Editor()
        self.register = Register(size=32)

        button_menu.addWidget(self.run_button)
        button_menu.addWidget(self.next_button)
        button_menu.addWidget(self.load_button)

        main_layout.addLayout(button_menu, 0, 0)
        main_layout.addWidget(self.editor, 1, 0)
        main_layout.addWidget(self.register, 1, 1)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def _connect_ui_signals(self):
        self.load_button.clicked.connect(self.import_files)
        self.run_button.clicked.connect(self.run)
        self.next_button.clicked.connect(self.move)

    def move(self):
        self.global_index += 1
        self.editor.move_cursor(self.global_index)

        instruction = self.editor.get_block()
        line_number = self.editor.get_line_numnber()
        logger.info(f"{line_number}-->{instruction}")

        self.run_instruction(instruction)
        self.global_index = line_number

    def run(self):
        # instructions = self.editor.toPlainText().split("\n")
        self.global_index = -1
        self.editor.set_read_mode(True)
        self.move()

    def run_instruction(self, instruction: str):
        logger.info(f"Run instruction: {instruction}")
        self.cpu.run_instruction(instruction)

    def import_files(self):
        for line in self.file_loader.import_from_dialog():
            self.editor.append_html(line)

    def import_file(self, filename: str):
        for line in self.file_loader.read_file(filename):
            self.editor.append_html(line)

def __init_logger():
    logger.remove()  # Remove default logger configuration
    logger.add(sys.stdout, format="{message}", level="INFO")

if __name__ == "__main__":
    __init_logger()
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    window = MainWindow()
    window.show()

    window.import_file("example_files/instructions.txt")

    app.exec()
