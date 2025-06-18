"""
Main content view that serves as entry point for the application UI.
"""

from src.utils.logger import get_logger
from src.ui.components.main_layout import MainLayout

logger = get_logger()


class ContentView:
    """Main content view that delegates to specialized components."""

    def __init__(self, parent):
        """
        Initialize the content view.

        Args:
            parent: The parent widget
        """
        self.parent = parent
        self.layout = MainLayout(parent)

    def get_content_frame(self):
        """Return the main content frame."""
        return self.layout.get_content_frame()
