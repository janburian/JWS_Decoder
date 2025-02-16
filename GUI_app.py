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


def save_output_to_json(decoded_outputs_list, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(decoded_outputs_list, f, sort_keys=True, ensure_ascii=False, indent=4)
        print(f"Decoded JSON list has been successfully saved to '{file_path}'")
    except Exception as e:
        print(f"An error occurred while saving the JSON file: {e}")


def ask_save_output(decoded_outputs_list):
    response = messagebox.askyesno("Save Output", "Do you want to create a .json file with the output?")
    if response:
        file_path = 'license_data.json'
        if os.path.exists(file_path):
            overwrite_response = messagebox.askyesnocancel("Save Output", f"'{file_path}' already exists. Do you want to overwrite it?", parent=root)
            if overwrite_response is None:
                return  # User cancelled
            elif overwrite_response:
                save_output_to_json(decoded_outputs_list, file_path)
                messagebox.showinfo("Success", f"Decoded JSON list has been successfully saved to '{file_path}'", parent=root)
            else:
                file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], parent=root)
                if file_path:
                    save_output_to_json(decoded_outputs_list, file_path)
                    messagebox.showinfo("Success", f"Decoded JSON list has been successfully saved to '{file_path}'", parent=root)
        else:
            save_output_to_json(decoded_outputs_list, file_path)
            messagebox.showinfo("Success", f"Decoded JSON list has been successfully saved to '{file_path}'", parent=root)


def select_files():
    text_widget.delete("1.0", END)  # Clear the text widget
    licenses_path = filedialog.askdirectory(title="Select Directory Containing JWS Files", parent=root)
    if licenses_path:
        path_var.set(licenses_path)
        full_filenames_list = get_filenames_list(Path(licenses_path))
        get_output_information(full_filenames_list, text_widget)


def select_single_file():
    text_widget.delete("1.0", END)  # Clear the text widget
    file_path = filedialog.askopenfilename(filetypes=[("JWS files", "*.jws")], parent=root)
    if file_path:
        path_var.set(file_path)
        get_output_information([Path(file_path)], text_widget)


def select_multiple_files():
    text_widget.delete("1.0", END)  # Clear the text widget
    files = filedialog.askopenfilenames(filetypes=[("JWS files", "*.jws")], parent=root)
    if files:
        path_var.set("; ".join(files))
        get_output_information(list(map(Path, files)), text_widget)


def open_search_dialog():
    search_window = Toplevel(root)
    search_window.title("Search")
    search_window.geometry("300x50")

    window_x = root.winfo_x()
    window_y = root.winfo_y()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    search_window.geometry("+%d+%d" % (window_x + window_width//2 - 150, window_y + window_height//2 - 25))

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
# root.geometry("1000x500")

window_width = 1000
window_height = 600

# Position the main window in the center of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_x = int(screen_width/2 - window_width/2)
position_y = int(screen_height/2 - window_height/2)
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

# Bind Ctrl+F to open the search dialog
root.bind('<Control-f>', lambda event: open_search_dialog())

# GUI Widgets
Label(root, text="Tool for decoding license files in .jws format", font=("Helvetica", 16, "bold")).pack(pady=5)
path_var = StringVar()
Label(root, textvariable=path_var).pack(pady=5)
frame_buttons = Frame(root)
frame_buttons.pack(pady=(10, 5))
Button(frame_buttons, text="Browse Directory...", command=select_files).pack(side=LEFT, padx=5)
Button(frame_buttons, text="Select Single File...", command=select_single_file).pack(side=LEFT, padx=5)
Button(frame_buttons, text="Select Multiple Files...", command=select_multiple_files).pack(side=LEFT, padx=5)

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