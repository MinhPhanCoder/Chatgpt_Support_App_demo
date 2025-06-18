from tkinter import PhotoImage
import ttkbootstrap as ttk


def load_bootstrap_image(image_path):
    return PhotoImage(file=image_path)


def set_theme(root, theme_name):
    """Change the theme of an existing ttkbootstrap window

    Args:
        root: The ttkbootstrap window/root
        theme_name: Name of the theme to apply
    """
    style = ttk.Style()
    style.theme_use(theme_name)


def create_widget(parent, widget_type, style=None, **kwargs):
    """Create a ttkbootstrap widget with the specified style

    Args:
        parent: Parent container
        widget_type: String representing the widget type (e.g., "Button", "Label")
        style: String representing the style (e.g., "primary", "success-outline")
        **kwargs: Additional keyword arguments for the widget

    Returns:
        The created widget
    """
    widget_map = {
        "Button": ttk.Button,
        "Label": ttk.Label,
        "Entry": ttk.Entry,
        "Frame": ttk.Frame,
        "Notebook": ttk.Notebook,
        "Progressbar": ttk.Progressbar,
        "Combobox": ttk.Combobox,
        "Treeview": ttk.Treeview,
        "Scrollbar": ttk.Scrollbar,
        "Checkbutton": ttk.Checkbutton,
        "Radiobutton": ttk.Radiobutton,
        "Scale": ttk.Scale,
        "Separator": ttk.Separator,
        "Spinbox": ttk.Spinbox,
    }

    if widget_type not in widget_map:
        raise ValueError(f"Widget type '{widget_type}' not supported")

    if style:
        if "style" not in kwargs:
            if widget_type == "Progressbar":
                kwargs["style"] = f"{style}.Horizontal.TProgressbar"
            else:
                kwargs["style"] = f"{style}.T{widget_type}"

    return widget_map[widget_type](parent, **kwargs)
