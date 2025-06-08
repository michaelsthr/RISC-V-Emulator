from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QLabel,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from loguru import logger

from src.model.ram import RAM


class RAMView(QWidget):
    FONT = "PT Mono"

    def __init__(self, ram: RAM):
        super().__init__()

        layout = QVBoxLayout(self)
        label = QLabel("RAM")
        label.setFont(QFont("PT Mono", 16, QFont.Bold))
        layout.addWidget(label)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        # font
        font = QFont("PT Mono")
        font.setPixelSize(16)
        self.table_widget.setFont(font)

        # table setup
        self.table_widget.setColumnCount(4)
        headers = ["Reg", "Base2", "Base10", "Base16"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        header: QHeaderView = self.table_widget.horizontalHeader()
        header.setFont(self.FONT)

        # Interactive               = ...  # 0x0
        # Stretch                   = ...  # 0x1
        # Custom                    = ...  # 0x2
        # Fixed                     = ...  # 0x2
        # ResizeToContents          = ...  # 0x3
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setShowGrid(False)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.align_left_vcenter = (
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.update_registers(ram)

    def update_registers(self, ram: RAM):
        len_reg = len(ram)
        self.table_widget.setRowCount(len_reg)
        for idx, (adress, word) in enumerate(list(ram.items())):
            # register name
            name_item = QTableWidgetItem(f"x{adress}")
            name_item.setFont(self.FONT)
            name_item.setTextAlignment(self.align_left_vcenter)
            self.table_widget.setItem(idx, 0, name_item)

            # binary
            bin_item = QTableWidgetItem(word.bin)
            bin_item.setFont(self.FONT)
            bin_item.setTextAlignment(self.align_left_vcenter)
            self.table_widget.setItem(idx, 1, bin_item)

            # decimal
            dec_item = QTableWidgetItem(str(word.dez))
            dec_item.setFont(self.FONT)
            dec_item.setTextAlignment(self.align_left_vcenter)
            self.table_widget.setItem(idx, 2, dec_item)

            # hex
            hex_item = QTableWidgetItem(word.hex)
            hex_item.setFont(self.FONT)
            hex_item.setTextAlignment(self.align_left_vcenter)
            self.table_widget.setItem(idx, 3, hex_item)

            self.table_widget.setRowHeight(idx, 1)
