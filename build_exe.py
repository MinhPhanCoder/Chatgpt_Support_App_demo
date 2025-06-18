import os
from PyInstaller.__main__ import run

if __name__ == "__main__":
    exe_name = "ChatGPT Assistant"

    current_dir = os.path.abspath(os.path.dirname(__file__))

    config_dir = os.path.join(current_dir, "config")
    app_dir = os.path.join(current_dir, "app")
    src_dir = os.path.join(current_dir, "src")

    utils_dir = os.path.join(src_dir, "utils")
    ui_dir = os.path.join(src_dir, "ui")

    logs_dir = os.path.join(current_dir, "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    options = [
        f"--name={exe_name}",
        "--onefile",
        "--windowed",
        f"--add-data={config_dir};config",
        f"--add-data={os.path.join(src_dir, 'assets')};src/assets",
        f"--add-data={logs_dir};logs",
        "--clean",
        "--hidden-import=src.utils.logger",
        "--hidden-import=src.ui.main_window",
        "main.py",
    ]

    print(f"Building {exe_name} with the following options:")
    for opt in options:
        print(f"  {opt}")
    run(options)
