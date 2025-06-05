from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QFont


class Terminal(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        font = QFont("PT Mono")
        font.setPixelSize(16)
        self.setFont(font)
        self.setReadOnly(True)

    def append_text(self, text: str):
        clean_text = text.rstrip("\n")
        self.appendPlainText(clean_text)
