from PySide6.QtWidgets import QFileDialog
from pathlib import Path


class FileLoader:
    # TODO: change
    DEFAULT_DIR = "/Users/michi/Projects/RISC-V-Emulator"

    def __init__(self, parent):
        self.parent = parent

    def read_file(self, filename):
        with open(filename, "r") as file:
            for line in file:
                yield line

    def import_from_dialog(self):
        # TODO: Check no file
        dialog = QFileDialog(self.parent)
        dialog.setDirectory(self.DEFAULT_DIR)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setViewMode(QFileDialog.ViewMode.List)
        # TODO: change filter
        dialog.setNameFilter("Text (*.txt)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            return self.read_file(str(Path(filenames[0])))
