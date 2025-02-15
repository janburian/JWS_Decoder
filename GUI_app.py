import json
import os
import jwt
from pathlib import Path
from tkinter import Tk, Label, Button, filedialog, messagebox, StringVar, Text, Scrollbar, END, RIGHT, Y, BOTH, Frame, LEFT

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
    save_output_to_json(decoded_outputs_list)

def save_output_to_json(decoded_outputs_list):
    try:
        with open('license_data.json', 'w', encoding='utf-8') as f:
            json.dump(decoded_outputs_list, f, sort_keys=True, ensure_ascii=False, indent=4)
        print("Decoded JSON list has been successfully saved to 'license_data.json'")
    except Exception as e:
        print(f"An error occurred while saving the JSON file: {e}")

def select_files():
    licenses_path = filedialog.askdirectory(title="Select Directory Containing JWS Files")
    if licenses_path:
        path_var.set(licenses_path)
        full_filenames_list = get_filenames_list(Path(licenses_path))
        get_output_information(full_filenames_list, text_widget)
        messagebox.showinfo("Success", "Decoded JSON list has been successfully saved to 'license_data.json'")

# Create the main window
root = Tk()
root.title("JWS File Decoder")
root.geometry("1000x500")

# GUI Widgets
#Label(root, text="Tool for decoding JWS files.").pack(pady=2)
Label(root, text="Tool for decoding license files in .jws format", font=("Helvetica", 16, "bold")).pack(pady=5)
path_var = StringVar()
Label(root, textvariable=path_var).pack(pady=5)
Button(root, text="Browse...", command=select_files).pack(pady=(10, 5))

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
