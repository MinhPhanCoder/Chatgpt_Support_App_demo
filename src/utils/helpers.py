import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, YES


def show_message(title, message):
    root = tk.Tk()
    # Hide the root window
    root.withdraw()
    messagebox.showinfo(title, message)


def get_available_themes():
    return ttk.Style().theme_names()


def show_app_centered_message(
    parent, title, message, button_text="OK", button_style="primary"
):
    """
    Shows a message dialog centered within the application window.

    Args:
        parent: The parent window to center the dialog on
        title: Dialog title in English
        message: Message content in English
        button_text: Text for the OK button (defaults to "OK")
        button_style: ttkbootstrap style for the button (defaults to "primary")
    """
    # Get the root window if a child widget is passed
    if not isinstance(parent, tk.Tk) and not isinstance(parent, ttk.Toplevel):
        root = parent.winfo_toplevel()
    else:
        root = parent

    # Create dialog
    dialog = ttk.Toplevel(root)
    dialog.title(title)
    dialog.transient(root)  # Make dialog transient to main window
    dialog.grab_set()  # Make dialog modal
    dialog.resizable(False, False)

    # Set size and position relative to main window
    dialog_width = 300
    dialog_height = 150

    # Calculate position to center dialog relative to main window
    root.update_idletasks()  # Update to get accurate dimensions
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    root_x = root.winfo_rootx()
    root_y = root.winfo_rooty()

    # Center dialog relative to main window
    position_x = root_x + (root_width - dialog_width) // 2
    position_y = root_y + (root_height - dialog_height) // 2

    dialog.geometry(f"{dialog_width}x{dialog_height}+{position_x}+{position_y}")

    # Create content frame
    frame = ttk.Frame(dialog, padding=20)
    frame.pack(fill=BOTH, expand=YES)

    # Add message label
    ttk.Label(frame, text=message, font=("Helvetica", 12), wraplength=250).pack(pady=10)

    # Add OK button
    ttk.Button(
        frame, text=button_text, style=button_style, command=dialog.destroy
    ).pack(pady=10)

    # Return the dialog for further customization if needed
    return dialog
