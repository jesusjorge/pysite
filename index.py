import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

def new_file():
    text_area.delete("1.0", tk.END)
    root.title("This is just a Test of Python from Web - Notepad")

def open_file():
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, file.read())
        root.title(f"{file_path} - Notepad")

def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get("1.0", tk.END))
        root.title(f"{file_path} - Notepad")

def exit_app():
    root.quit()

root = tk.Tk()
root.title("Wep2222 - Notepad")
root.geometry("800x600")

# Text area
text_area = ScrolledText(root, font=("Consolas", 12))
text_area.pack(fill=tk.BOTH, expand=True)

# Menu bar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Nuevo", command=new_file)
file_menu.add_command(label="Abrir...", command=open_file)
file_menu.add_command(label="Guardar como...", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=exit_app)
menu_bar.add_cascade(label="Archivo", menu=file_menu)

root.config(menu=menu_bar)
root.mainloop()
