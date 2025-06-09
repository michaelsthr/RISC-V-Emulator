from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QVBoxLayout,
    QLabel, 
    QWidget
)
from PySide6.QtGui import QColor, QFont, QPixmap, QPainter
from PySide6.QtCore import Qt

from src.model.register_set import RegisterSet


class RegisterSetView(QWidget):
    FONT = "PT Mono"

    def __init__(self, register_set: RegisterSet):
        super().__init__()

        layout = QVBoxLayout(self)
        label = QLabel("REGISTER SET")
        label.setFont(QFont("PT Mono", 16, QFont.Bold))
        label.setFixedHeight(40)
        layout.addWidget(label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        # font
        font = QFont("PT Mono")
        font.setPixelSize(16)
        self.table.setFont(font)

        # table setup
        self.table.setColumnCount(4)
        headers = ["Reg", "Base2", "Base10", "Base16"]
        self.table.setHorizontalHeaderLabels(headers)
        header: QHeaderView = self.table.horizontalHeader()
        header.setFont(self.FONT)

        # Interactive               = ...  # 0x0
        # Stretch                   = ...  # 0x1
        # Custom                    = ...  # 0x2
        # Fixed                     = ...  # 0x2
        # ResizeToContents          = ...  # 0x3
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.align_left_vcenter = (
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.update_registers(register_set)

    def update_registers(self, registers: RegisterSet):
        len_reg = len(registers)
        self.table.setRowCount(len_reg)
        for idx in range(len_reg):
            word = registers[idx]

            # pixmap = self.get_pixmap(idx)
            # icon = QIcon(pixmap)

            # register name
            name_item = QTableWidgetItem(f"x{idx}")
            name_item.setFont(self.FONT)
            # name_item.setIcon(icon)
            name_item.setTextAlignment(self.align_left_vcenter)
            self.table.setItem(idx, 0, name_item)

            # binary
            bin_item = QTableWidgetItem(word.bin)
            bin_item.setFont(self.FONT)
            bin_item.setTextAlignment(self.align_left_vcenter)
            self.table.setItem(idx, 1, bin_item)

            # decimal
            dec_item = QTableWidgetItem(str(word.dez))
            dec_item.setFont(self.FONT)
            dec_item.setTextAlignment(self.align_left_vcenter)
            self.table.setItem(idx, 2, dec_item)

            # hex
            hex_item = QTableWidgetItem(word.hex)
            hex_item.setFont(self.FONT)
            hex_item.setTextAlignment(self.align_left_vcenter)
            self.table.setItem(idx, 3, hex_item)

            self.table.setRowHeight(idx, 1)

    # obsolete
    def get_pixmap(self, idx: int) -> QPixmap:
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
