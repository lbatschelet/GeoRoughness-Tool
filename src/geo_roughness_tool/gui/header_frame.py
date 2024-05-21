import logging
from typing import Any

import customtkinter as ctk

from .defaults import DEFAULTS

# Set up logging
logger = logging.getLogger(__name__)


class HeaderFrame(ctk.CTkFrame):
    """
    A class used to create the header frame of the GUI.

    Attributes
    ----------
    main_gui : Any
        The main GUI object.
    title_label : ctk.CTkLabel
        The label that displays the title.
    description_label : ctk.CTkLabel
        The label that displays the description.
    """
    def __init__(self, parent: ctk.CTk, main_gui: Any, **kwargs: Any):
        """
        Constructs all the necessary attributes for the HeaderFrame object.

        Parameters
        ----------
            parent : ctk.CTk
                The parent widget.
            main_gui : Any
                The main GUI object.
            **kwargs : Any
                Additional keyword arguments.
        """
        super().__init__(parent, **kwargs)
        logger.info("Initializing HeaderFrame")
        self.main_gui = main_gui

        # Configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure([0, 1], weight=1)

        # Create the title label
        self.title_label = (
            ctk.CTkLabel(self,
                         text="GeoRoughness Tool",
                         font=self.main_gui.fonts['h1']))
        self.title_label.grid(row=0,
                              column=0,
                              padx=DEFAULTS.PADX,
                              pady=(DEFAULTS.PADY, 0),
                              sticky="w")
        logger.info("Title label created")

        # Create the description label
        self.description_label = (
            ctk.CTkLabel(self,
                         text="Program to calculate and categorize surface Roughness.",
                         font=self.main_gui.fonts['body']))
        self.description_label.grid(row=1,
                                    column=0,
                                    padx=DEFAULTS.PADX,
                                    pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5),
                                    sticky="w")
        logger.info("Description label created")

        # Create the toggle button
        self.toggle_button = ctk.CTkButton(self, text="Show Advanced", command=self.toggle_advanced_options)
        self.toggle_button.grid(row=0,
                                column=1,
                                padx=(DEFAULTS.PADX, DEFAULTS.PADY * 2),
                                pady=(DEFAULTS.PADY, 0),
                                sticky="e")
        logger.info("Toggle button created")

    def toggle_advanced_options(self):
        self.main_gui.toggle_advanced_options()
        if self.main_gui.show_advanced_options:
            self.toggle_button.configure(text="Hide Advanced")
        else:
            self.toggle_button.configure(text="Show Advanced")

