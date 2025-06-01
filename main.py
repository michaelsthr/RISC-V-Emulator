from loguru import logger
from PySide6.QtWidgets import QApplication

import sys

import qdarktheme
from src.controller import Controller


def __init_logger():
    logger.remove()  # Remove default logger configuration
    logger.add(sys.stdout, format="{message}", level="INFO")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet("dark"))

    __init_logger()
    controller: Controller = Controller()
    # controller.window.open_from_filename("example_files/3_BedingteVerzweigung(beq).txt")
    # controller.start_programm()

    app.exec()
