import logging
from typing import Any

import customtkinter as ctk

from src.geo_roughness_tool.gui.defaults import DEFAULTS

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

        # Create the title label
        self.title_label = (
            ctk.CTkLabel(self,
                         text="Surface Roughness Calculator",
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
                         text="This program calculates the surface roughness of a DEM.",
                         font=self.main_gui.fonts['body']))
        self.description_label.grid(row=1,
                                    column=0,
                                    padx=DEFAULTS.PADX,
                                    pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY),
                                    sticky="w")
        logger.info("Description label created")
