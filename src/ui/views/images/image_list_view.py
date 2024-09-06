from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ImageListView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Image List View"))
        self.setLayout(layout)