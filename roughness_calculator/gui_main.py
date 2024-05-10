"""
gui_main.py
-----------
Version: 1.2.0
Author: Lukas Batschelet
Date: 11.05.2024
-----------
This module contains the main GUI class for the Surface Roughness Calculator application.
"""

import logging
import tkinter as tk
from tkinter import messagebox, filedialog

import customtkinter as ctk
from PIL import Image
from customtkinter import CTkScrollableFrame

from roughness_calculator.classes.application_driver import ApplicationDriver
from roughness_calculator.classes.processing_parameters import ProcessingParameters
from roughness_calculator.gui.defaults import DEFAULTS
from roughness_calculator.gui.encapsulating_frame import EncapsulatingFrame
from roughness_calculator.gui.footer_frame import FooterFrame
from roughness_calculator.gui.header_frame import HeaderFrame
from roughness_calculator.gui.parameter_input import ParameterFrame
from roughness_calculator.gui.path_frame import PathFrame
from roughness_calculator.gui.preview_image import PreviewImage

logger = logging.getLogger(__name__)


class GUIMain(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.driver = None
        self.title("Surface Roughness Calculator")

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
        self.scrolled_frame.grid_rowconfigure([0, 1, 2, 3], weight=1)

        self.header_frame = EncapsulatingFrame(self.scrolled_frame, HeaderFrame, self)
        self.header_frame.grid(row=0,
                               column=0,
                               padx=DEFAULTS.PADX,
                               pady=(DEFAULTS.PADY, DEFAULTS.PADY * 0.5),
                               sticky="nsew")

        self.path_frame = EncapsulatingFrame(self.scrolled_frame, PathFrame, self)
        self.path_frame.grid(row=1,
                             column=0,
                             padx=DEFAULTS.PADX,
                             pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5),
                             sticky="nsew")

        self.parameter_frame = EncapsulatingFrame(self.scrolled_frame, ParameterFrame, self)
        self.parameter_frame.grid(row=2,
                                  column=0,
                                  padx=DEFAULTS.PADX,
                                  pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5),
                                  sticky="nsew")

        self.preview_frame = EncapsulatingFrame(self.scrolled_frame, PreviewImage, self, self.preview_image)
        self.preview_frame.grid(row=3,
                                column=0,
                                padx=DEFAULTS.PADX,
                                pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5),
                                sticky="nsew")

        self.footer_frame = EncapsulatingFrame(self.scrolled_frame, FooterFrame, self)
        self.footer_frame.grid(row=4,
                               column=0,
                               padx=DEFAULTS.PADX,
                               pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY),
                               sticky="nsew")

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
                if 'output_dir' not in filtered_params:
                    self.parameter_frame.child_frame.save_file_button.configure(state=tk.NORMAL)
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
        self.preview_frame.child_frame.display_preview(preview)

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


def main():
    GUIMain().mainloop()


if __name__ == "__main__":
    GUIMain().mainloop()
