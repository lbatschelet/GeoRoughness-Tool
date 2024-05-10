import webbrowser

import customtkinter as ctk

from roughness_calculator.gui.defaults import DEFAULTS


class FooterFrame(ctk.CTkFrame):
    def __init__(self, parent, main_gui, **kwargs):
        super().__init__(parent, **kwargs)
        self.main_gui = main_gui

        # Configure the grid
        self.grid_rowconfigure([0, 1], weight=1)
        self.grid_columnconfigure([0, 1, 2, 3], weight=1)

        # Create buttons in the upper row
        self.help_button = WebsiteButton(self, "https://github.com/lbatschelet/dem-roughness-calculator", text="Help")
        self.help_button.grid(row=0, column=0, padx=(DEFAULTS.PADX, DEFAULTS.PADX * 0.5), pady=(DEFAULTS.PADY, DEFAULTS.PADY * 0.5), sticky="nsew")

        self.button2 = ctk.CTkButton(self, text="Button 2")
        self.button2.grid(row=0, column=1, padx=(DEFAULTS.PADX * 0.5, DEFAULTS.PADX * 0.5), pady=(DEFAULTS.PADY, DEFAULTS.PADY * 0.5), sticky="nsew")

        self.button3 = ctk.CTkButton(self, text="Button 3")
        self.button3.grid(row=0, column=2, padx=(DEFAULTS.PADX * 0.5, DEFAULTS.PADX * 0.5), pady=(DEFAULTS.PADY, DEFAULTS.PADY * 0.5), sticky="nsew")

        self.button4 = ctk.CTkButton(self, text="Button 4")
        self.button4.grid(row=0, column=3, padx=(DEFAULTS.PADX * 0.5, DEFAULTS.PADX), pady=(DEFAULTS.PADY, DEFAULTS.PADY * 0.5), sticky="nsew")

        # Create a label in the lower row
        self.info_label = ctk.CTkLabel(self, text="Surface Roughness Calculator - © 2024 L. Batschelet, F. Mohaupt, S. Röthlisberger. Licensed under the MIT License.", font=self.main_gui.fonts['small'])
        self.info_label.grid(row=1, column=0, columnspan=4, padx=DEFAULTS.PADX, pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY), sticky="nsew")


class WebsiteButton(ctk.CTkButton):
    def __init__(self, parent, url, **kwargs):
        super().__init__(parent, command=self.open_website, **kwargs)
        self.url = url

    def open_website(self):
        webbrowser.open(self.url)