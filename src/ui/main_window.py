from src.utils.helpers import get_available_themes
from src.utils.logger import get_logger
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, YES, X
from src.assets.bootstrap import (
    set_theme,
)
from src.settings.settings import Settings
from src.settings.config_manager import ConfigManager
from src.ui.content_view import ContentView
from src.ui.components.settings_dialog import SettingsDialog

logger = get_logger()


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.config_manager = ConfigManager()
        self.setup_layout()
        self.create_menu()

    def setup_layout(self):
        # Main container
        self.container = ttk.Frame(self.master, padding=15)
        self.container.pack(fill=BOTH, expand=YES)

        # Create a header section
        self.create_header()
        logger.info("Header created")

        # Create main content section
        self.create_content()
        logger.info("Content created")

        # Create footer with theme switcher
        self.create_footer()
        logger.info("Footer created")

        # Apply the configured theme
        self.change_theme(self.config_manager.current_theme)

    def create_menu(self):
        # Create menu bar
        self.menu_bar = ttk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # File menu
        file_menu = ttk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Add settings option to file menu
        file_menu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

    def create_header(self):
        # Header with title and subtitle
        header_frame = ttk.Frame(self.container)
        header_frame.pack(fill=X, pady=(0, 15))

        title = ttk.Label(
            header_frame,
            text=Settings.NAME_APP,
            font=("Helvetica", 24, "bold"),
        )
        title.pack(pady=(0, 5))

        subtitle = ttk.Label(
            header_frame,
            text=f"v{Settings.VERSION}",
            font=("Helvetica", 12),
        )
        subtitle.pack()

    def create_content(self):
        # Create main content using ContentView class
        self.content_view = ContentView(self.container)

    def create_footer(self):
        # Footer with theme switcher
        footer_frame = ttk.Frame(self.container)
        footer_frame.pack(fill=X, pady=(15, 0))

        # Theme selection
        ttk.Label(footer_frame, text="Select Theme:").pack(side=LEFT)
        themes = get_available_themes()
        self.theme_combo = ttk.Combobox(footer_frame, values=themes, width=15)
        self.theme_combo.set(self.config_manager.current_theme)
        self.theme_combo.pack(side=LEFT, padx=5)

        # Apply theme button
        apply_btn = ttk.Button(
            footer_frame,
            text="Apply Theme",
            style="info",
            command=lambda: self.change_theme(self.theme_combo.get()),
        )
        apply_btn.pack(side=LEFT, padx=5)

    def change_theme(self, theme_name):
        logger.info(f"Changing theme to: {theme_name}")
        set_theme(self.master, theme_name)
        # Update the config manager with the new theme
        self.config_manager.set_theme(theme_name)
        # Update combobox if it exists
        if hasattr(self, "theme_combo"):
            self.theme_combo.set(theme_name)

    def open_settings(self):
        """Open the settings dialog"""
        logger.info("Opening settings dialog")
        SettingsDialog(self.master, on_settings_changed=self.change_theme)

    def show_message(self, message):
        """Show a message dialog centered within the application window.

        Args:
            message: The message to display
        """
        logger.info(f"Showing message: {message}")
        from src.utils.helpers import show_app_centered_message

        show_app_centered_message(self.master, "Message", message, "OK", "primary")
