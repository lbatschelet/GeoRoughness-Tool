import customtkinter as ctk

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
        self.calculate_quality_frame = CalculationFrame(self, "Calculate Quality", main_gui.calculate_quality)
        self.calculate_quality_frame.grid(row=0, column=1, sticky="nsew", padx=(DEFAULTS.PADX* 0.5, DEFAULTS.PADX), pady=(DEFAULTS.PADY, DEFAULTS.PADY * 0.5))

        # Right column, lower row: optimize thresholds button and label
        self.optimize_thresholds_frame = CalculationFrame(self, "Optimize Thresholds", main_gui.optimize_thresholds)
        self.optimize_thresholds_frame.grid(row=1, column=1, sticky="nsew", padx=(DEFAULTS.PADX* 0.5, DEFAULTS.PADX), pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY))



class CalculationFrame(ctk.CTkFrame):
    def __init__(self, parent, button_text, command, **kwargs):
        super().__init__(parent, **kwargs)

        # Create the button
        self.calculation_button = ctk.CTkButton(self, text=button_text, command=command)
        self.calculation_button.grid(row=0, column=0, sticky="ew", padx=DEFAULTS.PADX, pady=DEFAULTS.PADY)

        # Create the label
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.grid(row=0, column=1, sticky="ew", padx=DEFAULTS.PADX, pady=DEFAULTS.PADY)

    def update_label(self, text):
        self.result_label.configure(text=str(text))