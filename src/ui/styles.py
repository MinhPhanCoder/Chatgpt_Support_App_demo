class Styles:
    BUTTON_BG = "#007bff"  # Bootstrap primary color
    BUTTON_FG = "#ffffff"  # White text color
    BUTTON_HOVER_BG = "#0056b3"  # Darker shade for hover effect
    BUTTON_FONT = ("Helvetica", 12, "bold")

    LABEL_FONT = ("Helvetica", 12)
    LABEL_FG = "#343a40"  # Bootstrap text color

    ENTRY_BG = "#ffffff"  # White background for entry fields
    ENTRY_FG = "#495057"  # Darker text color for entry fields
    ENTRY_BORDER = "1px solid #ced4da"  # Bootstrap border color

    @staticmethod
    def apply_button_style(button):
        button.config(bg=Styles.BUTTON_BG, fg=Styles.BUTTON_FG, font=Styles.BUTTON_FONT)
        button.bind("<Enter>", lambda e: button.config(bg=Styles.BUTTON_HOVER_BG))
        button.bind("<Leave>", lambda e: button.config(bg=Styles.BUTTON_BG))

    @staticmethod
    def apply_label_style(label):
        label.config(fg=Styles.LABEL_FG, font=Styles.LABEL_FONT)

    @staticmethod
    def apply_entry_style(entry):
        entry.config(
            bg=Styles.ENTRY_BG, fg=Styles.ENTRY_FG, borderwidth=1, relief="solid"
        )  # Note: Tkinter does not support CSS styles directly
        entry.config(highlightbackground=Styles.ENTRY_BORDER)
