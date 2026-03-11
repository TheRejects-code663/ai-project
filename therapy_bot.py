import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
import time
import random

# --- 1. SETUP THE AI ---
# REPLACE WITH YOUR NEW KEY (Keep it private!)
API_KEY = "AIzaSyAPVROYRchF7q4DKhEezajqjaQZWpFT0kM"
# Try-Except block to handle connection errors immediately
try:
    genai.configure(api_key=API_KEY)
    
    # Using gemini-2.5-flash-lite: Best for Free Tier in 2026
    # We define the "Therapist" persona directly in the system_instruction
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash-lite',
        system_instruction="You are a kind, professional therapy assistant. "
                           "Ask helpful questions and use short, supportive language. "
                           "Always include a disclaimer that you are an AI."
    )
    
    chat_session = model.start_chat(history=[])
except Exception as e:
    print(f"Initial Setup Error: {e}")

class TherapyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mindful AI Companion")
        self.root.geometry("500x650")
        self.root.configure(bg="#F8F9FA")

        # UI Header
        tk.Label(root, text="AI Support Session", font=("Helvetica", 16, "bold"), bg="#F8F9FA", pady=15).pack()

        # Chat Area
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=55, height=22, font=("Segoe UI", 10))
        self.chat_area.pack(padx=20, pady=5)
        self.chat_area.config(state='disabled', bg="white", fg="#333")

        # Input Section
        self.input_frame = tk.Frame(root, bg="#F8F9FA")
        self.input_frame.pack(pady=20, fill="x", padx=20)

        self.user_input = tk.Entry(self.input_frame, font=("Segoe UI", 11), bd=1, relief="solid")
        self.user_input.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))
        self.user_input.bind("<Return>", lambda e: self.send_to_ai())

        self.send_btn = tk.Button(self.input_frame, text="Send", command=self.send_to_ai, 
                                 bg="#4A90E2", fg="white", font=("Helvetica", 10, "bold"), padx=20, pady=5)
        self.send_btn.pack(side="right")

    def send_to_ai(self):
        user_msg = self.user_input.get().strip()
        if not user_msg:
            return

        self.display_message("You", user_msg)
        self.user_input.delete(0, tk.END)

        try:
            # Send message to Gemini
            response = chat_session.send_message(user_msg)
            self.display_message("Bot", response.text)
        except Exception as e:
            # Check for Rate Limits (429) or Key Issues
            error_text = str(e)
            if "429" in error_text:
                self.display_message("System", "Error: Too many requests. Please wait a moment.")
            elif "API_KEY_INVALID" in error_text:
                self.display_message("System", "Error: Your API Key is invalid. Please check AI Studio.")
            else:
                self.display_message("System", f"Communication Error: {error_text}")

    def display_message(self, sender, text):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"{sender}: ", ("bold",))
        self.chat_area.insert(tk.END, f"{text}\n\n")
        self.chat_area.tag_configure("bold", font=("Segoe UI", 10, "bold"))
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

if __name__ == "__main__":
    window = tk.Tk()
    app = TherapyApp(window)
    window.mainloop()