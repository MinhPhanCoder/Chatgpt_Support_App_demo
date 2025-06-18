from src.ui.main_window import MainWindow
from src.settings.settings import Settings
from src.utils.logger import get_logger
import ttkbootstrap as ttk

# Initialize logger
logger = get_logger()


def main():
    logger.info("Application starting")
    root = ttk.Window(title=Settings.TITLE_APP, themename=Settings.DEFAULT_THEME)
    root.geometry(Settings.WINDOWN_SIZE)
    logger.info(f"Window created with theme: {Settings.DEFAULT_THEME}")

    MainWindow(root)
    logger.info("Main window initialized")
    root.mainloop()


if __name__ == "__main__":
    main()
