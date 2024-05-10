import customtkinter as ctk

from roughness_calculator.gui.defaults import DEFAULTS


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, parent, main_gui, **kwargs):
        super().__init__(parent, **kwargs)

        self.main_gui = main_gui

        self.title_label = ctk.CTkLabel(self, text="Surface Roughness Calculator", font=self.main_gui.fonts['h1'])
        self.title_label.grid(row=0, column=0, padx=DEFAULTS.PADX, pady=(DEFAULTS.PADY, 0), sticky="w")

        self.description_label = ctk.CTkLabel(self, text="This program calculates the surface roughness of a DEM.", font=self.main_gui.fonts['body'])
        self.description_label.grid(row=1, column=0, padx=DEFAULTS.PADX, pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY), sticky="w")