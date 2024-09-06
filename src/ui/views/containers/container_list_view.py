# ui/views/containers/container_list_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox
from PySide6.QtCore import Qt
from src.core.services.container_service import get_containers

class ContainerListView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("Containers")
        title.setStyleSheet("font-size: 24px; padding: 20px 0;")
        layout.addWidget(title)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # 5 columns + 1 for checkbox
        self.table.setHorizontalHeaderLabels(["", "Name", "Image", "Status", "Port(s)", "Created"])
        self.table.setStyleSheet(f"""
            QTableWidget {{
                border: none;
            }}
            QHeaderView::section {{
                padding: 4px;
                border: none;
                font-weight: bold;
            }}
        """)

        # Make columns resizable by dragging
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        layout.addWidget(self.table)

        # Populate with sample data
        self.populate_sample_data()

    def populate_sample_data(self):
        container_data = get_containers()

        self.table.setRowCount(len(container_data))
        for row, container in enumerate(container_data):
            # Add checkbox to the first column
            checkbox = QCheckBox()
            checkbox.setStyleSheet("margin-left: 10px; margin-right: 10px;")  # Optional styling
            checkbox.setChecked(False)
            self.table.setCellWidget(row, 0, checkbox)

            # Add the rest of the container data
            container_tuple = container.to_tuple()  # Extract the tuple representation
            for col, value in enumerate(container_tuple):
                self.table.setItem(row, col + 1, QTableWidgetItem(value))

