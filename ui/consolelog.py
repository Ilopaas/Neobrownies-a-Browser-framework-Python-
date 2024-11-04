import tkinter as tk
from tkinter import scrolledtext

class ConsoleLog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Console Log")
        self.geometry("600x400")

        # Create a ScrolledText widget
        self.text_area = scrolledtext.ScrolledText(self, state="normal", wrap="word")
        self.text_area.pack(fill='both', expand=True, padx=10, pady=10)
        self.text_area.configure(state="disabled")  # Start as read-only

    def log(self, message):
        """Log a message to the console."""
        self.text_area.configure(state="normal")  # Enable editing to insert text
        self.text_area.insert("end", message + "\n")  # Add message to the text area
        self.text_area.configure(state="disabled")  # Disable editing to make it read-only
        self.text_area.see("end")  # Scroll to the end of the text area
