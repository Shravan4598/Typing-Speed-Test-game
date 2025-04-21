import time
import random
import tkinter as tk
from tkinter import font

def get_text():
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Python programming is fun and engaging.",
        "Typing tests improve your speed and accuracy.",
        "Practice makes perfect when it comes to typing."
    ]
    return random.choice(texts)

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.configure(bg='#F0F0F0')

        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.text_font = font.Font(family="Courier New", size=16)
        self.result_font = font.Font(family="Arial", size=14, weight="bold")

        # Initialize test variables
        self.start_time = None
        self.running = False
        self.original_text = ""

        # Build the UI
        self.setup_ui()
        self.new_test()

    def setup_ui(self):
        # Header Label
        self.header = tk.Label(
            self.root,
            text="Typing Speed Test",
            font=self.title_font,
            bg='#F0F0F0',
            fg='#2C3E50'
        )
        self.header.pack(pady=20)

        # Frame for sample text
        self.sample_frame = tk.Frame(self.root, bg='white', padx=20, pady=20)
        self.sample_frame.pack(pady=10, fill=tk.X, padx=40)

        self.sample_label = tk.Label(
            self.sample_frame,
            text="",
            font=self.text_font,
            bg='white',
            fg='#34495E',
            wraplength=700,
            justify=tk.LEFT
        )
        self.sample_label.pack()

        # Text widget for user input
        self.input_text = tk.Text(
            self.root,
            font=self.text_font,
            height=5,
            width=60,
            padx=10,
            pady=10,
            wrap=tk.WORD,
            bg='#FFFFFF'
        )
        self.input_text.pack(pady=20)
        self.input_text.bind("<Key>", self.start_timer)  # Fixed binding

        # Frame for control buttons
        self.btn_frame = tk.Frame(self.root, bg='#F0F0F0')
        self.btn_frame.pack(pady=10)

        self.restart_btn = tk.Button(
            self.btn_frame,
            text="New Test",
            font=self.text_font,
            command=self.new_test,
            bg='#3498DB',
            fg='white'
        )
        self.restart_btn.pack(side=tk.LEFT, padx=10)

        # Results Label
        self.result_label = tk.Label(
            self.root,
            text="Click the text area below to start typing!",
            font=self.result_font,
            bg='#F0F0F0',
            fg='#27AE60'
        )
        self.result_label.pack(pady=20)

    def new_test(self):
        # Reset test and set new text
        self.original_text = get_text()
        self.sample_label.config(text=self.original_text)
        self.input_text.delete('1.0', tk.END)
        self.result_label.config(text="Click the text area below to start typing!", fg='#27AE60')
        self.running = False
        self.start_time = None
        self.input_text.config(bg='#FFFFFF')
        self.input_text.config(state=tk.NORMAL)
        self.input_text.focus_set()

    def start_timer(self, event):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.input_text.config(bg='#F9EBEA')
            self.result_label.config(text="Typing...", fg='#E74C3C')
            self.root.after(100, self.update_timer)
        # Check if text is complete on every key press
        self.check_completion()

    def update_timer(self):
        if self.running:
            elapsed = time.time() - self.start_time
            wpm = self.calculate_wpm(elapsed)
            self.result_label.config(text=f"Elapsed Time: {elapsed:.1f}s | WPM: {wpm}")
            self.root.after(1000, self.update_timer)

    def calculate_wpm(self, elapsed):
        typed_text = self.input_text.get('1.0', 'end-1c')
        typed_words = len(typed_text.split())
        return int(typed_words / (elapsed / 60)) if elapsed > 0 else 0

    def check_completion(self):
        user_input = self.input_text.get('1.0', 'end-1c')
        if user_input == self.original_text:
            self.show_final_results()

    def show_final_results(self):
        # Stop timer and disable further input
        self.running = False
        self.input_text.config(state=tk.DISABLED)
        elapsed_time = time.time() - self.start_time
        user_input = self.input_text.get('1.0', 'end-1c')

        # Calculate character accuracy
        min_length = min(len(self.original_text), len(user_input))
        correct = sum(1 if o == t else 0 for o, t in zip(self.original_text[:min_length], user_input[:min_length]))
        accuracy = (correct / len(self.original_text)) * 100 if len(self.original_text) > 0 else 0

        # Calculate WPM
        wpm = self.calculate_wpm(elapsed_time)

        # Display final results
        result_text = (
            f"Time: {elapsed_time:.2f}s | WPM: {wpm} | Accuracy: {accuracy:.1f}%\n"
            "Press 'New Test' to try again!"
        )
        if user_input == self.original_text:
            result_text = "Perfect! " + result_text

        self.result_label.config(text=result_text, fg='#27AE60')
        self.input_text.config(bg='#EAFAF1')

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()
