"""
Main layout component that coordinates the overall UI structure.
"""

import time
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, RIGHT, YES
from src.utils.logger import get_logger
from src.ui.components.preview_panel import PreviewPanel
from src.ui.components.answer_panel import AnswerPanel

logger = get_logger()


class MainLayout:
    """Main layout manager that coordinates the preview and answer panels."""

    def __init__(self, parent):
        """
        Initialize the main layout.

        Args:
            parent: The parent widget
        """
        self.parent = parent
        self.last_resize_time = 0
        self.original_screenshot = None
        self.last_window_width = None
        self.last_window_height = None

        # Create main content frame
        self.content_frame = ttk.Frame(self.parent)
        self.content_frame.pack(fill=BOTH, expand=YES, pady=10)

        # Set up the layout with preview and answer panels
        self.setup_layout()

        # Bind resize event
        self.parent.bind("<Configure>", self.on_window_resize)
        root = self.parent.winfo_toplevel()
        root.bind("<Configure>", self.on_window_resize)

    def setup_layout(self):
        """Set up the main layout with preview and answer panels."""
        # Split into two columns: Preview and Answer with 2:1 ratio
        self.preview_frame = ttk.Labelframe(
            self.content_frame, text="Preview", padding=10, width=500
        )
        self.preview_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 5))
        self.preview_frame.pack_propagate(False)

        self.answer_frame = ttk.Labelframe(
            self.content_frame, text="Answer", padding=10, width=250
        )
        self.answer_frame.pack(side=RIGHT, fill=BOTH, expand=YES, padx=(5, 0))
        self.answer_frame.pack_propagate(False)

        # Initialize preview panel
        self.preview_panel = PreviewPanel(self.preview_frame, self)

        # Initialize answer panel
        self.answer_panel = AnswerPanel(self.answer_frame, self)

    def on_window_resize(self, event):
        """Update the layout on window resize with throttling."""
        # Skip if not from parent or root window
        if event.widget != self.parent and event.widget != self.parent.master:
            return

        current_width = self.parent.winfo_width()
        current_height = self.parent.winfo_height()

        # Only proceed if dimensions actually changed
        if (
            self.last_window_width != current_width
            or self.last_window_height != current_height
        ):
            current_time = time.time()
            # Throttle updates to avoid excessive resizing calculations
            if current_time - self.last_resize_time < 0.1:
                return

            # Resize image in preview area if there's one
            self.preview_panel.resize_image()

            # Update the preview and answer frames to maintain a 2:1 ratio
            total_width = self.content_frame.winfo_width()
            if total_width > 100:  # Only adjust if valid dimensions
                # Calculate width for preview (2/3) and answer (1/3) frames
                preview_width = int(total_width * 0.67)  # Approximately 2/3
                answer_width = total_width - preview_width

                # Update the widths
                self.preview_frame.configure(width=preview_width)
                self.answer_frame.configure(width=answer_width)

            # Update timing and dimensions for next resize
            self.last_resize_time = current_time
            self.last_window_width = current_width
            self.last_window_height = current_height

    def get_content_frame(self):
        """Return the main content frame."""
        return self.content_frame

    def set_screenshot(self, image):
        """Set the current screenshot image.

        Args:
            image: PIL Image object
        """
        if image:
            self.original_screenshot = image.copy()
            # Update the preview with the new image
            self.preview_panel.set_image(self.original_screenshot)

    def analyze_screenshot(self):
        """Delegate screenshot analysis to the answer panel."""
        if self.original_screenshot is None:
            logger.warning("No screenshot available to analyze")

            # Use the common message dialog function with English message
            from src.utils.helpers import show_app_centered_message

            show_app_centered_message(
                self.parent,
                "Notification",
                "Please take a screenshot before analyzing",
                "OK",
                "primary",
            )

            # Update the answer panel text
            self.answer_panel.set_answer_text(
                "Please take a screenshot before analyzing"
            )
            return

        self.answer_panel.analyze_screenshot(self.original_screenshot)
