import tkinter as tk
from tkinter import ttk, messagebox
from src.settings.config_manager import ConfigManager
from src.settings.settings import Settings


class SettingsDialog(tk.Toplevel):
    """Dialog for configuring application settings"""

    def __init__(self, parent, on_settings_changed=None):
        super().__init__(parent)
        self.parent = parent
        self.on_settings_changed = on_settings_changed

        # Initialize settings
        self.config_manager = ConfigManager()
        self.settings = Settings()

        # Configure window
        self.title("Settings")
        self.geometry("550x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Create UI elements
        self.create_widgets()
        self.center_window()

        # Load current settings
        self.load_current_settings()

    def create_widgets(self):
        """Create all widgets for the settings dialog"""
        # Main frame with padding
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create notebook for tabbed interface
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Appearance tab
        appearance_frame = ttk.Frame(notebook, padding=10)
        notebook.add(appearance_frame, text="Appearance")

        # Theme selection
        ttk.Label(appearance_frame, text="Theme:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.theme_combobox = ttk.Combobox(
            appearance_frame,
            values=self.settings.AVAILABLE_THEMES,
            state="readonly",
            width=30,
        )
        self.theme_combobox.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

        # API tab
        api_frame = ttk.Frame(notebook, padding=10)
        notebook.add(api_frame, text="API Settings")

        # API URL
        ttk.Label(api_frame, text="API URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.api_url_entry = ttk.Entry(api_frame, width=40)
        self.api_url_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

        # API Key
        ttk.Label(api_frame, text="API Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.api_key_entry = ttk.Entry(api_frame, width=40, show="●")
        self.api_key_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)

        # Show/Hide API Key button
        self.show_key_var = tk.BooleanVar(value=False)
        self.show_key_check = ttk.Checkbutton(
            api_frame,
            text="Show API Key",
            variable=self.show_key_var,
            command=self.toggle_api_key_visibility,
        )
        self.show_key_check.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)

        # User tab
        user_frame = ttk.Frame(notebook, padding=10)
        notebook.add(user_frame, text="User Information")

        # Username
        ttk.Label(user_frame, text="Username:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.username_entry = ttk.Entry(user_frame, width=30)
        self.username_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

        # User ID
        ttk.Label(user_frame, text="User ID:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.user_id_entry = ttk.Entry(user_frame, width=30)
        self.user_id_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)

        # Buttons frame at the bottom
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        # Save button
        save_button = ttk.Button(button_frame, text="Save", command=self.save_settings)
        save_button.pack(side=tk.RIGHT, padx=5)

        # Cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)

    def load_current_settings(self):
        """Load current settings into the UI"""
        # Set theme
        self.theme_combobox.set(self.config_manager.current_theme)

        # Set API information
        self.api_url_entry.delete(0, tk.END)
        self.api_url_entry.insert(0, self.config_manager.api_url)

        self.api_key_entry.delete(0, tk.END)
        self.api_key_entry.insert(0, self.config_manager.api_key)

        # Set user information
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, self.config_manager.username)

        self.user_id_entry.delete(0, tk.END)
        self.user_id_entry.insert(0, self.config_manager.user_id)

    def save_settings(self):
        """Save settings and close the dialog"""
        # Get values from UI
        theme = self.theme_combobox.get()
        api_url = self.api_url_entry.get().strip()
        api_key = self.api_key_entry.get().strip()
        username = self.username_entry.get().strip()
        user_id = self.user_id_entry.get().strip()

        # Validate
        if not api_url:
            messagebox.showerror("Error", "API URL cannot be empty")
            return

        if not api_key:
            messagebox.showerror("Error", "API Key cannot be empty")
            return

        # Save settings
        old_theme = self.config_manager.current_theme

        self.config_manager.set_theme(theme)
        self.config_manager.set_api_url(api_url)
        self.config_manager.set_api_key(api_key)
        self.config_manager.set_user_info(username, user_id)

        # Notify parent if theme changed
        if old_theme != theme and self.on_settings_changed:
            self.on_settings_changed(theme)

        messagebox.showinfo("Success", "Settings saved successfully")
        self.destroy()

    def toggle_api_key_visibility(self):
        """Toggle showing the API key as plain text or hidden"""
        if self.show_key_var.get():
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="●")

    def center_window(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() / 2) - (width / 2)
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() / 2) - (height / 2)
        self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
