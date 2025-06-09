from PySide6.QtWidgets import (
    QPlainTextEdit,
    QTextEdit,
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtGui import QFont, QColor, QTextFormat
from PySide6.QtCore import Qt
from loguru import logger


class Editor(QWidget):
    def __init__(self):
        super().__init__()
        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        header_widget = QWidget()
        header_widget.setLayout(h_layout)
        header_widget.setFixedHeight(40)

        label = QLabel("EDITOR")
        label.setFont(QFont("PT Mono", 16, QFont.Bold))
        h_layout.addWidget(label)

        button_styleSheet = (
            "QPushButton {background-color: #e0e0e0;; border: 1px solid white; color: black;}"
            "QPushButton:hover {background-color: #e0e0e0;}"
            "QPushButton:pressed {background-color: #c0c0c0;}"
        )

        self.exec_step_button = QPushButton("Execute Step")
        self.exec_step_button.setStyleSheet(button_styleSheet)
        self.exec_step_button.setVisible(False)
        h_layout.addWidget(self.exec_step_button)

        self.exec_all_button = QPushButton("Execute All")
        self.exec_all_button.setStyleSheet(button_styleSheet)
        self.exec_all_button.setVisible(False)
        h_layout.addWidget(self.exec_all_button)

        self.editor = QPlainTextEdit()

        layout = QVBoxLayout(self)
        layout.addWidget(header_widget, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.editor)

        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        font = QFont("PT Mono")
        font.setPixelSize(20)
        self.editor.setFont(font)

        logger.info("InputBox created")

    def append_html(self, text: str):
        # TODO: Zero is here twice
        # TODO: Color is not fixed
        # text = text.replace(" ", "&nbsp;")
        self.editor.appendHtml(text)

    def move_cursor(self, line_number: int):
        self._unhighlight_block()
        block = self.editor.document().findBlockByLineNumber(line_number)
        block_pos = block.position()

        cursor = self.editor.textCursor()
        cursor.setPosition(block_pos)
        self.editor.setTextCursor(cursor)

        self._highlight_block(color="darkslategray")

    def _highlight_block(self, color: str):
        extra_selection = QTextEdit.ExtraSelection()
        extra_selection.format.setBackground(QColor(color))
        extra_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        extra_selection.cursor = self.editor.textCursor()
        self.editor.setExtraSelections([extra_selection])

    def _unhighlight_block(self):
        self.editor.setExtraSelections([])

    def get_text(self) -> list:
        return self.editor.toPlainText().split("\n")

    def get_block(self) -> str:
        return self.editor.textCursor().block().text()

    def get_line_number(self) -> int:
        return self.editor.textCursor().blockNumber()

    def set_read_mode(self, mode: bool):
        self.editor.setReadOnly(mode)
        logger.info(f"Read mode set to: {mode}")

    def finish_debug_cursor(self):
        self._unhighlight_block()

    def reset(self):
        self.editor.clear()
        self.set_header_buttons_visible(False)

    def set_header_buttons_visible(self, value: bool):
        self.exec_step_button.setVisible(value)
        self.exec_all_button.setVisible(value)
