from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QListWidget, QListWidgetItem
from PySide6.QtGui import QIcon, QColor, QFont
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt, QSize


class Register(QListWidget):
    def __init__(self, size: int):
        super().__init__()
        layout = QVBoxLayout()
        self.labels: list = []

        for idx in range(size):
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor(32, 33, 36, 255))
            painter = QPainter(pixmap)
            painter.setPen(QColor(82, 178, 220))
            font = painter.font()
            font.setPixelSize(20)
            painter.setFont(font)
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignLeft, f"x{idx}")
            painter.end()
            item = QListWidgetItem(pixmap, f"0000 0000")
            self.addItem(item)
            # self.addItem(f"x{str(idx)}")
            # label = QLabel(f"x{str(idx)}")
            # label.setStyleSheet("background-color: rgb(73, 73, 73);")
            # self.labels.append(label)
        
        # for label in self.labels:
        #     self.addItem(label)

        self.setLayout(layout)

    def get_register_value(self, index: int):
        label: QLabel = self.labels[index]
        return label.text()
    
    def set_register_value(self, index: int, value: str):
        label: QLabel = self.labels[index]
        label.setText(value)