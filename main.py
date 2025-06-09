from PySide6.QtWidgets import QApplication

import sys

import qdarktheme
from src.controller import Controller


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("dark"))

    controller: Controller = Controller()

    controller.window.open_from_filename("example_files/example_2.s")
    controller.start_programm()

    app.exec()
