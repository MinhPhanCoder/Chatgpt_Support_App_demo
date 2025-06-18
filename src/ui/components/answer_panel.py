"""
Answer panel component for displaying API responses and analysis results.
"""

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, RIGHT, YES, X, Y, CENTER
import threading
from datetime import datetime
from src.utils.logger import get_logger
from src.assets.bootstrap import create_widget
from src.services.retool_api_service import RetoolAPIService
from src.settings.settings import Settings
from src.ui.renderers.api_response_renderer import APIResponseRenderer

logger = get_logger()


class AnswerPanel:
    """Panel for displaying answer content and API responses."""

    def __init__(self, parent, main_layout):
        """
        Initialize the answer panel.

        Args:
            parent: The parent widget
            main_layout: Reference to the main layout manager
        """
        self.parent = parent
        self.main_layout = main_layout
        self.renderer = APIResponseRenderer()
        self.is_loading = False

        # Set up the UI elements
        self.setup_content()

    def setup_content(self):
        """Set up the answer panel UI elements."""
        # Button frame for answer actions - moved to top
        button_frame = ttk.Frame(self.parent)
        button_frame.pack(fill=X, pady=5)

        # Add action buttons (aligned to RIGHT to match preview panel)
        button_container = ttk.Frame(button_frame)
        button_container.pack(side=RIGHT, pady=2)

        clear_btn = create_widget(
            button_container,
            "Button",
            style="secondary",
            text="Clear",
            command=self.clear_answer,
        )
        clear_btn.pack(side=LEFT, padx=3)

        copy_btn = create_widget(
            button_container,
            "Button",
            style="info",
            text="Copy",
            command=self.copy_answer,
        )
        copy_btn.pack(side=LEFT, padx=3)

        # Create a frame for loading indicator
        self.loading_frame = ttk.Frame(self.parent)
        self.loading_frame.pack(fill=X, pady=(0, 5))

        # Create loading progress bar
        self.loading_progress = create_widget(
            self.loading_frame,
            "Progressbar",
            style="info",
            mode="indeterminate",
            length=200,
        )
        self.loading_progress.pack(pady=5, fill=X)

        # Create loading label
        self.loading_label = ttk.Label(
            self.loading_frame,
            text="Processing API request...",
            font=("Helvetica", 9),
            anchor=CENTER,
        )
        self.loading_label.pack(pady=(0, 5), fill=X)

        # Hide loading components initially
        self.loading_frame.pack_forget()

        # Create a frame for the text area and scrollbar
        text_frame = ttk.Frame(self.parent)
        text_frame.pack(fill=BOTH, expand=YES, pady=3)

        # Text area for displaying answers
        self.answer_text = tk.Text(
            text_frame,
            height=15,
            width=30,
            wrap="word",
            font=("Consolas", 10),
            padx=8,
            pady=5,
        )
        self.answer_text.pack(side=LEFT, fill=BOTH, expand=YES)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(text_frame, command=self.answer_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.answer_text.config(yscrollcommand=scrollbar.set)

    def clear_answer(self):
        """Clear the answer text."""
        logger.info("Clearing answer text")
        self.answer_text.config(state="normal")
        self.answer_text.delete("1.0", "end")
        self.answer_text.config(state="disabled")

    def copy_answer(self):
        """Copy answer text to clipboard."""
        logger.info("Copying answer to clipboard")
        answer_text = self.answer_text.get("1.0", "end-1c")
        self.parent.clipboard_clear()
        self.parent.clipboard_append(answer_text)

    def set_answer_text(self, text):
        """Set the answer text content.

        Args:
            text: The text to display
        """
        self.answer_text.config(state="normal")
        self.answer_text.delete("1.0", "end")
        self.answer_text.insert("1.0", text)
        self.answer_text.config(state="disabled")

    def show_loading_indicator(self):
        """Show the loading indicator and start animation."""
        self.is_loading = True
        self.loading_frame.pack(
            fill=X, pady=(0, 5), after=self.parent.winfo_children()[0]
        )
        self.loading_progress.start(10)  # Start animation with 10ms between updates

    def hide_loading_indicator(self):
        """Hide the loading indicator and stop animation."""
        self.is_loading = False
        self.loading_progress.stop()
        self.loading_frame.pack_forget()

    def analyze_screenshot(self, image):
        """Analyze the provided screenshot image using the Retool API.

        Args:
            image: PIL Image object to analyze
        """
        # Clear previous answer
        self.clear_answer()
        logger.info("Analyzing screenshot")

        # Show loading message in text area
        self.set_answer_text("Analyzing screenshot... please wait")

        # Show loading indicator
        self.show_loading_indicator()

        self.parent.update_idletasks()

        # Run API call in a background thread
        threading.Thread(
            target=self._analyze_screenshot_thread, args=(image,), daemon=True
        ).start()

    def _analyze_screenshot_thread(self, image):
        """Background thread for running API analysis.

        Args:
            image: PIL Image object to analyze
        """
        from src.services.screenshot_service import ScreenshotService

        screenshot_service = ScreenshotService()
        screenshot_service.image = image.copy()
        base64_image = screenshot_service.get_image_as_base64()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_{timestamp}.png"

        api_service = RetoolAPIService()
        response_answer = api_service.send_request(
            user_name=Settings.DEFAULT_USERNAME,
            user_id=Settings.DEFAULT_USER_ID,
            file_name=filename,
            image_data=base64_image,
        )

        # Schedule UI update on main thread
        self.parent.after(0, lambda: self._handle_api_response(response_answer))

    def _handle_api_response(self, api_response):
        """Handle the API response and hide loading indicator.

        Args:
            api_response: The API response dictionary
        """
        # Hide loading indicator first
        self.hide_loading_indicator()

        # Then render the response
        self.render_api_response(api_response)

    def render_api_response(self, api_response):
        """Render the formatted API response in the answer section.

        Args:
            api_response: The API response dictionary
        """
        # Delegate to the specialized renderer
        self.renderer.render(self.answer_text, api_response)
