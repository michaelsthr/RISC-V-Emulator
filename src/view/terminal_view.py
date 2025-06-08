from PySide6.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QFont
from ansi2html import Ansi2HTMLConverter


class Terminal(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        label = QLabel("TERMINAL")
        label.setFont(QFont("PT Mono", 16, QFont.Bold))
        layout.addWidget(label)

        self.terminal = QPlainTextEdit()
        layout.addWidget(self.terminal)

        font = QFont("PT Mono")
        font.setPixelSize(16)
        self.terminal.setFont(font)
        self.terminal.setReadOnly(True)

        self.conv = Ansi2HTMLConverter()


    def append_text(self, text: str):
        text = text.rstrip("\n")
        text = self.conv.convert(text)
        self.terminal.appendHtml(text)

    def clear(self):
        self.terminal.clear()
