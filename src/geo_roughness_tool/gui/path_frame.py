import abc
import os
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk

from .defaults import DEFAULTS


class PathFrame(ctk.CTkFrame):
    def __init__(self, parent, main_gui, **kwargs):
        super().__init__(parent, **kwargs)

        # Make the GUI responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.input_path_field = InputPathField(self, main_gui, "Input Path")
        self.input_path_field.grid(row=0,
                                   column=0,
                                   padx=DEFAULTS.PADX,
                                   pady=(DEFAULTS.PADY* 0.5, DEFAULTS.PADY * 0.5),
                                   sticky="nsew")

        self.output_dir_field = OutputDirField(self, main_gui, "Output Directory (Optional)")
        self.output_dir_field.grid(row=1,
                                   column=0,
                                   padx=DEFAULTS.PADX,
                                   pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY* 0.5),
                                   sticky="nsew")

    def get_parameters(self):
        return {
            "input_path": self.input_path_field.get(),
            "output_dir": self.output_dir_field.get() or None
        }


class PathField(ctk.CTkFrame, abc.ABC):
    def __init__(self, parent, main_gui, name, **kwargs):
        super().__init__(parent, **kwargs)
        self.main_gui = main_gui
        self.grid_columnconfigure(0, weight=1)

        self.name_label = ctk.CTkLabel(self, text=name, font=self.main_gui.fonts['h3'])
        self.name_label.grid(row=0,
                             column=0,
                             padx=DEFAULTS.PADX,
                             pady=(DEFAULTS.PADY, DEFAULTS.PADY * 0.5),
                             sticky="w")

        self.entry = ctk.CTkEntry(self)
        self.entry.grid(row=1,
                        column=0,
                        padx=(DEFAULTS.PADX, DEFAULTS.PADX * 0.5),
                        pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY),
                        sticky="ew")

        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.browse)
        self.browse_button.grid(row=1,
                                column=1,
                                padx=(DEFAULTS.PADX * 0.5, DEFAULTS.PADX),
                                pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY))

    @abc.abstractmethod
    def browse(self):
        pass

    def get(self):
        return self.entry.get()

    def validate(self):
        path = self.get()
        if not os.path.exists(path):
            print("Invalid path")
            return False
        return True


class InputPathField(PathField):
    def browse(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, file_path)


class OutputDirField(PathField):
    def browse(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, dir_path)
