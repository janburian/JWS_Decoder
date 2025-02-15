import json
import os
import jwt
from pathlib import Path
from tkinter import Tk, Label, Button, filedialog, messagebox, StringVar, Text, Scrollbar, END, RIGHT, Y, BOTH, Frame, LEFT, Toplevel, Entry, PhotoImage

def get_filenames_list(licenses_path):
    filenames_list = []
    print("FILENAMES FOUND: ")
    try:
        for dirpath, dirnames, filenames in os.walk(licenses_path):
            for filename in filenames:
                if filename.endswith(".jws"):  # Adjust the file extension as needed
                    full_path = os.path.join(dirpath, filename)
                    filenames_list.append(full_path)
                    print(filename)
    except FileNotFoundError:
        print(f"Error: The directory '{licenses_path}' does not exist.")
    except PermissionError:
        print(f"Error: You do not have permission to access '{licenses_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return filenames_list

def get_output_information(filenames_list, text_widget):
    decoded_outputs_list = []
    idx = 0
    for filename in filenames_list:
        with open(filename, 'r') as f:
            print(filename)
            decoded = jwt.decode(f.read(), options={"verify_signature": False})
            decoded_outputs_list.append(decoded)
            decoded_json_str = json.dumps(decoded, sort_keys=True, indent=4)
            text_widget.insert(END, f"{filename}\n{decoded_json_str}\n\n")
            text_widget.see(END)
            idx += 1
    ask_save_output(decoded_outputs_list)

def save_output_to_json(decoded_outputs_list):
    try:
        with open('license_data.json', 'w', encoding='utf-8') as f:
            json.dump(decoded_outputs_list, f, sort_keys=True, ensure_ascii=False, indent=4)
        print("Decoded JSON list has been successfully saved to 'license_data.json'")
    except Exception as e:
        print(f"An error occurred while saving the JSON file: {e}")

def ask_save_output(decoded_outputs_list):
    response = messagebox.askyesno("Save Output", "Do you want to create a .json file with the output?")
    if response:
        save_output_to_json(decoded_outputs_list)
        messagebox.showinfo("Success", "Decoded JSON list has been successfully saved to 'license_data.json'")

def select_files():
    licenses_path = filedialog.askdirectory(title="Select Directory Containing JWS Files")
    if licenses_path:
        path_var.set(licenses_path)
        full_filenames_list = get_filenames_list(Path(licenses_path))
        get_output_information(full_filenames_list, text_widget)

def open_search_dialog():
    search_window = Toplevel(root)
    search_window.title("Search")
    search_window.geometry("300x50")
    Label(search_window, text="Find:").pack(side=LEFT, padx=10)
    search_entry = Entry(search_window, width=20)
    search_entry.pack(side=LEFT, padx=10)

    def search_text():
        text_widget.tag_remove("match", "1.0", END)
        search_term = search_entry.get()
        if search_term:
            idx = "1.0"
            while True:
                idx = text_widget.search(search_term, idx, nocase=1, stopindex=END)
                if not idx:
                    break
                lastidx = f"{idx}+{len(search_term)}c"
                text_widget.tag_add("match", idx, lastidx)
                idx = lastidx
            text_widget.tag_config("match", background="yellow")

    search_entry.bind('<Return>', lambda event: search_text())
    Button(search_window, text="Find", command=search_text).pack(side=LEFT, padx=10)

# Create the main window
root = Tk()
root.title("JWS File Decoder")
root.geometry("1000x500")

# Bind Ctrl+F to open the search dialog
root.bind('<Control-f>', lambda event: open_search_dialog())

# GUI Widgets
Label(root, text="Tool for decoding license files in .jws format", font=("Helvetica", 16, "bold")).pack(pady=5)
path_var = StringVar()
Label(root, textvariable=path_var).pack(pady=5)
Button(root, text="Browse...", command=select_files).pack(pady=(10, 5))

# Add image to the main window
# Note: Replace 'your_image.png' with the path to the image you saved
# photo = PhotoImage(file="your_image.png")
# image_label = Label(root, image=photo)
# image_label.place(relx=1.0, y=10, anchor="ne")

# Frame to hold the Text widget and Scrollbar
Label(root, text="Output:", font=("Helvetica", 12, "bold")).pack(pady=5, anchor='w')
text_frame = Frame(root)
text_frame.pack(pady=5, expand=True, fill=BOTH)

# Text widget to display decoded JSON
text_widget = Text(text_frame, wrap='word')
text_widget.pack(side=LEFT, expand=True, fill=BOTH)

# Scrollbar for the Text widget
scrollbar = Scrollbar(text_frame, command=text_widget.yview, width=20)
scrollbar.pack(side=RIGHT, fill=Y)
text_widget.configure(yscrollcommand=scrollbar.set)

# Start the GUI loop
root.mainloop()
