from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class VolumeListView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Volume List View"))
        self.setLayout(layout)