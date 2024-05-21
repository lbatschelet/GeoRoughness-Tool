"""
gui_main.py
-----------
Version: 1.3.0
Author: Lukas Batschelet
Date: 14.05.2024
-----------
This module contains the main GUI class for the Surface Roughness Calculator application.
"""

import logging
import tkinter as tk
from tkinter import messagebox, filedialog

import customtkinter as ctk
import rasterio
from PIL import Image
from customtkinter import CTkScrollableFrame

from .classes.application_driver import ApplicationDriver
from .classes.processing_parameters import ProcessingParameters
from .classes.threshold_optimizer import ThresholdOptimizer
from .gui.defaults import DEFAULTS
from .gui.footer_frame import FooterFrame
from .gui.header_frame import HeaderFrame
from .gui.parameter_input import ParameterFrame
from .gui.path_frame import PathFrame
from .gui.preview_image import PreviewImage

logger = logging.getLogger(__name__)


class GUIMain(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.driver = None
        self.title("GeoRoughness Tool")
        self.show_advanced_options = False

        self.preview_image = None

        # Create Font objects
        self.fonts = {
            "h1": ctk.CTkFont(size=24, weight="bold"),
            "h2": ctk.CTkFont(size=18, weight="bold"),
            "h3": ctk.CTkFont(size=14, weight="bold"),
            "body": ctk.CTkFont(size=13),
            "small": ctk.CTkFont(size=10),
            "tiny": ctk.CTkFont(size=8),
            "monospace": ctk.CTkFont(family="Courier New", size=12)
        }

        # Get screen width and height
        screen_width = int(0.5 * self.winfo_screenwidth())
        screen_height = int(0.5 * self.winfo_screenheight())

        # Set window size to screen size
        self.geometry(f"{screen_width}x{screen_height}")

        # Create a ScrolledFrame
        self.scrolled_frame = CTkScrollableFrame(self)
        self.scrolled_frame.pack(fill="both", expand=True)

        # Make the GUI responsive
        self.scrolled_frame.grid_columnconfigure(0, weight=1)
        self.scrolled_frame.grid_rowconfigure([0, 1, 2, 3, 4, 5], weight=1)

        self.header_frame = HeaderFrame(self.scrolled_frame, self)
        self.header_frame.grid(row=0,
                               column=0,
                               sticky="nsew")

        self.path_frame = PathFrame(self.scrolled_frame, self)
        self.path_frame.grid(row=1,
                             column=0,
                             sticky="nsew")

        self.parameter_frame = ParameterFrame(self.scrolled_frame, self)
        self.parameter_frame.grid(row=2,
                                  column=0,
                                  sticky="nsew")

        self.preview_frame = PreviewImage(self.scrolled_frame, self, self.preview_image)
        self.preview_frame.grid(row=3,
                                column=0,
                                padx=DEFAULTS.PADX,
                                pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5),
                                sticky="nsew")

        self.footer_frame = FooterFrame(self.scrolled_frame, self)
        self.footer_frame.grid(row=4,
                               column=0,
                               sticky="nsew")

    def toggle_advanced_options(self):
        self.show_advanced_options = not self.show_advanced_options
        self.parameter_frame.toggle_advanced_options(self.show_advanced_options)
        self.path_frame.toggle_advanced_options(self.show_advanced_options)

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
            path_params = self.path_frame.get_parameters()
            parameter_params = self.parameter_frame.get_parameters()

            # Merge the two dictionaries
            params_dict = {**path_params, **parameter_params}

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
                if 'category_thresholds' in filtered_params:
                    self.parameter_frame.analyze_and_optimize_button.configure(state=tk.NORMAL)
                if 'output_dir' not in filtered_params:
                    self.parameter_frame.save_file_button.configure(state=tk.NORMAL)
            else:
                messagebox.showerror("Display Error", "No preview available.")

            messagebox.showinfo("Success", "Processing completed successfully.")

        except FileNotFoundError as e:
            messagebox.showerror("File Not Found", str(e))
        except ValueError as e:
            messagebox.showerror("Value Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def display_preview(self, preview: Image) -> None:
        """
        Displays the preview image in the GUI.

        Args:
            preview: The preview image to display.
        """
        self.preview_frame.display_preview(preview)

    def save_image(self) -> None:
        """
        Opens a file dialog to select the location to save the processed image.

        This method opens a file dialog that filters for TIFF files. If a location is selected,
        the processed data is saved to this location.

        Raises:
            RuntimeError: If there's an error opening the file dialog or saving the processed data.
        """
        try:
            # Generate a default filename using the create_output_filename method
            default_filename = ApplicationDriver.create_output_filename(self.driver.params, include_path=False)

            # Open a file dialog that filters for TIFF files
            output_path = filedialog.asksaveasfilename(initialfile=default_filename,
                                                       filetypes=[("TIFF files", "*.tif")])

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

    def calculate_quality(self):
        # Gather parameters from the GUI
        parameter_params = self.parameter_frame.get_parameters()
        control_input_path = parameter_params['control_input_path']

        # Load the manual data from the control_input_path
        with rasterio.open(control_input_path) as src:
            manual_data = src.read(1)

        # Get the categorized calculated data from the driver
        categorized_calculated_data = self.driver.processed_data

        # Calculate the number of categories
        parameter_params = self.parameter_frame.get_parameters()
        thresholds = [float(x) for x in parameter_params['category_thresholds'].split(',')]

        # Call the calculate_quality method and return the result
        quality = ThresholdOptimizer.calculate_quality(
            manual_data, categorized_calculated_data, thresholds)

        quality_string = "{:.2f}".format(quality * 100)

        # Update the quality label in the parameter frame
        self.parameter_frame.analyze_and_optimize_frame.calculate_quality_frame.update_label(quality_string)

        return quality

    def optimize_thresholds(self):
        try:
            # Gather parameters from the GUI
            parameter_params = self.parameter_frame.get_parameters()
            control_input_path = parameter_params['control_input_path']
            category_thresholds = parameter_params['category_thresholds']

            # Convert category_thresholds to a list of floats if it's a string
            if isinstance(category_thresholds, str):
                category_thresholds = [float(x) for x in category_thresholds.split(',')]

            # Load the manual data from the control_input_path
            with rasterio.open(control_input_path) as src:
                manual_data = src.read(1)

            # Ensure manual_data and category_thresholds are not empty
            if manual_data.size == 0:
                raise ValueError("Loaded manual data is empty.")
            if len(category_thresholds) < 1:
                raise ValueError("Category thresholds are not properly defined.")

            # Get the uncategorized calculated data from the driver
            uncategorized_calculated_data = self.driver.processed_uncategorized_data

            # Call the calculate_optimized_thresholds method and get the result
            optimized_thresholds = ThresholdOptimizer.calculate_optimized_thresholds(
                manual_data, uncategorized_calculated_data, (len(category_thresholds) + 1))

            optimized_thresholds_string = ", ".join("{:.3f}".format(threshold) for threshold in optimized_thresholds)
            self.parameter_frame.analyze_and_optimize_frame.optimize_thresholds_frame.update_label(
                optimized_thresholds_string)

            return optimized_thresholds

        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None


def main():
    GUIMain().mainloop()


if __name__ == "__main__":
    GUIMain().mainloop()
