"""
Number Guessing Game - Kivy Mobile App
----------------------------------------
A simple, mobile-friendly number guessing game built with Kivy.

How it works:
- The app picks a random secret number between 1 and 100.
- The user types a guess into a TextInput and taps "Check Guess".
- The app tells the user if their guess is Too High, Too Low, or Correct.
- The number of attempts is tracked and displayed.
- A "New Game" button resets everything with a fresh random number.

To run:
    pip install kivy
    python main.py
"""

import random

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.core.window import Window


# ---------------------------------------------------------------------------
# Main game widget
# ---------------------------------------------------------------------------
class NumberGuessGame(BoxLayout):
    """
    Root widget for the app.

    A BoxLayout (vertical orientation) is used to stack the UI elements
    neatly from top to bottom, which works well on mobile screens.
    """

    def __init__(self, **kwargs):
        # Configure the BoxLayout itself (vertical stack, padding, spacing)
        super().__init__(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(16),
            **kwargs
        )

        # ------------------------------------------------------------------
        # Game state variables
        # ------------------------------------------------------------------
        self.secret_number = random.randint(1, 100)  # The number to guess
        self.attempts = 0                              # Attempt counter

        # ------------------------------------------------------------------
        # Title label
        # ------------------------------------------------------------------
        self.title_label = Label(
            text="Number Guessing Game",
            font_size=dp(28),
            bold=True,
            size_hint=(1, 0.15),
        )
        self.add_widget(self.title_label)

        # ------------------------------------------------------------------
        # Instructions label
        # ------------------------------------------------------------------
        self.instructions_label = Label(
            text="Guess a number between 1 and 100",
            font_size=dp(18),
            size_hint=(1, 0.1),
        )
        self.add_widget(self.instructions_label)

        # ------------------------------------------------------------------
        # Text input for the user's guess
        # ------------------------------------------------------------------
        self.guess_input = TextInput(
            hint_text="Enter your guess here",
            multiline=False,           # Single-line input, like a search box
            input_filter="int",        # Only allows integer characters to be typed
            font_size=dp(20),
            size_hint=(1, 0.12),
            halign="center",
            padding=[dp(10), dp(15), dp(10), dp(15)],
        )
        self.add_widget(self.guess_input)

        # ------------------------------------------------------------------
        # "Check Guess" button
        # ------------------------------------------------------------------
        self.check_button = Button(
            text="Check Guess",
            font_size=dp(20),
            size_hint=(1, 0.14),
            background_color=(0.2, 0.6, 0.86, 1),  # Friendly blue
        )
        # Bind the button press to our check_guess method
        self.check_button.bind(on_press=self.check_guess)
        self.add_widget(self.check_button)

        # ------------------------------------------------------------------
        # Result label - shows "Too High", "Too Low", success, or errors
        # ------------------------------------------------------------------
        self.result_label = Label(
            text="Make your first guess!",
            font_size=dp(22),
            bold=True,
            size_hint=(1, 0.2),
            halign="center",
            valign="middle",
        )
        # Allow text to wrap nicely within the label's width
        self.result_label.bind(size=self._update_text_size)
        self.add_widget(self.result_label)

        # ------------------------------------------------------------------
        # Attempts counter label
        # ------------------------------------------------------------------
        self.attempts_label = Label(
            text="Attempts: 0",
            font_size=dp(18),
            size_hint=(1, 0.1),
        )
        self.add_widget(self.attempts_label)

        # ------------------------------------------------------------------
        # "New Game" button
        # ------------------------------------------------------------------
        self.new_game_button = Button(
            text="New Game",
            font_size=dp(20),
            size_hint=(1, 0.14),
            background_color=(0.18, 0.8, 0.44, 1),  # Friendly green
        )
        self.new_game_button.bind(on_press=self.new_game)
        self.add_widget(self.new_game_button)

    # ----------------------------------------------------------------------
    # Helper to keep result_label text wrapping inside its own width
    # ----------------------------------------------------------------------
    def _update_text_size(self, instance, value):
        instance.text_size = (instance.width, None)

    # ----------------------------------------------------------------------
    # Core game logic: check the user's guess against the secret number
    # ----------------------------------------------------------------------
    def check_guess(self, instance):
        raw_text = self.guess_input.text.strip()

        # --- Handle empty input ---
        if raw_text == "":
            self.result_label.text = "Please enter a number before checking."
            self.result_label.color = (1, 0.6, 0, 1)  # Orange warning color
            return

        # --- Handle non-numeric / invalid input gracefully ---
        # (input_filter="int" already blocks most bad characters, but we
        # still validate here in case of paste actions or edge cases.)
        try:
            guess = int(raw_text)
        except ValueError:
            self.result_label.text = "Invalid input. Please enter a whole number."
            self.result_label.color = (1, 0.2, 0.2, 1)  # Red error color
            return

        # --- Handle out-of-range guesses ---
        if guess < 1 or guess > 100:
            self.result_label.text = "Please enter a number between 1 and 100."
            self.result_label.color = (1, 0.6, 0, 1)
            return

        # --- Valid guess: increment attempts and compare ---
        self.attempts += 1
        self.attempts_label.text = f"Attempts: {self.attempts}"

        if guess > self.secret_number:
            self.result_label.text = "Too High! Try again."
            self.result_label.color = (1, 0.4, 0.2, 1)  # Reddish-orange
        elif guess < self.secret_number:
            self.result_label.text = "Too Low! Try again."
            self.result_label.color = (0.2, 0.5, 1, 1)  # Blue
        else:
            self.result_label.text = (
                f"Congratulations! You guessed correctly in "
                f"{self.attempts} attempt(s)."
            )
            self.result_label.color = (0.18, 0.8, 0.44, 1)  # Green success

        # Clear the input field so the user can type their next guess easily
        self.guess_input.text = ""

    # ----------------------------------------------------------------------
    # Reset the game: new secret number, reset attempts, clear UI
    # ----------------------------------------------------------------------
    def new_game(self, instance):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.attempts_label.text = "Attempts: 0"
        self.result_label.text = "New game started! Make your first guess."
        self.result_label.color = (1, 1, 1, 1)  # Reset to default white
        self.guess_input.text = ""


# ---------------------------------------------------------------------------
# Main App class
# ---------------------------------------------------------------------------
class NumberGuessApp(App):
    """The Kivy App that wraps our NumberGuessGame widget."""

    def build(self):
        self.title = "Number Guessing Game"
        # Set a reasonable default window size for desktop testing in VS Code.
        # (This has no effect on actual mobile devices, where the app fills
        # the screen automatically.)
        Window.size = (400, 650)
        return NumberGuessGame()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    NumberGuessApp().run()
