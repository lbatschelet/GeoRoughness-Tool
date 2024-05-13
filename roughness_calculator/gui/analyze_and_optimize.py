import customtkinter as ctk
import tkinter as tk

from roughness_calculator.gui.defaults import DEFAULTS
from roughness_calculator.gui.path_frame import InputPathField


class AnalyzeAndOptimizeFrame(ctk.CTkFrame):
    def __init__(self, parent, main_gui, **kwargs):
        super().__init__(parent, **kwargs)

        # Set up the extra frame
        self.grid_columnconfigure([0, 1], weight=1)
        self.grid_rowconfigure([0, 1], weight=1)

        # Left column: input file frame
        self.control_input_path_field = InputPathField(self, main_gui, "Control Data")
        self.control_input_path_field.grid(row=0,
                                           column=0,
                                           rowspan=2,
                                           padx=(DEFAULTS.PADX, DEFAULTS.PADX * 0.5),
                                           pady=DEFAULTS.PADY,
                                           sticky="nsew")

        # Right column, upper row: calculate quality button and label
        self.calculate_quality_frame = CalculationFrame(self, "Calculate Quality", main_gui.calculate_quality, label_prefix='Calculated quality of the thresholds: ')
        self.calculate_quality_frame.grid(row=0, column=1, sticky="nsew", padx=(DEFAULTS.PADX* 0.5, DEFAULTS.PADX), pady=(DEFAULTS.PADY, DEFAULTS.PADY * 0.5))

        # Right column, lower row: optimize thresholds button and label
        self.optimize_thresholds_frame = CalculationFrame(self, "Optimize Thresholds", main_gui.optimize_thresholds, label_prefix='Calculated optimized thresholds: ')
        self.optimize_thresholds_frame.grid(row=1, column=1, sticky="nsew", padx=(DEFAULTS.PADX* 0.5, DEFAULTS.PADX), pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY))


class CalculationFrame(ctk.CTkFrame):
    def __init__(self, parent, button_text, command, label_prefix="", **kwargs):
        super().__init__(parent, **kwargs)

        # Configure the columns to expand and contract with the window size
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create the calculation button using CustomTkinter
        self.calculation_button = ctk.CTkButton(self, text=button_text, command=command)
        self.calculation_button.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        # Create the copy button but do not display it initially
        self.copy_button = ctk.CTkButton(self, text="Copy", command=self.copy_to_clipboard)
        self.copy_button.grid(row=0, column=1, sticky="e", padx=10, pady=10)

        # Create the result label using CustomTkinter
        self.label_prefix = label_prefix
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=10)

        # Flag to track if the label has been updated
        self.is_label_updated = False

    def update_label(self, text):
        if not self.is_label_updated:
            self.result_label.configure(text=self.label_prefix + str(text))
            self.show_copy_button()
            self.is_label_updated = True
        else:
            self.result_label.configure(text=self.label_prefix + str(text))

    def copy_to_clipboard(self):
        root = self.winfo_toplevel()  # Get the top-level window containing this frame
        root.clipboard_clear()
        # Only copy the values, not the whole label
        root.clipboard_append(self.result_label.cget("text").replace(self.label_prefix, ""))

    def show_copy_button(self):
        self.copy_button.grid(row=0, column=2, sticky="ew", padx=10, pady=10)
