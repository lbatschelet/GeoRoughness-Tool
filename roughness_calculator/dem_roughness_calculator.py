"""
dem_roughness_calculator.py
-----------
Version: 0.2.0
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

from PIL import Image, ImageTk

from roughness_calculator.classes.application_driver import ApplicationDriver


import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button, Entry, Frame

class ApplicationGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("GeoTIFF Processor")

        # Set initial geometry based on screen size and make it resizable
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = int(screen_width * 0.5)  # Adjust width as needed
        window_height = int(screen_height * 0.7)
        self.master.geometry(f"{window_width}x{window_height}")

        # Setup GUI components
        self.setup_gui()

        # Bind the window resize event to adjust the image label height dynamically
        self.master.bind("<Configure>", self.adjust_image_label_height)

    def setup_gui(self):
        """ Setup GUI components in the main application window """
        # Ensure that all main GUI components fill the window and expand as needed
        self.master.grid_columnconfigure(0, weight=1)

        # Header with description
        header_frame = Frame(self.master)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        header_frame.grid_columnconfigure(0, weight=1)
        Label(header_frame, text="Welcome to the GeoTIFF Processor!", font=("Helvetica", 16, "bold")).grid(row=0,
                                                                                                           column=0,
                                                                                                           sticky="ew")
        Label(header_frame, text="Adjust the settings below and load your GeoTIFF files to begin processing.",
              font=("Helvetica", 10)).grid(row=1, column=0, sticky="ew")

        # Input and Output configuration
        config_frame = Frame(self.master)
        config_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        config_frame.grid_columnconfigure(1, weight=1)
        Label(config_frame, text="Input TIFF Path:").grid(row=0, column=0, sticky='w')
        self.input_path_entry = Entry(config_frame)
        self.input_path_entry.grid(row=0, column=1, sticky="ew")
        Button(config_frame, text="Browse", command=self.load_input).grid(row=0, column=2)

        Label(config_frame, text="Output Directory:").grid(row=1, column=0, sticky='w')
        self.output_dir_entry = Entry(config_frame)
        self.output_dir_entry.grid(row=1, column=1, sticky="ew")
        Button(config_frame, text="Browse", command=self.set_output_dir).grid(row=1, column=2)

        # Processing options
        options_frame = Frame(self.master)
        options_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        Label(options_frame, text="Processing Options:").grid(row=0, column=0, sticky="w", columnspan=3)

        Label(options_frame, text="Window Size (m):").grid(row=1, column=0, sticky='w')
        self.window_size_entry = Entry(options_frame, width=10)
        self.window_size_entry.grid(row=1, column=1, sticky='w')

        Label(options_frame, text="Band Number:").grid(row=2, column=0, sticky='w')
        self.band_number_entry = Entry(options_frame, width=10)
        self.band_number_entry.grid(row=2, column=1, sticky='w')

        Label(options_frame, text="High Value Threshold:").grid(row=3, column=0, sticky='w')
        self.high_value_threshold_entry = Entry(options_frame, width=10)
        self.high_value_threshold_entry.grid(row=3, column=1, sticky='w')

        Button(self.master, text="Start Processing", command=self.start_processing).grid(row=3, column=0, pady=20, sticky="ew")

        # Image display label and description
        self.image_frame = Frame(self.master)
        self.image_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)
        self.master.grid_rowconfigure(4, weight=3)
        Label(self.image_frame, text="Processed Image (Pseudocolored for Visualization):", font=("Helvetica", 10)).grid(
            row=0, column=0, sticky="w")
        self.image_label = Label(self.image_frame, borderwidth=2, relief="groove")
        self.image_label.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.image_frame.grid_columnconfigure(0, weight=1)  # Ensure the image frame takes up full width

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

        # Use defaults if fields are empty and handle input conversion
        try:
            window_size = float(self.window_size_entry.get()) if self.window_size_entry.get() else 1.0
            if window_size <= 0:
                raise ValueError("Window size must be a positive number.")
        except ValueError:
            messagebox.showerror("Input Error", "Window size must be a positive number.")
            return

        try:
            band_number = int(self.band_number_entry.get()) if self.band_number_entry.get() else 1
            if band_number <= 0:
                raise ValueError("Band number must be a positive integer.")
        except ValueError:
            messagebox.showerror("Input Error", "Band number must be a positive integer.")
            return

        try:
            high_value_threshold = float(
                self.high_value_threshold_entry.get()) if self.high_value_threshold_entry.get() else 1.0
            if high_value_threshold <= 0:
                raise ValueError("High value threshold must be a positive number.")
        except ValueError:
            messagebox.showerror("Input Error", "High value threshold must be a positive number.")
            return

        try:
            driver = ApplicationDriver(input_path, output_dir, window_size, band_number, high_value_threshold)
            driver.run()
            processed_image = driver.get_processed_image()  # Retrieve the image directly from the driver
            if processed_image:
                self.display_image(processed_image)  # Pass the PIL Image directly to display_image
            else:
                messagebox.showerror("Display Error", "No image is available to display.")
            messagebox.showinfo("Success", "Processing completed successfully.")
        except FileNotFoundError as e:
            messagebox.showerror("File Not Found", str(e))
        except ValueError as e:
            messagebox.showerror("Value Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_image(self, image):
        """Display the given PIL Image in the GUI, resized to fit the label."""
        try:
            self.processed_image = image  # Directly use the PIL image passed to the function
            self.resize_and_display_image()  # Call to resize and display the image appropriately
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display image: {str(e)}")

    def resize_and_display_image(self):
        """Resize and display the image to fully utilize the label dimensions while maintaining aspect ratio."""
        if self.processed_image:
            label_width = self.image_label.winfo_width()
            label_height = self.image_label.winfo_height()
            original_width, original_height = self.processed_image.size
            ratio = min(label_width / original_width, label_height / original_height)
            new_size = (int(original_width * ratio), int(original_height * ratio))
            resized_image = self.processed_image.resize(new_size, Image.Resampling.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(resized_image)  # Convert PIL image to PhotoImage
            self.image_label.config(image=self.photo_image)
            self.image_label.image = self.photo_image  # Keep a reference to avoid garbage collection

    def on_window_resize(self, event):
        """Handle the window resize event."""
        if self.processed_image:  # Check if there's an image to resize
            self.resize_and_display_image()

    def adjust_image_label_height(self, event):
        """Adjust the height of the image label to maintain a 16:9 aspect ratio based on the frame's width."""
        # Get the current width of the image frame
        current_width = self.image_frame.winfo_width()
        # Calculate the height to maintain a 16:9 aspect ratio
        new_height = int(current_width * 9 / 16)
        # Set the minimum height to avoid too small values when minimizing the window
        new_height = max(new_height, 100)  # For example, minimum height could be 100 pixels
        # Configure the row of the image label to use the calculated height
        self.image_frame.grid_rowconfigure(1, minsize=new_height)


def main():
    root = tk.Tk()
    app = ApplicationGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()