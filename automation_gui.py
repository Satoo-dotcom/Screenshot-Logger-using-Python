import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import shutil
import os

class AutomationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automation Toolkit")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # File Operations Tab
        file_ops_frame = ttk.Frame(notebook)
        notebook.add(file_ops_frame, text='File Operations')
        self.create_file_ops_tab(file_ops_frame)

        # Placeholder for other tabs
        # notebook.add(ttk.Frame(notebook), text='Batch Image Resize')
        # notebook.add(ttk.Frame(notebook), text='Send Email')
        # notebook.add(ttk.Frame(notebook), text='Web Form Filler')

    def create_file_ops_tab(self, parent):
        # Source file/folder selection
        self.src_path = tk.StringVar()
        self.dst_path = tk.StringVar()
        ttk.Label(parent, text="Source:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        ttk.Entry(parent, textvariable=self.src_path, width=40).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(parent, text="Browse", command=self.browse_src).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(parent, text="Destination:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        ttk.Entry(parent, textvariable=self.dst_path, width=40).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(parent, text="Browse", command=self.browse_dst).grid(row=1, column=2, padx=5, pady=5)

        # Operation buttons
        ttk.Button(parent, text="Copy", command=self.copy_file).grid(row=2, column=0, padx=5, pady=10)
        ttk.Button(parent, text="Move", command=self.move_file).grid(row=2, column=1, padx=5, pady=10)
        ttk.Button(parent, text="Rename", command=self.rename_file).grid(row=2, column=2, padx=5, pady=10)

    def browse_src(self):
        path = filedialog.askopenfilename()
        if path:
            self.src_path.set(path)

    def browse_dst(self):
        path = filedialog.askdirectory()
        if path:
            self.dst_path.set(path)

    def copy_file(self):
        src = self.src_path.get()
        dst = self.dst_path.get()
        if not src or not dst:
            messagebox.showerror("Error", "Please select both source and destination.")
            return
        try:
            shutil.copy(src, dst)
            messagebox.showinfo("Success", f"Copied to {dst}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def move_file(self):
        src = self.src_path.get()
        dst = self.dst_path.get()
        if not src or not dst:
            messagebox.showerror("Error", "Please select both source and destination.")
            return
        try:
            shutil.move(src, dst)
            messagebox.showinfo("Success", f"Moved to {dst}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def rename_file(self):
        src = self.src_path.get()
        dst = self.dst_path.get()
        if not src or not dst:
            messagebox.showerror("Error", "Please select both source and new name (destination).")
            return
        try:
            base = os.path.dirname(src)
            new_path = os.path.join(base, dst)
            os.rename(src, new_path)
            messagebox.showinfo("Success", f"Renamed to {new_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = AutomationApp()
    app.mainloop()