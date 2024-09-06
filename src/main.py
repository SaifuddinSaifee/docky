import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.docker_engine import DockerEngineManager

def main():

    # Check if Docker is running
    if not DockerEngineManager.is_docker_running():
        print("Docker is not running. Attempting to start...")
        success = DockerEngineManager.start_docker_engine()
        if not success:
            print(f"Failed to start Docker")
            sys.exit(1)
        print("Docker started successfully.")

if __name__ == "__main__":
    main()
    # Create and show the main window
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())