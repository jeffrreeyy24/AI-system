import tkinter as tk
import difflib

root = tk.Tk()
root.title("FAQ's")
root.geometry("450x600")
root.config(bg="#f4f4f9")

window_width = 450
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create a scrollable frame for chat history
chat_frame = tk.Frame(root, bg="#f4f4f9")
chat_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(chat_frame, bg="#f4f4f9", highlightthickness=0)
scrollbar = tk.Scrollbar(chat_frame, orient="vertical", command=canvas.yview)
chat_area = tk.Frame(canvas, bg="#f4f4f9")

canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas.create_window((0, 0), window=chat_area, anchor="nw")

def update_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

chat_area.bind("<Configure>", update_scroll_region)

# Configure grid weights for dynamic resizing
chat_area.columnconfigure(0, weight=1)  # Left spacer column
chat_area.columnconfigure(1, weight=0)  # Message bubble column
chat_area.columnconfigure(2, weight=1)  # Right spacer column

# Row tracker for grid positioning
row_tracker = 0

# Function to display messages in the chat area
def display_message(message, sender="bot"):
    global row_tracker

    # Determine alignment and colors
    if sender == "user":
        bg_color = "#2196F3"  # blue
        text_color = "white"
        sticky = "e"  # Align to the right
        column = 1
        padx = (50, 30)  # Spacer on the left
    else:
        bg_color = "#E0E0E0"  # white
        text_color = "black"
        sticky = "w"  # Align to the left
        column = 1
        padx = (40, 50)  # Spacer on the right

    # Create a label for the message bubble
    message_label = tk.Label(
        chat_area,
        text=message,
        bg=bg_color,
        fg=text_color,
        wraplength=300,  # Wrap text at 300 pixels
        font=("Arial", 12),
        padx=10,
        pady=5,
        bd=0,
        relief=tk.SOLID,
        justify = "left"  # Align multi-line text to the left

    )
    message_label.grid(row=row_tracker, column=column, padx=padx, pady=5, sticky=sticky)

    # Increment row tracker for the next message
    row_tracker += 1

    # Scroll to the bottom
    canvas.update_idletasks()
    canvas.yview_moveto(1)

# Function to start a new conversation
def start_new_conversation():
    global button_frame, input_frame, toggle_button

    reset_ui()
    display_message("Hello bot!", sender="user")
    display_message("Hello there! What can I help you with today?", sender="bot")
    toggle_button.config(text="Something Else", command=show_response_buttons)
    show_response_buttons()

# Function to display predefined response options
def show_response_buttons():
    global button_frame, input_frame, toggle_button

    button_frame.pack(fill=tk.X, pady=5)
    input_frame.pack_forget()  # Hide the input frame

    # Keep the toggle button functionality consistent
    toggle_button.config(text="Something Else to Ask?", command=show_input_box)

    # Define FAQ options
    options = ["Lost Account", "Technical Issue", "Billing Problem",
               "Game Feedback"]

    for widget in button_frame.winfo_children():
        widget.destroy()  # Clear existing buttons

    # Dynamically create FAQ option buttons
    for option in options:
        button = tk.Button(
            button_frame,
            text=option,
            font=("Arial", 10),
            bg="#2196f3",
            fg="white",
            command=lambda opt=option: handle_selection(opt)
        )
        button.pack(side=tk.LEFT, padx=5, pady=5)

# Function to show the input box for custom queries
def show_input_box():
    global button_frame, input_frame, toggle_button

    button_frame.pack_forget()
    input_frame.pack(fill=tk.X, pady=10)

    toggle_button.config(text="Select a Topic to Explore", command=show_response_buttons)

# Function to handle user response selection
def handle_selection(option):
    if option == "Something Else":
        show_input_box()
        return

    display_message(option, sender="user")
    response = get_faq_response(option)
    display_message(response, sender="bot")

# Function to send the user's custom message
def send_message():
    user_message = user_input.get().strip()
    if user_message == "":
        return
    display_message(user_message, sender="user")
    user_input.delete(0, tk.END)

    if user_message.lower() in ["thank you", "bye", "goodbye"]:
        reset_ui()
        return
    response = get_faq_response(user_message)
    display_message(response, sender="bot")

# Function to reset the UI for a new conversation
def reset_ui():
    for widget in chat_area.winfo_children():
        widget.destroy()
    button_frame.pack_forget()
    input_frame.pack_forget()
    toggle_button.config(text="New Conversation", command=start_new_conversation)


def get_faq_response(user_message):
    faqs = {
        "Lost Account": "Please provide your account ID, and we'll help recover it.",
        "Technical Issue": "Please describe the issue, and we’ll assist you.",
        "Billing Problem": "Contact our billing team for assistance with payments.",
        "Game Feedback": "We value your feedback! Please share your thoughts about the game, and we’ll forward them to our team."
    }

    # Find the closest match to the user's message
    closest_match = difflib.get_close_matches(user_message, faqs.keys(), n=1, cutoff=0.5)

    if closest_match:
        return faqs[closest_match[0]]
    return "I couldn't find an exact answer to your query. Could you provide more details or your question is not applicable to our business? "

# Create a frame for predefined response buttons
button_frame = tk.Frame(root, bg="#f4f4f9")

# Create a frame for the input field and send button
input_frame = tk.Frame(root, bg="#f4f4f9")
user_input = tk.Entry(input_frame, font=("Arial", 11), width=40, bd=2)
user_input.grid(row=0, column=0, padx=10, sticky="ew")

# Sending a message using enter key
user_input.bind("<Return>", lambda event: send_message())


send_button = tk.Button(input_frame, text="Send", font=("Arial", 12), bg="#4CAF50", fg="white", command=send_message)
send_button.grid(row=0, column=1, padx=10)
input_frame.grid_columnconfigure(0, weight=1)

# Create a toggle button
toggle_button = tk.Button(root, text="New Conversation", font=("Arial", 12), bg="#4CAF50", fg="white", command=start_new_conversation)
toggle_button.pack(fill=tk.X, pady=10)

root.mainloop()
