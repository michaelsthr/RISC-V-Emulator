from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QListWidget, QListWidgetItem
from PySide6.QtGui import QIcon, QColor, QFont
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt, QSize

from src.model.register import Registers


class RegisterView(QListWidget):
    def __init__(self, registers: Registers):
        super().__init__()
        layout = QVBoxLayout()

        self.update_registers(registers)
        self.setLayout(layout)

    def update_registers(self, registers: Registers):
        self.clear()
        for idx in range(len(registers)):
            register = registers[idx]

            pixmap = self.get_pixmap(idx=idx)
            icon = QIcon(pixmap)
            item = QListWidgetItem(icon, f"{register}")
            self.addItem(item)

    def get_pixmap(self, idx: str):
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor(32, 33, 36, 255))
        painter = QPainter(pixmap)
        painter.setPen(QColor(82, 178, 220))
        font = painter.font()
        font.setPixelSize(20)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignLeft, f"x{idx}")
        painter.end()

        return pixmap
