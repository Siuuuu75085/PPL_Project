import tkinter as tk
from tkinter import scrolledtext
from handle_input import handle_input  

class ChatboxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbox")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12), state='disabled')
        self.chat_display.pack(padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.entry = tk.Entry(self.input_frame, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry.bind("<Return>", self.process_input)

        self.send_button = tk.Button(self.input_frame, text="Send", font=("Arial", 12), command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

        self.add_message("System", "Chatbox is now online. Type 'exit' to quit.")

    def add_message(self, sender, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.yview(tk.END)

    def send_message(self):
        self.process_input(None)

    def process_input(self, event):
        user_input = self.entry.get().strip()
        self.entry.delete(0, tk.END)

        if not user_input:
            return

        if user_input.lower() in ("exit", "quit"):
            self.root.quit()

        self.add_message("You", user_input)

        try:
            response = handle_input(user_input)
            self.add_message("Chatbox", response)
        except Exception as e:
            self.add_message("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatboxApp(root)
    root.mainloop()
