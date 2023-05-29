import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str):
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def handle_user_input(event=None):
    user_input = entry.get()

    if user_input.lower() == 'quit':
        window.quit()
        return

    # Display the user's input in the chat area
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "You: " + user_input + "\n", "user")
    chat_area.see(tk.END)  # Scroll to the bottom
    chat_area.config(state=tk.DISABLED)

    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
    else:
        answer = "I don't know the answer. Can you teach me?"

    # Display the bot's response in the chat area
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "Bot: " + answer + "\n", "bot")
    chat_area.see(tk.END)  # Scroll to the bottom
    chat_area.config(state=tk.DISABLED)

    if not best_match:
        new_answer = messagebox.askquestion("New Answer", "Do you want to add a new answer?")

        if new_answer == 'yes':
            answer = messagebox.askstring("New Answer", "Enter the answer:")
            if answer:
                knowledge_base["questions"].append({"question": user_input, "answer": answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                messagebox.showinfo("Bot Response", "Thank you! I've learned something new.")

    entry.delete(0, tk.END)  # Clear the user input

knowledge_base = load_knowledge_base('knowledge_base.json')

window = tk.Tk()
window.title("Chat Bot GUI")
window.geometry("500x500")
window.resizable(0, 0)

# Load and set the background image for the chat area
bg_image = Image.open("background.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a frame to hold the chat area and scrollbar
chat_frame = ttk.Frame(window, style="Chat.TFrame")
chat_frame.place(x=10, y=10, width=480, height=420)

# Create a chat area using a Text widget
chat_area = tk.Text(
    chat_frame,
    height=20,
    width=58,
    state=tk.DISABLED,
    font=("Arial", 12),
    background="#F7F7F7",
    foreground="#000000",
    insertbackground="#000000",
    relief=tk.FLAT
)
chat_area.tag_config("user", foreground="#0096FF")
chat_area.tag_config("bot", foreground="#7BFF00")
chat_area.pack(pady=10)

# Add a scrollbar to the chat area
scrollbar = ttk.Scrollbar(chat_frame, command=chat_area.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_area.config(yscrollcommand=scrollbar.set)

# Create a label and an entry field for user input
label = tk.Label(
    window,
    text="Enter your message:",
    font=("Arial", 12),
    foreground="#FFFFFF",
    background="#2B2B2B"
)
label.place(x=10, y=440)

entry = tk.Entry(
    window,
    width=40,
    font=("Arial", 12),
    background="#FFFFFF",
    foreground="#000000",
    relief=tk.FLAT,
    bd=1
)
entry.place(x=140, y=440)
entry.focus()  # Set focus to the entry field

# Create a button to send the user input
button = tk.Button(
    window,
    text="Send",
    command=handle_user_input,
    font=("Arial", 12),
    background="#0096FF",
    foreground="#FFFFFF",
    activebackground="#007ACC",
    activeforeground="#FFFFFF",
    relief=tk.FLAT,
    bd=0
)
button.place(x=400, y=438)

# Bind the Enter key to the send functionality
window.bind("<Return>", handle_user_input)

# Configure the ttk styles
style = ttk.Style()
style.configure("Chat.TFrame", background="#2B2B2B")
style.configure("TLabel", foreground="#FFFFFF")

window.mainloop()

