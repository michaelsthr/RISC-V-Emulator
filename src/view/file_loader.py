from PySide6.QtWidgets import QFileDialog
from pathlib import Path


class FileLoader:
    def __init__(self, parent):
        self.parent = parent

    def read_file(self, filename):
        with open(filename, "r") as file:
            for line in file:
                yield line

    def import_from_dialog(self):
        # TODO: Check no file
        dialog = QFileDialog(self.parent)
        dialog.setDirectory("/Users/michi/Projects/RISC-V-Emulator")
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setViewMode(QFileDialog.ViewMode.List)
        dialog.setNameFilter("Text (*.txt)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            print(str(Path(filenames[0])))
            return self.read_file(str(Path(filenames[0])))
