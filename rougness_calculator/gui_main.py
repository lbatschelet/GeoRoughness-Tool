"""
gui_main.py
-----------
Version: 0.1.0
Author: Lukas Batschelet
Date: 18.04.2024
-----------
THIS IS AN EARLY VERSION OF THE GUI
FUNCTIONALITY IS LIMITED
This module contains the ApplicationGUI class which is
responsible for creating the graphical user interface (GUI) of the application.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button, Entry

from rougness_calculator.application_driver import ApplicationDriver


class ApplicationGUI:
    def __init__(self, master):
        self.master = master
        master.title("GeoTIFF Processor")
        master.geometry("700x300")  # Increased width to accommodate all elements

        # Label and entry for input path
        Label(master, text="Input TIFF Path:").grid(row=0, column=0, sticky='w')
        self.input_path_entry = Entry(master, width=58)
        self.input_path_entry.grid(row=0, column=1)
        Button(master, text="Browse", command=self.load_input).grid(row=0, column=2)

        # Label and entry for output directory
        Label(master, text="Output Directory:").grid(row=1, column=0, sticky='w')
        self.output_dir_entry = Entry(master, width=58)
        self.output_dir_entry.grid(row=1, column=1)
        Button(master, text="Browse", command=self.set_output_dir).grid(row=1, column=2)

        # Entry for window size with description
        Label(master, text="Window Size (m): (Default = 1)").grid(row=2, column=0, sticky='w')
        self.window_size_entry = Entry(master, width=10)
        self.window_size_entry.grid(row=2, column=1)

        # Entry for band number with description
        Label(master, text="Band Number: (Default = 1)").grid(row=3, column=0, sticky='w')
        self.band_number_entry = Entry(master, width=10)
        self.band_number_entry.grid(row=3, column=1)

        # Entry for high value threshold with description
        Label(master, text="High Value Threshold: (Default = 1)").grid(row=4, column=0, sticky='w')
        self.high_value_threshold_entry = Entry(master, width=10)
        self.high_value_threshold_entry.grid(row=4, column=1)

        # Button to start processing
        Button(master, text="Start Processing", command=self.start_processing).grid(row=5, column=1, pady=20)

    def load_input(self):
        filename = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tif *.tiff")])
        if filename:
            self.input_path_entry.delete(0, tk.END)
            self.input_path_entry.insert(0, filename)

    def set_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_entry.delete(0, tk.END)
            self.output_dir_entry.insert(0, directory)

    def start_processing(self):
        input_path = self.input_path_entry.get()
        output_dir = self.output_dir_entry.get()

        if not input_path or not output_dir:
            messagebox.showerror("Error", "Please specify both input and output directory.")
            return

        window_size = self.window_size_entry.get()
        band_number = self.band_number_entry.get()
        high_value_threshold = self.high_value_threshold_entry.get()

        try:
            # Assuming ApplicationDriver can handle input and output directory
            driver = ApplicationDriver(input_path, output_dir,
                                       int(window_size) if window_size.isdigit() else 1,
                                       int(band_number) if band_number.isdigit() else 1,
                                       int(high_value_threshold) if high_value_threshold.isdigit() else 1)
            driver.run()
            messagebox.showinfo("Success", "Processing completed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = ApplicationGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
