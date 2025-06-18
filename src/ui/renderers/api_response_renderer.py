"""
API Response Renderer for formatting and displaying API responses.
"""

from src.utils.logger import get_logger

logger = get_logger()


class APIResponseRenderer:
    """Renderer for formatting and displaying API responses in a text widget."""

    def __init__(self):
        """Initialize the API response renderer."""
        pass

    def render(self, text_widget, api_response):
        """
        Render the formatted API response in the provided text widget.

        Args:
            text_widget: The tkinter Text widget to render into
            api_response: The API response dictionary
        """
        logger.info("Rendering API response")

        # Extract data from the API response
        data = api_response.get("data")
        if not data or not isinstance(data, list) or len(data) == 0:
            self._set_text(text_widget, "Invalid API response format")
            return

        # Prepare the text widget
        self._prepare_text_widget(text_widget)

        # Render the header
        self._render_header(text_widget)

        # Process each question in the data
        for idx, question_data in enumerate(data):
            # Render the question and its answers
            self._render_question(text_widget, question_data, idx)

        # Finish up
        text_widget.see("1.0")  # Scroll to the beginning
        text_widget.config(state="disabled")  # Disable editing

    def _prepare_text_widget(self, text_widget):
        """Set up the text widget with the necessary styles.

        Args:
            text_widget: The tkinter Text widget to configure
        """
        # Clean up the text area and prepare it for new content
        text_widget.config(state="normal")
        text_widget.delete("1.0", "end")

        # Set the background color to white for better visibility
        text_widget.configure(background="#FFFFFF")

        text_widget.tag_configure(
            "title",
            font=("Helvetica", 12, "bold"),
            foreground="#FFFFFF",
            background="#0066cc",
        )

        text_widget.tag_configure(
            "question_number",
            font=("Helvetica", 11, "bold"),
            foreground="#FFFFFF",
            background="#333333",
        )

        text_widget.tag_configure(
            "question_text",
            font=("Helvetica", 10),
            foreground="#000000",
            background="#F5F5F5",
        )

        text_widget.tag_configure(
            "section_header",
            font=("Helvetica", 10, "bold"),
            foreground="#FFFFFF",
            background="#666666",
        )

        text_widget.tag_configure(
            "correct_answer",
            font=("Helvetica", 10, "bold"),
            foreground="#006400",
            background="#CCFFCC",
        )

        text_widget.tag_configure(
            "incorrect_answer",
            font=("Helvetica", 10),
            foreground="#000000",
            background="#F8F8F8",
        )

        text_widget.tag_configure(
            "explanation_text",
            font=("Helvetica", 10),
            foreground="#000000",
            background="#FFF8DC",
        )

        text_widget.tag_configure(
            "confidence",
            font=("Helvetica", 10, "bold"),
            foreground="#FFFFFF",
            background="#0066cc",
        )

        text_widget.tag_configure(
            "separator", font=("Helvetica", 1), foreground="#000000"
        )

        text_widget.tag_configure(
            "multiple_correct",
            font=("Helvetica", 10, "bold"),
            foreground="#FFFFFF",
            background="#FF5722",
        )

    def _render_header(self, text_widget):
        """Render the header section of the response.

        Args:
            text_widget: The tkinter Text widget to render into
        """
        text_widget.insert("end", "EXAM QUESTION ANALYSIS\n", "title")

    def _render_question(self, text_widget, question_data, idx):
        """Render a single question with its answers and explanation.

        Args:
            text_widget: The tkinter Text widget to render into
            question_data: Dictionary containing the question data
            idx: The index of the question in the list
        """
        # Extract question details
        question_number = question_data.get("number", f"Q{idx+1}")
        question_text = question_data.get("question_raw", "N/A")
        answer_raw = question_data.get("answer_raw", [])
        correct_answers = question_data.get("answer", [])
        reason = question_data.get("reason", "N/A")
        question_type = question_data.get("type_question", "N/A")
        accuracy = question_data.get("accuracy", "N/A")

        text_widget.insert("end", f"Question {question_number}:\n", "question_number")
        text_widget.insert("end", f"{question_text}\n\n", "question_text")

        # Render answer choices
        self._render_answer_choices(
            text_widget, question_type, correct_answers, answer_raw
        )

        # Render explanation
        text_widget.insert("end", "EXPLANATION:\n", "section_header")
        text_widget.insert("end", f"{reason}\n\n", "explanation_text")

        # Render confidence meter
        self._render_confidence_meter(text_widget, accuracy, idx)

    def _render_answer_choices(
        self, text_widget, question_type, correct_answers, answer_raw
    ):
        """Render the answer choices for a question.

        Args:
            text_widget: The tkinter Text widget to render into
            question_type: question_type
            correct_answers: List or string of correct answer identifiers
            answer_raw: List of answer choice texts
            question_text: The full question text
        """
        # Render choices header
        if question_type == "single-choice":
            text_widget.insert("end", "CHOICES (Single Answer):\n", "section_header")
        else:
            text_widget.insert("end", "CHOICES (Multiple Answers):\n", "section_header")

        # Render each choice
        for i, choice in enumerate(answer_raw):
            choice_id = None
            choice_text = choice

            if choice.strip() and choice.strip()[0].isdigit() and ". " in choice:
                parts = choice.split(". ", 1)
                if len(parts) == 2:
                    choice_id = parts[0].strip()
                    choice_text = parts[1].strip()

            if not choice_id:
                choice_id = chr(65 + i) if i < 26 else str(i + 1)

            # Check if the answer is correct or not
            is_correct = correct_answers[i]
            prefix = "☑ " if is_correct else "☐ "
            tag = "correct_answer" if is_correct else "incorrect_answer"

            # Insert the formatted choice
            if choice_id in choice_text:
                text_widget.insert("end", f"{prefix}{choice_text}\n", tag)
            else:
                text_widget.insert("end", f"{prefix}{choice_id}. {choice_text}\n", tag)

    def _render_confidence_meter(self, text_widget, accuracy, idx):
        """Render the confidence meter for a question.

        Args:
            text_widget: The tkinter Text widget to render into
            accuracy: The accuracy value (string or numeric)
            idx: The index of the question
        """
        text_widget.insert("end", "CONFIDENCE: ", "section_header")

        if isinstance(accuracy, str) and "%" in accuracy:
            try:
                accuracy_value = int(accuracy.strip("%"))

                # Configure colors based on confidence level
                if accuracy_value >= 80:
                    # High confidence - green color
                    meter_color = "#006400"
                    bg_color = "#CCFFCC"
                elif accuracy_value >= 50:
                    # Medium confidence - orange color
                    meter_color = "#FF8C00"
                    bg_color = "#FFE4B5"
                else:
                    # Low confidence - red color
                    meter_color = "#B22222"
                    bg_color = "#FFCCCC"

                # Create image icon for the meter
                meter = "█" * (accuracy_value // 20) + "░" * (5 - accuracy_value // 20)

                # Display confidence value
                text_widget.insert("end", f"{accuracy} ", "confidence")

                # Configure tag for meter with custom text and background colors
                text_widget.tag_configure(
                    f"meter_{idx}",
                    foreground=meter_color,
                    background=bg_color,
                    font=("Helvetica", 10, "bold"),
                )

                # Display meter with custom colors
                text_widget.insert("end", f"{meter}\n", f"meter_{idx}")
            except ValueError:
                text_widget.insert("end", f"{accuracy}\n", "confidence")
        else:
            text_widget.insert("end", f"{accuracy}\n", "confidence")

    def _set_text(self, text_widget, message):
        """Set a simple message in the text widget.

        Args:
            text_widget: The tkinter Text widget to update
            message: The message to display
        """
        text_widget.config(state="normal")
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", message)
        text_widget.config(state="disabled")
