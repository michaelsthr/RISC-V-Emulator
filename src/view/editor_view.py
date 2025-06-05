from PySide6.QtWidgets import QPlainTextEdit, QTextEdit
from PySide6.QtGui import QFont, QColor, QTextFormat
from loguru import logger


class Editor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        font = QFont("PT Mono")
        font.setPixelSize(20)
        self.setFont(font)

        logger.info("InputBox created")

    def append_html(self, text: str):
        # TODO: Zero is here twice
        # TODO: Color is not fixed
        # text = text.replace(" ", "&nbsp;")
        self.appendHtml(text)

    def move_cursor(self, line_number: int):
        self._unhighlight_block()
        block = self.document().findBlockByLineNumber(line_number)
        block_pos = block.position()

        cursor = self.textCursor()
        cursor.setPosition(block_pos)
        self.setTextCursor(cursor)

        self._highlight_block(color="darkorange")

        logger.info(
            f"Current Block: [{self.get_block()}] Cursor block_pos: {block_pos}, line_number: {line_number} "
        )

    def _highlight_block(self, color: str):
        extra_selection = QTextEdit.ExtraSelection()
        extra_selection.format.setBackground(QColor(color))
        extra_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        extra_selection.cursor = self.textCursor()
        self.setExtraSelections([extra_selection])

    def _unhighlight_block(self):
        self.setExtraSelections([])

    def get_text(self) -> list:
        return self.toPlainText().split("\n")

    def get_block(self) -> str:
        return self.textCursor().block().text()

    def get_line_number(self) -> int:
        return self.textCursor().blockNumber()

    def set_read_mode(self, mode: bool):
        self.setReadOnly(mode)
        logger.info(f"Read mode set to: {mode}")

    def finish_debug_cursor(self):
        self._unhighlight_block()