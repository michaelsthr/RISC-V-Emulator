from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtGui import QFont

class Label(QWidget):
    def __init__(self, heading: str, init_value: str):
        super().__init__()
        layout = QHBoxLayout(self)
        label = QLabel(heading)
        font = QFont("PT Mono", 16, QFont.Bold)
        label.setFont(font)
        layout.addWidget(label)

        self.value_label = QLabel(init_value)
        self.value_label.setFont(font)
        layout.addWidget( self.value_label)

    def set_value(self, value: str):
        self.value_label.setText(value)