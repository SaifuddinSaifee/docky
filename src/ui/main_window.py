# ui/main_window.py
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QStackedWidget
from .sidebar import Sidebar
from .views.containers.container_list_view import ContainerListView
from .views.images.image_list_view import ImageListView
from .views.volumes.volume_list_view import VolumeListView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Docker Desktop Clone")
        self.setGeometry(100, 100, 1200, 800)

        # Create main layout
        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create and add sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # Create stack for main content
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)

        # Add views to the stack
        self.container_view = ContainerListView()
        self.image_view = ImageListView()
        self.volume_view = VolumeListView()

        self.content_stack.addWidget(self.container_view)
        self.content_stack.addWidget(self.image_view)
        self.content_stack.addWidget(self.volume_view)

        # Connect sidebar signals
        self.sidebar.containers_clicked.connect(lambda: self.content_stack.setCurrentWidget(self.container_view))
        self.sidebar.images_clicked.connect(lambda: self.content_stack.setCurrentWidget(self.image_view))
        self.sidebar.volumes_clicked.connect(lambda: self.content_stack.setCurrentWidget(self.volume_view))