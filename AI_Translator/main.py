import tkinter as tk
from tkinter import ttk
from deep_translator import GoogleTranslator
import pyperclip  # For copying text to clipboard
import pyttsx3  # For text-to-speech
from PIL import Image, ImageTk  # Import Pillow modules

engine = pyttsx3.init()

# Translate function using deep-translator
def translate_text():
    input_text = input_textbox.get("1.0", "end-1c").strip()  # Get input text and strip whitespace
    source_language = source_lang.get()  # Get selected source language
    target_language = target_lang.get()  # Get selected target language

    if not input_text:
        status_label.config(text="Please enter text to translate.", fg="red")
        return

    if source_language not in languages or target_language not in languages:
        status_label.config(text="Please select valid languages.", fg="red")
        return

    try:
        source_code = language_dict[source_language]
        target_code = language_dict[target_language]

        # Perform translation
        translated = GoogleTranslator(source=source_code, target=target_code).translate(input_text)
        output_textbox.config(state="normal")  # Enable temporarily
        output_textbox.delete("1.0", "end")  # Clear previous output
        output_textbox.insert("1.0", translated)  # Display translated text
        output_textbox.config(state="disabled")  # Disable input again

        status_label.config(text="Translation successful!", fg="green")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")

# Function to copy translated text to clipboard
def copy_text():
    translated_text = output_textbox.get("1.0", "end-1c")  # Get translated text
    if translated_text:
        pyperclip.copy(translated_text)  # Copy to clipboard using pyperclip
        status_label.config(text="Text copied to clipboard!", fg="blue")
    else:
        status_label.config(text="Nothing to copy.", fg="red")

# Function to clear text boxes
def clear_text():
    # Clear input text box
    input_textbox.delete("1.0", "end")  # Clear input text
    # Clear output text box
    output_textbox.config(state="normal")  # Enable temporarily
    output_textbox.delete("1.0", "end")  # Clear output text
    output_textbox.config(state="disabled")  # Disable input again
    status_label.config(text="Cleared text", fg="red")  # Reset status label

# Function to speak the translated text
def speak_text():
    translated_text = output_textbox.get("1.0", "end-1c")  # Get translated text
    if translated_text:
        engine.say(translated_text)  # Speak the translated text
        engine.runAndWait()  # Wait until speaking is finished
    else:
        status_label.config(text="Nothing to speak.", fg="red")

root = tk.Tk()
root.title("AI Language Translator")

# Set the window size and center it
window_width = 920
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Set window background color
root.config(bg="#f4f4f9")

# Language names and codes
language_dict = {
    "Arabic": "ar",
    "Chinese (Simplified)": "zh-CN",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Portuguese": "pt",
    "Spanish": "es",
    "Tagalog": "tl"
}
languages = list(language_dict.keys())

# Source language
source_lang_label = tk.Label(root, text="Source Language", font=("Arial", 12), bg="#f4f4f9")
source_lang_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

source_lang = ttk.Combobox(root, values=languages,width=16, state="readonly", font=("Arial", 10))
source_lang.set("English")  # Default source language (English)
source_lang.grid(row=1, column=0,columnspan=2, padx=20, pady=10)

# Status label for feedback
status_label = tk.Label(root, text="", font=("Arial", 12), fg="green", bg="#f4f4f9")
status_label.grid(row=1, column=1, columnspan=2, pady=10)

# Target language
target_lang_label = tk.Label(root, text="Target Language", font=("Arial", 12), bg="#f4f4f9")
target_lang_label.grid(row=0, column=2,columnspan=2, padx=20, pady=10)

target_lang = ttk.Combobox(root, values=languages, state="readonly", font=("Arial", 10))
target_lang.set("Spanish")  # Default target language (Spanish)
target_lang.grid(row=1, column=2,columnspan=2, padx=20, pady=10)

# Input text box
input_textbox = tk.Text(root, height=15, width=45, font=("Arial", 12), wrap="word",bd=0, highlightthickness=1, highlightbackground="#000000")
input_textbox.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
input_textbox.bind("<Return>", lambda event: translate_text())

# Output text box
output_textbox = tk.Text(root, height=15, width=45, font=("Arial", 12), wrap="word", bd=0, highlightthickness=1, highlightbackground="#000000")
output_textbox.grid(row=2, column=2, columnspan=2, padx=20)
output_textbox.config(state="disabled")  # Disable user input

translate_icon = ImageTk.PhotoImage(Image.open(r"icon\translate.png") .resize((30, 30)))  # Resize the image to 50x50
translate_button = tk.Button(root, image=translate_icon, command=translate_text, borderwidth=0)
translate_button.place(x=200, y=380)

copy_icon = ImageTk.PhotoImage(Image.open(r"icon\copy_icon.png") .resize((30, 30)))  # Resize the image to 50x50
copy_button = tk.Button(root, image=copy_icon, command=copy_text, borderwidth=0)
copy_button.place(x=480, y=380)

clear_icon = ImageTk.PhotoImage(Image.open(r"icon\x.png") .resize((30, 30)))  # Resize the image to 50x50
clear_button = tk.Button(root, image=clear_icon, command=clear_text, borderwidth=0)
clear_button.place(x=840, y=380)

speak_icon = ImageTk.PhotoImage(Image.open(r"icon\speak.png") .resize((30, 30)))  # Resize the image to 50x50
speak_button = tk.Button(root, image=speak_icon, command=speak_text, borderwidth=0)
speak_button.place(x=530, y=380)

root.mainloop()
