import tkinter as tk

import customtkinter as ctk

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
                           "Window size",
                           "The size of the window to use for processing. Defaults to 1.0.",
                           self.main_gui))
        self.window_size_field.grid(row=0,
                                    column=0,
                                    padx=(DEFAULTS.PADX, DEFAULTS.PADX * 0.5),
                                    pady=(DEFAULTS.PADY, DEFAULTS.PADY * 0.5),
                                    sticky="nsew")

        self.category_thresholds_field = (
            ParameterInput(self,
                           "Category Thresholds",
                           "List of thresholds for categorizing data. "
                           "First category starts from first value. (Optional)",
                           self.main_gui))
        self.category_thresholds_field.grid(row=0,
                                            column=1,
                                            padx=(DEFAULTS.PADX * 0.5, DEFAULTS.PADX),
                                            pady=(DEFAULTS.PADY, DEFAULTS.PADY * 0.5),
                                            sticky="nsew")

        self.band_number_field = (
            ParameterInput(self,
                           "Band Number",
                           "The band number to use for processing. Defaults to 1.",
                           self.main_gui))
        self.band_number_field.grid(row=1,
                                    column=0,
                                    padx=(DEFAULTS.PADX, DEFAULTS.PADX * 0.5),
                                    pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5),
                                    sticky="nsew")

        self.high_value_threshold_field = (
            ParameterInput(self,
                           "High value threshold",
                           "Used to filter out high values at the borders of the data. Defaults to 10.",
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
                               pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY),
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

        # Create a new button
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

        # Create a new frame and initially hide it
        self.analyze_and_optimize_frame = AnalyzeAndOptimizeFrame(self, main_gui)
        self.analyze_and_optimize_frame.grid(row=3,
                                             column=0,
                                             columnspan=3,
                                             padx=DEFAULTS.PADX,
                                             pady=(0, DEFAULTS.PADY),
                                             sticky="ew")
        self.analyze_and_optimize_frame.grid_remove()

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


class DescriptionField(ctk.CTkLabel):
    def __init__(self, parent, text, **kwargs):
        super().__init__(parent, text=text, **kwargs)


class ParameterInput(ctk.CTkFrame):
    def __init__(self, parent, name, description, main_gui, **kwargs):
        super().__init__(parent, **kwargs)
        self.main_gui = main_gui
        self.grid_columnconfigure([0, 1], weight=1)

        self.name_label = ctk.CTkLabel(self, text=name, font=self.main_gui.fonts['h3'])
        self.name_label.grid(row=0,
                             column=0,
                             padx=(DEFAULTS.PADX, DEFAULTS.PADX * 0.25),
                             pady=DEFAULTS.PADY,
                             sticky="w")

        self.description_button = ctk.CTkButton(self, text="Description", command=self.show_description)
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

        self.description_field = DescriptionField(self, description)
        self.description_field.grid(row=2,
                                    column=0,
                                    columnspan=2,
                                    padx=(DEFAULTS.PADX, DEFAULTS.PADX),
                                    pady=(0, DEFAULTS.PADY),
                                    sticky="w")
        self.description_field.grid_remove()

    def show_description(self):
        if self.description_field.winfo_viewable():
            self.description_field.grid_remove()
        else:
            self.description_field.grid()

    def get(self):
        return self.entry.get()
