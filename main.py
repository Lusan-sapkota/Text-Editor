import tkinter as tk
from tkinter import filedialog


def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())
        root.title(f"Simple Text Editor - {file_path}")


def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text.get(1.0, tk.END))
        root.title(f"Simple Text Editor - {file_path}")


root = tk.Tk()
root.title("Simple Text Editor")

# Create a Frame to hold the Text widget and give it a border
text_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
text_frame.pack(expand=True, fill="both", padx=10, pady=10)

text = tk.Text(text_frame, wrap="word", undo=True)
text.pack(expand=True, fill="both")

# Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)

root.mainloop()
