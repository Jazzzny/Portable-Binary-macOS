# PortableBinaryGUI.py
# Copyright (c) 2024 Jazzzny

from argparse import Namespace
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PortableBinary import PortableBinary, version

class PortableBinaryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Portable Binary {version} GUI")
        self.root.geometry("500x125")
        self.root.resizable(False, False)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)

        # Binary file selection
        self.binary_label = ttk.Label(self.root, text="Binary:")
        self.binary_label.grid(row=0, column=0, sticky="e")

        self.binary_entry = ttk.Entry(self.root)
        self.binary_entry.grid(row=0, column=1, sticky="ew")

        self.binary_browse_button = ttk.Button(self.root, text="Browse...", command=self.browse_binary)
        self.binary_browse_button.grid(row=0, column=2, padx=(0, 10))

        # Output directory selection
        self.output_dir_label = ttk.Label(self.root, text="Output Directory:")
        self.output_dir_label.grid(row=1, column=0, sticky="e")

        self.output_dir_entry = ttk.Entry(self.root)
        self.output_dir_entry.grid(row=1, column=1, sticky="ew")

        self.output_dir_browse_button = ttk.Button(self.root, text="Browse...", command=self.browse_output_dir)
        self.output_dir_browse_button.grid(row=1, column=2, padx=(0, 10))

        # Library directory name input
        self.lib_dir_name_label = ttk.Label(self.root, text="Library Directory Name:")
        self.lib_dir_name_label.grid(row=2, column=0, sticky="e")

        self.lib_dir_name_entry = ttk.Entry(self.root)
        self.lib_dir_name_entry.grid(row=2, column=1, sticky="ew")

        self.lib_dir_name_entry.insert(0, "lib")

        # Run button
        self.run_button = ttk.Button(self.root, text="Run", command=self.run)
        self.run_button.grid(row=3, column=0, columnspan=3, pady=5)

    def browse_binary(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.binary_entry.delete(0, tk.END)
            self.binary_entry.insert(0, filename)

    def browse_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, directory)

    def showinfo(self, title, message):
        tk.messagebox.showinfo(title, message)

    def run(self):
        portable_binary = PortableBinary(Namespace(binary=self.binary_entry.get(), output_dir=self.output_dir_entry.get(), lib_dir_name=self.lib_dir_name_entry.get()))
        result = portable_binary.run()
        if result == 0:
            self.showinfo("Success", "Portable binary created successfully!")
        else:
            self.showerror("Error", "An error occurred while creating the portable binary.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PortableBinaryGUI(root)
    root.mainloop()