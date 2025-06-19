# 🚀 ChatGPT Assistant Desktop App

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Platform](https://img.shields.io/badge/platform-Windows-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

<p align="center">
  <img src="https://raw.githubusercontent.com/TkinterEP/ttkbootstrap/main/docs/assets/themes/themes.gif" alt="Screenshot of application" width="600"/>
</p>

## 📖 Overview

ChatGPT Assistant is a modern desktop application built with Python's Tkinter and ttkbootstrap, providing a beautiful and responsive user interface. The application features a customizable theme system, screenshot capabilities, and integration with external services.

<video width="600" controls>
  <source src="https://github.com/MinhPhanCoder/Chatgpt_Support_App_demo/blob/main/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## ✨ Features

- 🎨 **Sleek UI**: Modern interface built with ttkbootstrap themes
- 🔄 **Real-time API Integration**: Seamless connection with Retool API services
- 📸 **Screenshot Capability**: Capture and process screen content
- 🛠️ **Customizable Settings**: Adjust application parameters through a user-friendly interface
- 📝 **Logging System**: Comprehensive application logging for troubleshooting
- 🔌 **Modular Architecture**: Well-structured codebase for easy maintenance and extension

## 🔧 Installation

### Prerequisites
- Python 3.11+
- Pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tkinter-bootstrap-app.git
cd tkinter-bootstrap-app
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## 📦 Building an Executable

The project includes PyInstaller configuration for creating standalone executables:

```bash
python build_exe.py
```

The executable will be created in the `build/ChatGPT Assistant` directory.

## 🏗️ Project Structure

```
chatgpt_app/
├── main.py                 # Application entry point
├── build_exe.py            # Script for building executable
├── requirements.txt        # Project dependencies
├── config/                 # Configuration files
│   └── app_config.json     # Application configuration
├── src/                    # Source code
│   ├── assets/             # Application assets
│   ├── core/               # Core functionality
│   ├── logs/               # Log files
│   ├── screenshots/        # Screenshot storage
│   ├── services/           # API and service integrations
│   ├── settings/           # Application settings
│   ├── ui/                 # User interface components
│   │   ├── components/     # Reusable UI components
│   │   └── renderers/      # Content rendering
│   └── utils/              # Utility functions
└── build/                  # Build outputs
```

## 🖥️ Usage

1. Launch the application
2. Use the GUI to interact with the ChatGPT API
3. Customize themes using the theme selector in the footer
4. Access additional settings through the File menu

## ⚙️ Configuration

The application can be configured through the `config/app_config.json` file or via the Settings dialog within the application.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

<p align="center">
  Made with ❤️ using Python and ttkbootstrap
</p>