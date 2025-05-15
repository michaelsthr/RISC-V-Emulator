from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtGui import QTextCursor
from PySide6.QtGui import QFont, QColor, QBrush, QTextCharFormat
from PySide6 import QtGui
from loguru import logger


class Editor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        font = QFont()
        font.setPixelSize(20)
        font.setFamilies("monospace")
        self.setFont(font)

        logger.info("InputBox created")

    def append_html(self, text: str):
        logger.info(f"Append HTML: {text}")
        # TODO: Zero is here twice
        # TODO: Color is not fixed
        # self.appendHtml(f"<font color='gray'>{self.blockCount()}</font>\t{text}")
        self.appendHtml(text)

    def move_cursor(self, line_number: int):
        self._unhighlight_block()
        block = self.document().findBlockByLineNumber(line_number)
        block_pos = block.position()

        cursor = self.textCursor()
        cursor.setPosition(block_pos)
        self.setTextCursor(cursor)

        self._highlight_block(color="orange")

        logger.info(f"Current Block: [{self.get_block()}] Cursor block_pos: {block_pos}, line_number: {line_number} ")

    def _highlight_block(self, color: str):
        char_format = QTextCharFormat()
        char_format.setForeground(QBrush(QColor(color)))
        char_format.setFontItalic(True)
        char_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SingleUnderline)

        cursor: QTextCursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfBlock)
        cursor.select(QTextCursor.BlockUnderCursor)
        cursor.setCharFormat(char_format)

    def _unhighlight_block(self):
        cursor: QTextCursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        cursor.setCharFormat(QtGui.QTextCharFormat())

    def get_text(self) -> list:
        return self.toPlainText().split("\n")

    def get_block(self) -> str:
        return self.textCursor().block().text()