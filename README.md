# Docky 🐳

![Docky Logo](https://via.placeholder.com/150x150.png?text=Docky)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Docky is an open-source, cross-platform Docker management application built with Python and Qt. It aims to provide a user-friendly interface for managing Docker containers, images, volumes, and networks, similar to Docker Desktop. Pretty much a light-weight docker desktop client

## 🚀 Features

- **Container Management**: View, start, stop, and remove containers
- **Image Management**: List, pull, and remove Docker images
- **Volume Management**: Create, list, and delete volumes
- **Network Management**: View and manage Docker networks
- **Docker Compose Integration**: Manage multi-container applications
- **Kubernetes Support**: Basic Kubernetes cluster management
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **User-Friendly Interface**: Intuitive design inspired by Docker Desktop

## 📋 Prerequisites (for Dev)

- Python 3.8 or higher
- Docker Engine installed and running on your system
- PySide6 (Qt for Python)

## 🛠️ Installation (for Dev)

1. Clone the repository:
   ```
   git clone https://github.com/SaifuddinSaifee/docky.git
   cd docky
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run Docky:
   ```
   python src/main.py
   ```

## 🖥️ Usage

After launching Docky, you'll be presented with the main interface:

- Use the sidebar to navigate between different views (Containers, Images, etc.)
- The main area displays details and controls for the selected view
- Use the top bar for global actions like searching and accessing settings

For more detailed instructions, please refer to our [User Guide](docs/user_guide.md).

## 📷 Screenshots



## 🤝 Contributing

We welcome contributions to Docky! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details on how to get started.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Docker for inspiration and the amazing containerization technology
- The Qt Company for the Qt framework
- All our contributors and supporters

---

📌 **Note**: Docky is currently under active development. Features and interfaces may change as the project evolves.