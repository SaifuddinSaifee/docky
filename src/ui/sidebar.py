# ui/sidebar.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QIcon, QFont
# from .style.colors import Colors

class SidebarButton(QPushButton):
    def __init__(self, text, icon_path):
        super().__init__(text)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(24, 24))
        self.setCheckable(True)
        self.setAutoExclusive(True)
        # self.setStyleSheet(f"""
        #     SidebarButton {{
        #         # background-color: {Colors.DARK_BLUE};
        #         # color: {Colors.LIGHT_GRAY};
        #         border: none;
        #         padding: 10px;
        #         text-align: left;
        #         font-size: 14px;
        #     }}
        #     SidebarButton:checked {{
        #         background-color: {Colors.BLUE};
        #         color: {Colors.WHITE};
        #     }}
        #     SidebarButton:hover:!checked {{
        #         background-color: {Colors.DARK_GRAY};
        #     }}
        # """)

class Sidebar(QWidget):
    containers_clicked = Signal()
    images_clicked = Signal()
    volumes_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        # self.setStyleSheet(f"background-color: {Colors.DARK_BLUE};")

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Logo
        logo = QLabel("Docker")
        logo.setAlignment(Qt.AlignCenter)
        # logo.setStyleSheet(f"color: {Colors.WHITE}; font-size: 18px; padding: 20px 0;")
        layout.addWidget(logo)

        # Create sidebar buttons
        self.containers_btn = SidebarButton("Containers", "path/to/container_icon.png")
        self.images_btn = SidebarButton("Images", "path/to/image_icon.png")
        self.volumes_btn = SidebarButton("Volumes", "path/to/volume_icon.png")

        # Add buttons to layout
        layout.addWidget(self.containers_btn)
        layout.addWidget(self.images_btn)
        layout.addWidget(self.volumes_btn)
        layout.addStretch()

        # Connect buttons to signals
        self.containers_btn.clicked.connect(self.containers_clicked)
        self.images_btn.clicked.connect(self.images_clicked)
        self.volumes_btn.clicked.connect(self.volumes_clicked)

        # Set initial selection
        self.containers_btn.setChecked(True)