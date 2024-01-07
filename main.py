import tkinter as tk
from tkinter import filedialog, simpledialog
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

# Initialize file_path as a global variable
file_path = ""

def open_file(*args):
    global file_path, modified
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())
        root.title(f"Simple Text Editor - {file_path}")
        modified = False

def save_file(*args):
    global file_path, modified
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text.get(1.0, tk.END))
        root.title(f"Simple Text Editor - {file_path}")
        modified = False
    else:
        save_as_file()

def save_as_file(*args):
    global file_path, modified
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text.get(1.0, tk.END))
        root.title(f"Simple Text Editor - {file_path}")
        modified = False

def convert_to_pdf(*args):
    global file_path
    if not file_path:
        save_as_file()

    pdf_path = file_path[:-3] + "pdf"
    pdf_canvas = canvas.Canvas(pdf_path)
    pdf_canvas.setFont("Helvetica", 12)
    text_content = text.get(1.0, tk.END)
    pdf_canvas.drawString(50, 750, text_content)
    pdf_canvas.save()
    root.title(f"Simple Text Editor - {pdf_path}")

def open_pdf(*args):
    global file_path, modified
    file_path = filedialog.askopenfilename(defaultextension=".pdf",
                                           filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")])
    if file_path:
        pdf_reader = PdfReader(file_path)
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text()
        text.delete(1.0, tk.END)
        text.insert(tk.END, text_content)
        root.title(f"Simple Text Editor - {file_path}")
        modified = False

from PyPDF2 import PdfReader, PdfWriter

# ... (previous code)

def save_as_pdf(*args):
    global file_path, modified
    if not file_path:
        save_as_file()

    pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")])
    if pdf_path:
        pdf_writer = PdfWriter()
        pdf_writer.add_blank_page()  # Updated method to add a blank page
        pdf_writer.pages[0].merge_page(file_path)
        with open(pdf_path, 'wb') as pdf_file:
            pdf_writer.write(pdf_file)
        root.title(f"Simple Text Editor - {pdf_path}")
        modified = False


def on_text_change(event):
    global modified
    modified = True

def increase_font_size_popup():
    new_size = simpledialog.askinteger("Font Size", "Enter the new font size:", parent=root)
    if new_size is not None:
        text.config(font=("Helvetica", new_size))

def change_font(font_name):
    text.config(font=(font_name, text.cget("size")))

root = tk.Tk()
root.title("Simple Text Editor")
root.configure(bg='#E0FFFF')

text_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN, bg='#E0FFFF')
text_frame.pack(expand=True, fill="both", padx=10, pady=10)

text = tk.Text(text_frame, wrap="word", undo=True, bg='white', fg='black', font=("Helvetica", 12))
text.pack(expand=True, fill="both")

menu_bar = tk.Menu(root, bg='#87CEEB')
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0, bg='#87CEEB')
menu_bar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Save As", command=save_as_file, accelerator="Ctrl+Shift+S")
file_menu.add_separator()
file_menu.add_command(label="Convert to PDF", command=convert_to_pdf)
file_menu.add_command(label="Open PDF", command=open_pdf)
file_menu.add_command(label="Save As PDF", command=save_as_pdf)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)

edit_menu = tk.Menu(menu_bar, tearoff=0, bg='#87CEEB')
menu_bar.add_cascade(label="Edit", menu=edit_menu)

edit_menu.add_command(label="Increase Font Size", command=increase_font_size_popup)

font_menu = tk.Menu(menu_bar, tearoff=0, bg='#87CEEB')
menu_bar.add_cascade(label="Font", menu=font_menu)

font_menu.add_command(label="Helvetica", command=lambda: change_font("Helvetica"))
font_menu.add_command(label="Arial", command=lambda: change_font("Arial"))
font_menu.add_command(label="Courier", command=lambda: change_font("Courier"))
font_menu.add_command(label="Times", command=lambda: change_font("Times"))
font_menu.add_command(label="Verdana", command=lambda: change_font("Verdana"))

root.bind("<Control-o>", open_file)
root.bind("<Control-s>", save_file)
root.bind("<Control-S>", save_as_file)

modified = False
text.bind("<<Modified>>", on_text_change)

root.mainloop()
