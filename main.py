import time
import os
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from google import genai

MODEL = "gemini-3.8-flash"

SYSTEM_INSTRUCTION = """
You are a friendly AI tutor.
Explain concepts in simple English.
Use examples and step-by-step explanations when helpful.
Be supportive, accurate, and concise.
Adapt your explanations to the student's questions.
"""


class AITutorChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Tutor Chatbot")
        self.root.geometry("800x650")
        self.root.minsize(600, 500)
        self.root.configure(bg="#f3f5f9")

        self.history = []
        self.busy = False

        api_key = os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key) if api_key else None

        self.create_ui()

    def create_ui(self):
        header = tk.Frame(self.root, bg="#243b64", pady=16)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="AI Tutor Chatbot",
            font=("Arial", 21, "bold"),
            fg="white",
            bg="#243b64"
        ).pack()

        tk.Label(
            header,
            text="Ask questions. Learn at your own pace.",
            font=("Arial", 10),
            fg="#e0e7ff",
            bg="#243b64"
        ).pack(pady=(5, 0))

        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Arial", 11),
            bg="white",
            fg="#202938",
            padx=14,
            pady=12,
            state=tk.DISABLED
        )
        self.chat_area.pack(
            fill=tk.BOTH, expand=True, padx=16, pady=14
        )

        self.chat_area.tag_config(
            "user", foreground="#2459a9",
            font=("Arial", 11, "bold")
        )
        self.chat_area.tag_config(
            "tutor", foreground="#16805d",
            font=("Arial", 11, "bold")
        )
        self.chat_area.tag_config(
            "body", foreground="#202938",
            font=("Arial", 11)
        )

        input_frame = tk.Frame(self.root, bg="#f3f5f9")
        input_frame.pack(fill=tk.X, padx=16, pady=(0, 8))

        self.message_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            relief=tk.SOLID,
            bd=1
        )
        self.message_entry.pack(
            side=tk.LEFT, fill=tk.X, expand=True, ipady=10
        )
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg="#3159a5",
            fg="white",
            activebackground="#244680",
            activeforeground="white",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        self.send_button.pack(side=tk.LEFT, padx=(8, 0))

        footer = tk.Frame(self.root, bg="#f3f5f9")
        footer.pack(fill=tk.X, padx=16, pady=(0, 14))

        self.status = tk.Label(
            footer,
            text="Ready to help you learn",
            bg="#f3f5f9",
            fg="#596579",
            anchor="w"
        )
        self.status.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(
            footer,
            text="Clear Chat",
            command=self.clear_chat,
            font=("Arial", 9),
            relief=tk.GROOVE,
            cursor="hand2"
        ).pack(side=tk.RIGHT)

        self.add_message(
            "AI Tutor",
            "Hello! I'm your AI tutor. Ask me anything you want to learn."
        )

        self.message_entry.focus_set()

    def add_message(self, sender, message):
        self.chat_area.configure(state=tk.NORMAL)

        tag = "user" if sender == "You" else "tutor"
        self.chat_area.insert(tk.END, f"{sender}\n", tag)
        self.chat_area.insert(tk.END, f"{message}\n\n", "body")

        self.chat_area.configure(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def send_message(self, event=None):
        if self.busy:
            return

        message = self.message_entry.get().strip()
        if not message:
            return

        if not self.client:
            messagebox.showerror(
                "API Key Missing",
                "Set your GEMINI_API_KEY environment variable "
                "in the terminal, then restart the application."
            )
            return

        self.message_entry.delete(0, tk.END)
        self.add_message("You", message)

        self.history.append({
            "role": "user",
            "parts": [{"text": message}]
        })

        self.busy = True
        self.send_button.configure(state=tk.DISABLED)
        self.status.configure(text="Tutor is thinking...")

        threading.Thread(
            target=self.get_ai_response,
            daemon=True
        ).start()

    
    def get_ai_response(self):
        answer = None
        last_error = None

        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=MODEL,
                    contents=[
                        {
                            "role": "user",
                            "parts": [{"text": SYSTEM_INSTRUCTION}]
                        },
                        *self.history
                    ]
                )

                answer = response.text
                if not answer:
                    answer = "No response generated. Please try again."
                break

            except Exception as error:
                last_error = error
                print(f"API attempt {attempt + 1} failed: {error}")

                if "503" not in str(error) or attempt == 2:
                    break

                time.sleep(2 * (attempt + 1))

        if answer:
            self.root.after(0, self.finish_response, answer)
        else:
            self.root.after(
                0, self.handle_error,
                str(last_error) if last_error else "Unknown API error"
            )

    def finish_response(self, answer):
        # Update conversation history on the Tkinter UI thread
        if answer and not answer.startswith("No response generated"):
            self.history.append({
                "role": "model",
                "parts": [{"text": answer}]
            })

        self.add_message("AI Tutor", answer)
        self.status.configure(text="Ready to help you learn")
        self.busy = False
        self.send_button.configure(state=tk.NORMAL)
        self.message_entry.focus_set()

    def handle_error(self, error):
        self.add_message(
            "AI Tutor",
            "Sorry, I couldn't get a response. "
            "Please check your internet connection, API key, "
            "model availability, and API quota."
        )
        print("API error:", error)

        self.status.configure(text="Request failed — please try again")
        self.busy = False
        self.send_button.configure(state=tk.NORMAL)

        # Remove the failed user message from API history
        if self.history and self.history[-1]["role"] == "user":
            self.history.pop()

    def clear_chat(self):
        if self.busy:
            messagebox.showinfo(
                "Please wait",
                "Wait for the current response to finish."
            )
            return

        self.history.clear()

        self.chat_area.configure(state=tk.NORMAL)
        self.chat_area.delete("1.0", tk.END)
        self.chat_area.configure(state=tk.DISABLED)

        self.add_message(
            "AI Tutor",
            "New conversation started! What would you like to learn?"
        )
        self.status.configure(text="Conversation history cleared")


if __name__ == "__main__":
    root = tk.Tk()
    app = AITutorChatbot(root)
    root.mainloop()
