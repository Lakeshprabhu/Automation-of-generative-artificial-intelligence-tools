from tkinter import PhotoImage, messagebox,simpledialog
import tkinter as tk
from filereader import PDF
from deepseek import Deepseek
import os
import subprocess
import pandas
import sys

model_mapping = {
    "Chatgpt": "1",
    "Gemini": "2",
}

def get_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def starting():
    os.makedirs(get_path("complex_extract"), exist_ok=True)
    os.makedirs(get_path("excel"), exist_ok=True)
    user_input = None
    model_input = model_var.get()
    print(model_input)
    if model_input == "Chatgpt":
        user_input = simpledialog.askstring("Input","Enter API KEY to be used for Chatgpt")
    if model_input == "Deepseek":
        user_input = simpledialog.askstring("Input","Enter API KEY to be used for Deepseek")

    gem_input = simpledialog.askstring("Input", "Enter API KEY to be used for Gemini")
    file = file_entry.get()
    model_input = model_mapping.get(model_input)
    Pdf = PDF(file, model_input, user_input,gem_input)

    Pdf.extract_to_file_text()

    answers = Pdf.start_()

    excel_path = answers
    messagebox.showinfo(title="Finished", message="The answer scripts have been generated")

    try:
        os.startfile(excel_path)  # Simple and reliable
        messagebox.showinfo("Finished", "Excel file opened successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Excel file:\n{e}")

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Automation of Generative AI Tools")
    window.geometry("1000x1000")
    window.config(background="white")
    window.resizable(False, False)

    image_path = PhotoImage(file=get_path("photo/img.png"))
    image = tk.Label(window, image=image_path, highlightthickness=0, borderwidth=0)
    image.pack(pady=5)

    model_frame = tk.Frame(window, bg="#e0e0e0", bd=2, relief=tk.GROOVE)
    model_frame.pack(pady=(20,10), padx=20, fill="x")

    model_title = tk.Label(model_frame, text="Select AI Model", font=("Helvetica", 14, "bold"), bg="#e0e0e0")
    model_title.pack(pady=(10,5))

    model_var = tk.StringVar()
    model_dropdown = tk.OptionMenu(model_frame, model_var, "Chatgpt", "Gemini")
    model_dropdown.config(width=25, font=("Helvetica", 12))
    model_dropdown.pack(pady=(0,10))



    tk.Label(window, text="Enter PDF Path:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=(15,5))
    file_entry = tk.Entry(window, width=40, font=("Helvetica", 11))
    file_entry.pack(pady=5)

    start_button = tk.Button(window, text="Start", command=starting,
                             bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5)
    start_button.pack(pady=25)

    window.mainloop()
