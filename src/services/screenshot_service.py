import os
import tkinter as tk
from PIL import ImageGrab
from datetime import datetime
from src.utils.logger import get_logger
import time
import base64
from io import BytesIO
import threading
import keyboard

logger = get_logger()


class ScreenshotService:
    """Service class to handle screenshot functionality"""

    def __init__(self):
        app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.screenshots_dir = os.path.join(app_root, "screenshots")
        os.makedirs(self.screenshots_dir, exist_ok=True)

        self.image = None
        self.root = None
        self.exit_selection = False

    def set_root_window(self, root):
        """Set the root window reference for hiding during screenshots

        Args:
            root: The root Tk window
        """
        self.root = root

    def take_screenshot(self, save_to_disk=False):
        """Capture screenshot of entire screen,
        temporarily hiding the application window to avoid self-capture

        Args:
            save_to_disk (bool): Whether to save the screenshot to disk. Defaults to False.

        Returns:
            str: Path to the saved screenshot if saved, None otherwise
        """
        # Get reference to root window if not already set
        if not self.root:
            for widget in tk._default_root.winfo_children():
                if isinstance(widget, tk.Toplevel) or widget.winfo_toplevel() == widget:
                    self.root = widget
                    break
            # If still not found, use the default root
            if not self.root:
                self.root = tk._default_root

        # Store the current window state
        was_visible = False
        if self.root:
            was_visible = self.root.winfo_viewable()
            if was_visible:
                # Hide the window
                self.root.withdraw()
                # Allow time for window to be removed from screen
                time.sleep(0.2)

        try:
            # Take screenshot of the entire screen
            self.image = ImageGrab.grab()
        finally:
            # Restore window visibility if it was visible before
            if self.root and was_visible:
                self.root.deiconify()

        if save_to_disk:
            return self._save_image("screenshot")
        return None

    def monitor_escape_key(self, overlay):
        """Monitor for Escape key press in a separate thread"""
        while not self.exit_selection:
            if keyboard.is_pressed("esc"):
                logger.info("ESC key detected in monitoring thread")
                # Schedule destroy on main thread
                overlay.after(0, overlay.destroy)
                break
            time.sleep(0.1)

    def take_region_screenshot(self, save_to_disk=False):
        """Capture screenshot of a user-defined region

        Args:
            save_to_disk (bool): Whether to save the screenshot to disk. Defaults to False.

        Returns:
            str: Path to the saved screenshot if saved, None otherwise
        """
        # Reset exit flag
        self.exit_selection = False

        # Hide main window temporarily
        was_visible = False
        if self.root:
            was_visible = self.root.winfo_viewable()
            if was_visible:
                self.root.withdraw()
                # Small delay to ensure window is hidden
                time.sleep(0.2)

        try:
            # Create an overlay window that covers the entire screen
            overlay = tk.Toplevel()
            overlay.attributes("-alpha", 0.3)  # Semi-transparent
            overlay.attributes("-fullscreen", True)
            overlay.attributes("-topmost", True)

            # Configure overlay appearance
            overlay.configure(bg="gray")

            # Create a canvas for drawing the selection rectangle
            canvas = tk.Canvas(overlay, bg="gray", highlightthickness=0)
            canvas.pack(fill=tk.BOTH, expand=True)

            # Variables to store selection coordinates
            selection_coords = {"start_x": 0, "start_y": 0, "end_x": 0, "end_y": 0}
            selection_rect = None
            selection_made = [False]  # Using a list to make it mutable in closures

            # Create status label with clear instructions
            instructions = tk.Label(
                overlay,
                text="Click and drag to select a region. Press ESC to cancel.",
                bg="black",
                fg="white",
                font=("Arial", 12),
            )
            instructions.place(x=10, y=10)

            # Create a large, prominent cancel button
            cancel_btn = tk.Button(
                overlay,
                text="CANCEL (ESC)",
                command=overlay.destroy,
                bg="red",
                fg="white",
                font=("Arial", 12, "bold"),
                padx=10,
                pady=5,
                relief=tk.RAISED,
                bd=3,
            )
            cancel_btn.place(x=10, y=50)

            # Event handlers for selection
            def on_mouse_down(event):
                selection_coords["start_x"] = event.x
                selection_coords["start_y"] = event.y
                nonlocal selection_rect
                if selection_rect:
                    canvas.delete(selection_rect)
                selection_rect = canvas.create_rectangle(
                    event.x, event.y, event.x, event.y, outline="red", width=2
                )

            def on_mouse_move(event):
                if selection_rect:
                    selection_coords["end_x"] = event.x
                    selection_coords["end_y"] = event.y
                    canvas.coords(
                        selection_rect,
                        selection_coords["start_x"],
                        selection_coords["start_y"],
                        event.x,
                        event.y,
                    )

            def on_mouse_up(event):
                selection_coords["end_x"] = event.x
                selection_coords["end_y"] = event.y
                # Only consider it a valid selection if drag distance is significant
                if (
                    abs(selection_coords["end_x"] - selection_coords["start_x"]) > 10
                    and abs(selection_coords["end_y"] - selection_coords["start_y"])
                    > 10
                ):
                    selection_made[0] = True
                    overlay.destroy()

            # Register the event handlers
            canvas.bind("<ButtonPress-1>", on_mouse_down)
            canvas.bind("<B1-Motion>", on_mouse_move)
            canvas.bind("<ButtonRelease-1>", on_mouse_up)

            # Start a background thread to monitor for ESC key
            monitor_thread = threading.Thread(
                target=self.monitor_escape_key, args=(overlay,), daemon=True
            )
            monitor_thread.start()

            # Wait for overlay to be destroyed (selection complete or cancelled)
            overlay.wait_window()

            # Signal thread to exit
            self.exit_selection = True

            # Check if a valid selection was made
            if not selection_made[0]:
                logger.info("Region selection cancelled or invalid")
                return None

            # Normalize coordinates (start < end)
            left = min(selection_coords["start_x"], selection_coords["end_x"])
            top = min(selection_coords["start_y"], selection_coords["end_y"])
            right = max(selection_coords["start_x"], selection_coords["end_x"])
            bottom = max(selection_coords["start_y"], selection_coords["end_y"])

            # Take the screenshot of the selected region
            self.image = ImageGrab.grab(bbox=(left, top, right, bottom))
            logger.info(f"Captured region: ({left}, {top}, {right}, {bottom})")

            if save_to_disk:
                return self._save_image("region_screenshot")
            return None

        finally:
            # Restore main window visibility if needed
            if self.root and was_visible:
                self.root.deiconify()

    def _save_image(self, prefix):
        """Save the current image to disk with a timestamp

        Args:
            prefix: Prefix for the filename

        Returns:
            str: Path to the saved image
        """
        if not self.image:
            return None

        # Generate a unique filename based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(
            self.screenshots_dir, f"{prefix}_{timestamp}.png"
        )
        self.image.save(screenshot_path)
        logger.info(f"Image saved to: {screenshot_path}")
        return screenshot_path

    def get_image_as_base64(self):
        """
        Convert the current image to base64 encoded string
        """
        # Create a BytesIO buffer to save the image
        buffer = BytesIO()
        self.image.save(buffer, format="PNG")

        img_bytes = buffer.getvalue()
        base64_string = base64.b64encode(img_bytes).decode("utf-8")

        # Return with data URL prefix
        return f"data:image/png;base64,{base64_string}"
