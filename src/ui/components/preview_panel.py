"""
Preview panel component for displaying and capturing screenshots.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, RIGHT, YES, X, CENTER
from src.utils.logger import get_logger
from src.assets.bootstrap import create_widget
from PIL import ImageTk
from src.services.screenshot_service import ScreenshotService

logger = get_logger()


class PreviewPanel:
    """Panel for displaying screenshot previews and providing capture controls."""

    def __init__(self, parent, main_layout):
        """
        Initialize the preview panel.

        Args:
            parent: The parent widget
            main_layout: Reference to the main layout manager
        """
        self.parent = parent
        self.main_layout = main_layout
        self.screenshot_image = None
        self.original_image = None

        # Set up the UI elements
        self.setup_content()

    def setup_content(self):
        """Set up the preview panel UI elements."""
        # Create a frame to hold title and buttons at the top
        top_frame = ttk.Frame(self.parent)
        top_frame.pack(fill=X, pady=5)

        # Buttons frame for preview actions
        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(side=RIGHT, pady=2)

        # Add a screenshot button
        screenshot_btn = create_widget(
            btn_frame,
            "Button",
            style="success",
            text="Full Screen",
            command=self.take_screenshot,
        )
        screenshot_btn.pack(side=LEFT, padx=3)

        # Add region screenshot button
        region_screenshot_btn = create_widget(
            btn_frame,
            "Button",
            style="primary",
            text="Select Region",
            command=self.take_region_screenshot,
        )
        region_screenshot_btn.pack(side=LEFT, padx=3)

        # Add analyze button
        analyze_btn = create_widget(
            btn_frame,
            "Button",
            style="warning",
            text="Analyze",
            command=self.analyze_screenshot,
        )
        analyze_btn.pack(side=LEFT, padx=3)

        # Add a clear button (Changed from F5 to Clear)
        clear_btn = create_widget(
            btn_frame,
            "Button",
            style="info",
            text="Clear",
            command=self.refresh_preview,
        )
        clear_btn.pack(side=LEFT, padx=3)

        # Create a frame container for image that expands with the window
        self.image_container = ttk.Frame(self.parent)
        self.image_container.pack(fill=BOTH, expand=YES, pady=3)

        # Create a label to display the screenshot (centered)
        self.image_label = ttk.Label(self.image_container)
        self.image_label.pack(anchor=CENTER, expand=YES)

    def take_screenshot(self):
        """Capture full screen screenshot and display in preview area."""
        logger.info("Taking screenshot")

        # Use the screenshot service
        screenshot_service = ScreenshotService()

        # Set the root window to avoid capturing the app itself
        root = self.parent.winfo_toplevel()
        screenshot_service.set_root_window(root)

        # Take the screenshot
        screenshot_service.take_screenshot(save_to_disk=False)

        # Store the original image for resizing when window changes
        if screenshot_service.image:
            self.set_image(screenshot_service.image)
            # Also update the main layout's reference to the screenshot
            self.main_layout.set_screenshot(screenshot_service.image)

    def take_region_screenshot(self):
        """Capture screen region screenshot and display in preview area."""
        logger.info("Taking region screenshot")

        # Use the screenshot service
        screenshot_service = ScreenshotService()

        # Set the root window to avoid capturing the app itself
        root = self.parent.winfo_toplevel()
        screenshot_service.set_root_window(root)

        # Take region screenshot
        screenshot_service.take_region_screenshot(save_to_disk=False)

        # If a region was selected and captured successfully
        if screenshot_service.image:
            self.set_image(screenshot_service.image)
            # Also update the main layout's reference to the screenshot
            self.main_layout.set_screenshot(screenshot_service.image)
        else:
            logger.info("Region selection was cancelled or failed")

    def set_image(self, image):
        """Set and display an image in the preview panel.

        Args:
            image: PIL Image object
        """
        if image:
            self.original_image = image.copy()
            self.resize_image()

    def resize_image(self):
        """Resize the original image to fit the current container and display it."""
        if self.original_image is None:
            return

        self.parent.update_idletasks()

        # Calculate maximum dimensions for the image to fit in the container
        container_width = self.image_container.winfo_width() - 20
        container_height = self.image_container.winfo_height() - 20

        logger.info(f"Container dimensions: {container_width}x{container_height}")

        # If container dimensions are not available yet, use reasonable defaults
        if container_width < 100:
            container_width = 450
        if container_height < 100:
            container_height = 280

        # Calculate scale factor to maintain aspect ratio
        img_aspect = self.original_image.width / self.original_image.height
        container_aspect = container_width / container_height

        # Determine dimensions based on aspect ratios
        if img_aspect >= container_aspect:
            # Scale to container width
            new_width = container_width
            new_height = int(new_width / img_aspect)
        else:  # Image is taller than container
            # Scale to container height
            new_height = container_height
            new_width = int(new_height * img_aspect)

        logger.info(f"Resizing image to: {new_width}x{new_height}")

        # Resize the image with the calculated dimensions
        resized_image = self.original_image.resize((new_width, new_height), 1)

        # Convert to PhotoImage and display
        self.screenshot_image = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.screenshot_image)

    def refresh_preview(self):
        """Clear the current preview image."""
        logger.info("Refreshing preview content")
        self.image_label.config(image="")
        self.original_image = None
        # Also clear the main layout's reference
        self.main_layout.original_screenshot = None

    def analyze_screenshot(self):
        """Trigger analysis of the current screenshot."""
        logger.info("Triggering screenshot analysis")
        self.main_layout.analyze_screenshot()
