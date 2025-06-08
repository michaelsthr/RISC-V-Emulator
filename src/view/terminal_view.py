from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QFont
from ansi2html import Ansi2HTMLConverter


class Terminal(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        font = QFont("PT Mono")
        font.setPixelSize(16)
        self.setFont(font)
        self.setReadOnly(True)

        self.conv = Ansi2HTMLConverter()

    def append_text(self, text: str):
        text = text.rstrip("\n")
        text = self.conv.convert(text)
        self.appendHtml(text)
