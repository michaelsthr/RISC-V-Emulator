from PySide6.QtWidgets import QApplication
import qdarktheme
import sys

from src.controller import Controller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("dark"))

    controller: Controller = Controller()

    app.exec()
