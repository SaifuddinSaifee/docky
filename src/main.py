import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.docker_manager import DockerManager

def main():
    app = QApplication(sys.argv)

    # Check if Docker is running
    if not DockerManager.is_docker_running():
        print("Docker is not running. Attempting to start...")
        success, message = DockerManager.start_docker()
        if not success:
            print(f"Failed to start Docker: {message}")
            sys.exit(1)
        print("Docker started successfully.")

    # Create and show the main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()