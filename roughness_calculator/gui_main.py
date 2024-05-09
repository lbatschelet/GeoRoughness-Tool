"""
gui_main.py
-----------
Version: 1.1.0
Author: Lukas Batschelet
Date: 09.05.2024
-----------
This module contains the ApplicationGUI class which is
responsible for creating the graphical user interface (GUI) of the application.
"""
from PIL import Image, ImageTk

from roughness_calculator.classes.application_driver import ApplicationDriver

import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button, Entry, Frame
import logging

from roughness_calculator.classes.processing_parameters import ProcessingParameters
from .log_config import setup_logging

# Ensure the logger is set up (optional if you know `log_config.py` is already imported elsewhere)
setup_logging()

logger = logging.getLogger(__name__)


class ApplicationGUI:
    def __init__(self, master: tk.Tk) -> None:
        """
        Initializes the graphical user interface for the application.

        This method sets up the main window and its components.

        Args:
            master (tk.Tk): The root window.

        Raises:
            RuntimeError: If there's an error setting up the GUI.
        """
        try:
            self.master = master
            self.master.title("Surface Roughness Calculator")

            # Set initial geometry based on screen size and make it resizable
            # Get screen dimensions
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()

            # Calculate window dimensions as a fraction of screen dimensions
            window_width = int(screen_width * 0.5)  # Adjust width as needed
            window_height = int(screen_height * 1.0)

            # Set the geometry of the window
            self.master.geometry(f"{window_width}x{window_height}")

            # Setup GUI components
            self.setup_gui()

            # Bind the window resize event to adjust the image label height dynamically
            self.master.bind("<Configure>", self.adjust_image_label_height)
        except Exception as e:
            # Log the error and raise the original exception
            logging.error("Error setting up the GUI: " + str(e))
            raise RuntimeError("Error setting up the GUI: " + str(e))

    def setup_gui(self) -> None:
        """
        Sets up the GUI components in the main application window.

        This method configures the main window and initializes all the GUI components such as
        frames, labels, entries, and buttons.

        Raises:
            RuntimeError: If there's an error setting up the GUI.
        """
        try:
            # Ensure that all main GUI components fill the window and expand as needed
            self.master.grid_columnconfigure(0, weight=1)

            # Header with description
            header_frame = Frame(self.master)
            header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
            header_frame.grid_columnconfigure(0, weight=1)
            Label(header_frame, text="DEM Surface Roughness Calculator",
                  font=("Helvetica", 16, "bold"), anchor='w').grid(row=0, column=0, sticky="ew")
            Label(header_frame, text="Adjust the settings below and load your GeoTIFF files to begin processing.",
                  font=("Helvetica"), anchor='w').grid(row=1, column=0, sticky="ew")

            # Input and Output configuration
            config_frame = Frame(self.master)
            config_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
            config_frame.grid_columnconfigure(1, weight=1)

            # Input field
            Label(config_frame, text="Input TIFF Path:").grid(row=0, column=0, sticky='w')
            self.input_path_entry = Entry(config_frame)
            self.input_path_entry.grid(row=0, column=1, sticky="ew")
            Button(config_frame, text="Browse", command=self.load_input).grid(row=0, column=2)

            # Empty label for spacing
            Label(config_frame, text="").grid(row=1, column=0)

            # Output field
            Label(config_frame, text="Output Directory:").grid(row=2, column=0, sticky='w')
            self.output_dir_entry = Entry(config_frame)
            self.output_dir_entry.grid(row=2, column=1, sticky="ew")
            Button(config_frame, text="Browse", command=self.set_output_dir).grid(row=2, column=2)

            # Detailed description for the Output field
            Label(config_frame, text="Output is optional. If you want to save the file only after seeing a preview, "
                                     "leave this field empty.",
                  font=("Helvetica")).grid(row=3, column=1, columnspan=3, sticky='w')

            # Empty label for spacing
            Label(config_frame, text="").grid(row=1, column=0)

            # Processing options
            options_frame = Frame(self.master)
            options_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
            (Label(options_frame,text="Further Processing Options are all optional and use default values "
                                      "if not defined by the user.").grid(row=0, column=0, sticky="w", columnspan=3))

            # window_size
            Label(options_frame, text="Window Size (m): (Default is 1.0 meter)").grid(row=1, column=0, sticky='e')
            self.window_size_entry = Entry(options_frame, width=15)
            self.window_size_entry.grid(row=1, column=1, sticky='w')

            # band_number
            (Label(options_frame, text="Band Number: (Default is 1, only in rare cases different)").
             grid(row=2, column=0, sticky='e'))
            self.band_number_entry = Entry(options_frame, width=15)
            self.band_number_entry.grid(row=2, column=1, sticky='e')

            # high_value_threshold
            (Label(options_frame, text="High Value Threshold: (Default is 10.0, used to cut off crazy values at file borders)").
             grid(row=3, column=0, sticky='e'))
            self.high_value_threshold_entry = Entry(options_frame, width=15)
            self.high_value_threshold_entry.grid(row=3, column=1, sticky='e')

            # category_thresholds
            (Label(options_frame, text="category Thresholds (comma-separated): (Default is None)").
             grid(row=4, column=0, sticky='e'))
            self.category_thresholds_entry = Entry(options_frame, width=15)
            self.category_thresholds_entry.grid(row=4, column=1, sticky='e')

            Button(self.master, text="Start Processing", command=self.start_processing).grid(row=3, column=0,
                                                                                             pady=20, sticky="ew")

            # Image display label and description
            self.image_frame = Frame(self.master)
            self.image_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)
            self.master.grid_rowconfigure(4, weight=3)
            Label(self.image_frame, text="Processed Image (Pseudo-colored for Visualization):",
                  font=("Helvetica", 10)).grid(
                row=0, column=0, sticky="w")
            self.image_label = Label(self.image_frame, borderwidth=2, relief="groove")
            self.image_label.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
            self.image_frame.grid_columnconfigure(0, weight=1)  # Ensure the image frame takes up full width

            # Create a frame for the buttons
            button_frame = Frame(self.master)
            button_frame.grid(row=5, column=0, pady=20, sticky="ew")

            # Now place buttons inside this frame
            self.help_button = Button(button_frame, text="Help", command=self.show_help)
            self.help_button.grid(row=0, column=0, padx=5, sticky="ew")

            self.save_button = Button(button_frame, text="Save Processed Image", command=self.save_image,
                                      state='disabled')
            self.save_button.grid(row=0, column=1, padx=5, sticky="ew")

            # Configure the button frame column weights if necessary
            button_frame.grid_columnconfigure(0, weight=1)
            button_frame.grid_columnconfigure(1, weight=1)
        except Exception as e:
            # Log the error and raise the original exception
            logging.error("Error setting up the GUI: " + str(e))
            raise RuntimeError("Error setting up the GUI: " + str(e))

    def load_input(self) -> None:
        """
        Opens a file dialog to select the input GeoTIFF file.

        This method opens a file dialog that filters for TIFF files. If a file is selected, its path is inserted
        into the input path entry field.

        Raises:
            RuntimeError: If there's an error opening the file dialog or setting the input path.
        """
        try:
            # Open a file dialog that filters for TIFF files
            filename = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tif *.tiff")])

            # If a file is selected (i.e., the filename is not an empty string)
            if filename:
                # Clear the input path entry field
                self.input_path_entry.delete(0, tk.END)

                # Insert the selected file's path into the input path entry field
                self.input_path_entry.insert(0, filename)
        except Exception as e:
            # Log the error and raise the original exception
            logging.error("Error loading input file: " + str(e))
            raise RuntimeError("Error loading input file: " + str(e))

    def set_output_dir(self) -> None:
        """
        Opens a directory dialog to select the output directory.

        This method opens a directory dialog. If a directory is selected, its path is
        inserted into the output directory entry field.

        Raises:
            RuntimeError: If there's an error opening the directory dialog or setting the output directory.
        """
        try:
            # Open a directory dialog
            directory = filedialog.askdirectory()

            # If a directory is selected (i.e., the directory is not an empty string)
            if directory:
                # Clear the output directory entry field
                self.output_dir_entry.delete(0, tk.END)

                # Insert the selected directory's path into the output directory entry field
                self.output_dir_entry.insert(0, directory)
        except Exception as e:
            # Log the error and raise the original exception
            logging.error("Error setting output directory: " + str(e))
            raise RuntimeError("Error setting output directory: " + str(e))

    def start_processing(self) -> None:
        """
        Starts the processing of the GeoTIFF file with the provided parameters.

        This method gathers the parameters from the GUI, creates an instance of the ProcessingParameters class,
        initializes the ApplicationDriver with these parameters, and manages the processing flow,
        including displaying results and handling errors.

        Raises:
            FileNotFoundError: If the input file is not found.
            ValueError: If an invalid value is provided for a parameter.
            RuntimeError: If there's an error during processing.
        """
        try:
            # Gather parameters from the GUI
            params_dict = {
                "input_path": self.input_path_entry.get() or None,
                "output_dir": self.output_dir_entry.get() or None,
                "window_size": self.window_size_entry.get() or None,
                "band_number": self.band_number_entry.get() or None,
                "high_value_threshold": self.high_value_threshold_entry.get() or None,
                "category_thresholds": self.category_thresholds_entry.get() or None
            }

            # Filter out None values to allow optional parameters to use defaults
            filtered_params = {k: v for k, v in params_dict.items() if v is not None}

            # Create ProcessingParameters instance using the factory method
            processing_params = ProcessingParameters.create_from_dict(filtered_params)

            # Initialize and run the application driver with the validated and converted parameters
            self.driver = ApplicationDriver(processing_params)
            self.driver.run()

            # Get the preview of the processed data
            preview = self.driver.get_preview()
            if preview:
                self.display_preview(preview)
                if 'output_dir' not in filtered_params:
                    self.save_button.config(state='normal')
            else:
                messagebox.showerror("Display Error", "No preview available.")

            messagebox.showinfo("Success", "Processing completed successfully.")

        except FileNotFoundError as e:
            messagebox.showerror("File Not Found", str(e))
        except ValueError as e:
            messagebox.showerror("Value Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def save_image(self) -> None:
        """
        Opens a file dialog to select the location to save the processed image.

        This method opens a file dialog that filters for TIFF files. If a location is selected,
        the processed data is saved to this location.

        Raises:
            RuntimeError: If there's an error opening the file dialog or saving the processed data.
        """
        try:
            # Open a file dialog that filters for TIFF files
            output_path = filedialog.asksaveasfilename(filetypes=[("TIFF files", "*.tif")])

            # If a location is selected (i.e., the output_path is not an empty string)
            if output_path:
                # Save the processed data to the selected location
                self.driver.save_processed_data(output_path)

                # Show a success message
                messagebox.showinfo("Success", "Image saved successfully.")
        except Exception as e:
            # Log the error and raise the original exception
            logging.error("Error saving image: " + str(e))
            raise RuntimeError("Error saving image: " + str(e))

    def display_preview(self, image: Image) -> None:
        """
        Displays the given PIL Image in the GUI, resized to fit the label.

        This method takes a PIL Image, resizes it to fit the label, and displays it in the GUI.

        Args:
            image (Image): The PIL Image to be displayed.

        Raises:
            RuntimeError: If there's an error displaying the image.
        """
        try:
            # Directly use the PIL image passed to the function
            self.preview = image

            # Call to resize and display the image appropriately
            self.resize_and_display_image()
        except Exception as e:
            # Log the error and raise the original exception
            logging.error("Error displaying preview: " + str(e))
            raise RuntimeError("Error displaying preview: " + str(e))

    def resize_and_display_image(self) -> None:
        """
        Resize and display the image to fully utilize the label dimensions while
        maintaining aspect ratio and pixel integrity.

        This method checks if a preview image is available. If available, it retrieves the
        dimensions of the image and the label, calculates the ratio to maintain the aspect
        ratio, resizes the image, and displays it in the label.

        Raises:
            RuntimeError: If there's an error resizing or displaying the image.
        """
        try:
            # Check if there's an image to resize
            if self.preview:
                # Get the current dimensions of the label and the image
                label_width = self.image_label.winfo_width()
                label_height = self.image_label.winfo_height()
                original_width, original_height = self.preview.size

                # Log the dimensions to help with debugging
                logging.debug(
                    f"Label dimensions: {label_width}x{label_height}, "
                    f"Image dimensions: {original_width}x{original_height}")

                # Calculate the ratio to maintain the aspect ratio
                ratio = min(label_width / original_width, label_height / original_height)
                new_size = (int(original_width * ratio), int(original_height * ratio))

                logging.debug(f"Resizing image to: {new_size} using nearest neighbor interpolation.")

                # Resize with nearest neighbor interpolation to avoid altering pixel values
                resized_image = self.preview.resize(new_size, Image.Resampling.NEAREST)
                self.photo_image = ImageTk.PhotoImage(resized_image)  # Convert PIL image to PhotoImage

                # Display the resized image in the label
                self.image_label.config(image=self.photo_image)
                self.image_label.image = self.photo_image  # Keep a reference to avoid garbage collection
        except Exception as e:
            # Log the error and raise the original exception
            logging.error("Error resizing or displaying image: " + str(e))
            raise RuntimeError("Error resizing or displaying image: " + str(e))

    def on_window_resize(self, event: tk.Event) -> None:
        """
        Handles the window resize event.

        This method is triggered when the window is resized. If a preview image is available,
        it calls the method to resize and display the image.

        Args:
            event (tk.Event): The event information.

        Raises:
            RuntimeError: If there's an error resizing or displaying the image.
        """
        try:
            # Log the window resize event
            logging.debug("Window resized, adjusting preview image...")

            # Check if there's an image to resize
            if self.preview:
                # Call the method to resize and display the image
                self.resize_and_display_image()
        except Exception as e:
            # Log the error and raise the original exception
            logging.error("Error resizing or displaying image: " + str(e))
            raise RuntimeError("Error resizing or displaying image: " + str(e))

    def adjust_image_label_height(self, event: tk.Event) -> None:
        """
        Adjusts the height of the image label to maintain a 16:9 aspect ratio based on the frame's width.

        This method is triggered when the window is resized. It calculates the new height based
        on the current width of the image frame and a 16:9 aspect ratio. It then sets the minimum height
        to avoid too small values when minimizing the window and configures the row of
        the image label to use the calculated height.

        Args:
            event (tk.Event): The event information.

        Raises:
            RuntimeError: If there's an error adjusting the image label height.
        """
        try:
            # Get the current width of the image frame
            current_width = self.image_frame.winfo_width()

            # Calculate the height to maintain a 16:9 aspect ratio
            new_height = int(current_width * 9 / 16)

            # Set the minimum height to avoid too small values when minimizing the window
            new_height = max(new_height, 100)  # For example, minimum height could be 100 pixels

            # Configure the row of the image label to use the calculated height
            self.image_frame.grid_rowconfigure(1, minsize=new_height)
        except Exception as e:
            # Log the error and raise the original exception
            logging.error("Error adjusting image label height: " + str(e))
            raise RuntimeError("Error adjusting image label height: " + str(e))

    def show_help(self):
        help_text = """
        DEM Roughness Calculator Help:


        Input TIFF Path:
        Path to the input GeoTIFF file.
        
        
        Output Directory:
        Directory where the output files will be saved.
        (Optional, if not set you can choose to save the processed image after previewing it.)

        Window Size (m):
        Defines the size of the square window in meters to calculate roughness. 
        (Optional, default is 1.0)
        
        
        Band Number:
        Specifies the band of the GeoTIFF to be processed.
        (Optional, default is 1, only different in rare cases where the GeoTIFF has multiple bands including a DEM)
        
        
        High Value Threshold:
        Sets the threshold above which values are considered as noise and set to nodata.
        (Optional, default is 1.0, should often be lower, rarely higher)
        
        
        category Thresholds:
        Comma-separated thresholds for categorizing the roughness values.
        (Optional, default is None. Grouping roughness values into categories can help in visualizing the data.)


        For more detailed information, visit the GitHub wiki at:
        https://github.com/lbatschelet/dem-roughness-calculator/wiki
        """
        messagebox.showinfo("Help", help_text)


def main():
    root = tk.Tk()
    app = ApplicationGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
