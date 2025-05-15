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

from layout.editor import Editor


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RISC-V-Emulator")
        # self.loader = Loader(self)
        self.input_arry = []
        self._init_ui()
        self._connect_ui_signals()

    def _init_ui(self):
        main_layout = QGridLayout()

        button_menu = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.next_button = QPushButton("Next")
        self.load_button = QPushButton("Load File")
        self.back_button = QPushButton("Back")

        self.editor = Editor()

        button_menu.addWidget(self.start_button)
        button_menu.addWidget(self.next_button)
        button_menu.addWidget(self.load_button)
        button_menu.addWidget(self.back_button)

        info_button = QPushButton("More Informations")
        placeholder = QPlainTextEdit()

        main_layout.addLayout(button_menu, 0, 0)
        main_layout.addWidget(self.editor, 1, 0)
        main_layout.addWidget(placeholder, 1, 1)
        main_layout.addWidget(info_button, 0, 1)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.i = 0

        self.load_file(filename="example_files/instructions.txt")
        block = self.editor.get_block()
        print(block)

    def _connect_ui_signals(self):
        self.load_button.clicked.connect(self.load_files)
        self.start_button.clicked.connect(self.run)
        self.next_button.clicked.connect(self.move)
        self.back_button.clicked.connect(self.back)

    def back(self):
        self.i -= 1
        self.editor.move_cursor(self.i - 1)

    def move(self):
        self.editor.move_cursor(self.i)
        self.i += 1

    def run(self):
        instructions = self.editor.toPlainText().split("\n")

    def load_files(self):
        print("open_files")
        dialog = QFileDialog(self)
        dialog.setDirectory("/Users/michi/Projects/RISC-V-Emulator")
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            # TODO: Only one file
            filenames = dialog.selectedFiles()
            if filenames:
                print(filenames)
                files = [str(Path(filename)) for filename in filenames]
                print(files)
                for f in filenames:
                    self.load_file(str(f))
                return filenames

    def update(self):
        for a in self.input_arry:
            self.editor.append_html(a)

    def load_file(self, filename):
        with open(filename) as filename:
            lines = filename.readlines()

        for line in lines:
            self.input_arry.append(line)
        self.update()

    def check_pattern(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    window = MainWindow()
    window.setMaximumSize(1000, 1000)
    window.show()

    app.exec()
