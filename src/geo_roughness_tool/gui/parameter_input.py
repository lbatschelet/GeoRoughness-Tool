import tkinter as tk
import customtkinter as ctk
import webbrowser

from .analyze_and_optimize import AnalyzeAndOptimizeFrame
from .defaults import DEFAULTS

class ParameterFrame(ctk.CTkFrame):
    def __init__(self, parent, main_gui, **kwargs):
        super().__init__(parent, **kwargs)

        self.main_gui = main_gui

        # Make the GUI responsive
        self.grid_columnconfigure([0, 1], weight=1)
        self.grid_rowconfigure([0, 1], weight=1)

        self.window_size_field = (
            ParameterInput(self,
                           "Window Size (meters)",
                           "https://github.com/lbatschelet/GeoRoughness-Tool/wiki/Parameter-Explanation#window-size-meters",
                           self.main_gui))
        self.window_size_field.grid(row=0,
                                    column=0,
                                    padx=(DEFAULTS.PADX, DEFAULTS.PADX * 0.5),
                                    pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5),
                                    sticky="nsew")

        self.category_thresholds_field = (
            ParameterInput(self,
                           "Categorical Thresholds",
                           "https://github.com/lbatschelet/GeoRoughness-Tool/wiki/Parameter-Explanation#categorical-thresholds",
                           self.main_gui))
        self.category_thresholds_field.grid(row=0,
                                            column=1,
                                            padx=(DEFAULTS.PADX * 0.5, DEFAULTS.PADX),
                                            pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5),
                                            sticky="nsew")

        self.band_number_field = (
            ParameterInput(self,
                           "Band Number",
                           "https://github.com/lbatschelet/GeoRoughness-Tool/wiki/Parameter-Explanation#band-number",
                           self.main_gui))
        self.band_number_field.grid(row=1,
                                    column=0,
                                    padx=(DEFAULTS.PADX, DEFAULTS.PADX * 0.5),
                                    pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5),
                                    sticky="nsew")

        self.high_value_threshold_field = (
            ParameterInput(self,
                           "High Value Threshold",
                           "https://github.com/lbatschelet/GeoRoughness-Tool/wiki/Parameter-Explanation#high-value-threshold",
                           self.main_gui))
        self.high_value_threshold_field.grid(row=1,
                                             column=1,
                                             padx=(DEFAULTS.PADX * 0.5, DEFAULTS.PADX),
                                             pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5),
                                             sticky="nsew")

        # Create a new frame for the buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2,
                               column=0,
                               columnspan=2,
                               padx=DEFAULTS.PADX,
                               pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5),
                               sticky="ew")
        # Set equal weights for each column in the button frame
        self.button_frame.grid_columnconfigure([0, 1, 2], weight=1)

        self.start_processing_button = (
            ctk.CTkButton(self.button_frame, text="Start Processing", command=self.main_gui.start_processing))
        self.start_processing_button.grid(row=0,
                                          column=0,
                                          padx=(DEFAULTS.PADX, DEFAULTS.PADX * 0.5),
                                          pady=DEFAULTS.PADY,
                                          sticky="ew")

        self.analyze_and_optimize_button = ctk.CTkButton(self.button_frame,
                                                         text="Analyze and optimize...",
                                                         command=self.toggle_frame, state=tk.DISABLED)
        self.analyze_and_optimize_button.grid(row=0,
                                              column=1,
                                              padx=(DEFAULTS.PADX * 0.5, DEFAULTS.PADX * 0.5),
                                              pady=DEFAULTS.PADY,
                                              sticky="ew")

        self.save_file_button = (
            ctk.CTkButton(self.button_frame, text="Save File", command=self.main_gui.save_image, state=tk.DISABLED))
        self.save_file_button.grid(row=0,
                                   column=2,
                                   padx=(DEFAULTS.PADX * 0.5, DEFAULTS.PADX * 0.5),
                                   pady=DEFAULTS.PADY,
                                   sticky="ew")

        # Initially hide advanced options
        self.band_number_field.grid_remove()
        self.high_value_threshold_field.grid_remove()

        # Create a new frame and initially hide it
        self.analyze_and_optimize_frame = AnalyzeAndOptimizeFrame(self, main_gui)
        self.analyze_and_optimize_frame.grid(row=3,
                                             column=0,
                                             columnspan=3,
                                             padx=DEFAULTS.PADX,
                                             pady=(0, DEFAULTS.PADY),
                                             sticky="ew")
        self.analyze_and_optimize_frame.grid_remove()

    def toggle_advanced_options(self, show):
        if show:
            self.band_number_field.grid()
            self.high_value_threshold_field.grid()
        else:
            self.band_number_field.grid_remove()
            self.high_value_threshold_field.grid_remove()

    def toggle_frame(self):
        if self.analyze_and_optimize_frame.winfo_viewable():
            self.analyze_and_optimize_frame.grid_remove()
        else:
            self.analyze_and_optimize_frame.grid()

    def get_parameters(self):
        return {
            "window_size": self.window_size_field.get() or None,
            "category_thresholds": self.category_thresholds_field.get() or None,
            "band_number": self.band_number_field.get() or None,
            "high_value_threshold": self.high_value_threshold_field.get() or None,
            "control_input_path": self.analyze_and_optimize_frame.control_input_path_field.get() or None
        }


class ParameterInput(ctk.CTkFrame):
    def __init__(self, parent, name, url, main_gui, **kwargs):
        super().__init__(parent, **kwargs)
        self.main_gui = main_gui
        self.url = url
        self.grid_columnconfigure([0, 1], weight=1)

        self.name_label = ctk.CTkLabel(self, text=name, font=self.main_gui.fonts['h3'])
        self.name_label.grid(row=0,
                             column=0,
                             padx=(DEFAULTS.PADX, DEFAULTS.PADX * 0.25),
                             pady=DEFAULTS.PADY,
                             sticky="w")

        self.description_button = ctk.CTkButton(self, text="Description", command=self.open_url)
        self.description_button.grid(row=0,
                                     column=1,
                                     padx=(DEFAULTS.PADX * 0.25, DEFAULTS.PADX),
                                     pady=DEFAULTS.PADY,
                                     sticky="e")

        self.entry = ctk.CTkEntry(self)
        self.entry.grid(row=1,
                        column=0,
                        columnspan=2,
                        padx=(DEFAULTS.PADX, DEFAULTS.PADX),
                        pady=(0, DEFAULTS.PADY),
                        sticky="ew")

    def open_url(self):
        webbrowser.open(self.url)

    def get(self):
        return self.entry.get()
