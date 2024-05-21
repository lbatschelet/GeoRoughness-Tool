import logging
import logging.handlers
import webbrowser
from typing import Any
import tkinter as tk
import tkinter.scrolledtext as st

import customtkinter as ctk


from .defaults import DEFAULTS
from geo_roughness_tool.log_config import Defaults

# Set up logging
logger = logging.getLogger(__name__)


class FooterFrame(ctk.CTkFrame):
    """
    A class used to create the footer frame of the GUI.

    Attributes
    ----------
    main_gui : Any
        The main GUI object.
    help_button : WebsiteButton
        The button that opens the documentation website.
    info_label : ctk.CTkLabel
        The label that displays the copyright information.
    """

    def __init__(self, parent: ctk.CTk, main_gui: Any, **kwargs: Any):
        """
        Constructs all the necessary attributes for the FooterFrame object.

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
        logger.info("Initializing FooterFrame")
        self.main_gui = main_gui

        # Configure the grid
        self.grid_rowconfigure([0, 1], weight=1)
        self.grid_columnconfigure([0, 1, 2, 3], weight=1)

        # Create the help button
        self.help_button = WebsiteButton(self,
                                         "https://github.com/lbatschelet/GeoRoughness-Tool",
                                         text="Documentation")
        self.help_button.grid(row=0,
                              column=0,
                              padx=(DEFAULTS.PADX, DEFAULTS.PADX * 0.5),
                              pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5),
                              sticky="nsew")

        # Create the log button
        self.log_button = ctk.CTkButton(self, text="Show Logs", command=self.open_log_window)
        self.log_button.grid(row=0,
                             column=3,
                             padx=(DEFAULTS.PADX * 0.5, DEFAULTS.PADX),
                             pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5),
                             sticky="nsew")

        # Create the info label
        self.info_label = (
            ctk.CTkLabel(self,
                         text="GeoRoughness Tool - © 2024 L. Batschelet, F. Mohaupt, S. Röthlisberger. "
                              "Licensed under the MIT License.",
                         font=self.main_gui.fonts['small']))
        self.info_label.grid(row=1,
                             column=0,
                             columnspan=4,
                             padx=DEFAULTS.PADX,
                             pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY),
                             sticky="nsew")

    def open_log_window(self):
        """
        Opens the log window.
        """
        LogWindow(self)


class WebsiteButton(ctk.CTkButton):
    """
    A class used to create a button that opens a website.

    Attributes
    ----------
    url : str
        The URL of the website to open.
    """

    def __init__(self, parent: ctk.CTk, url: str, **kwargs: Any):
        """
        Constructs all the necessary attributes for the WebsiteButton object.

        Parameters
        ----------
            parent : ctk.CTk
                The parent widget.
            url : str
                The URL of the website to open.
            **kwargs : Any
                Additional keyword arguments.
        """
        super().__init__(parent, command=self.open_website, **kwargs)
        logger.info("Initializing WebsiteButton with URL: %s", url)
        self.url = url

    def open_website(self):
        """
        Opens the website in a web browser.
        """
        logger.info("Opening website: %s", self.url)
        webbrowser.open(self.url)


class LogWindow(tk.Toplevel):
    """
    A class used to create a window that displays the logs.

    Attributes
    ----------
    text_area : st.ScrolledText
        The text area that displays the logs.
    """

    def __init__(self, parent: ctk.CTk):
        super().__init__(parent)
        self.title("Logs")
        self.geometry("500x500")  # adjust as needed

        # Create a scrollable text area
        self.text_area = st.ScrolledText(self, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Bind the mouse wheel to the text area to handle scrolling independently
        self.text_area.bind("<Enter>", self._bind_mouse_wheel)
        self.text_area.bind("<Leave>", self._unbind_mouse_wheel)

        # Get the log file handler from the root logger
        root_logger = logging.getLogger()
        self.file_handler = next((handler for handler in root_logger.handlers if isinstance(handler, logging.FileHandler)), None)

        # Set the state to disabled to make the text read-only
        self.text_area.config(state=tk.DISABLED)

        # Store the last log content
        self.last_log_content = ""

        # Start the log update loop
        self.update_logs()

    def _bind_mouse_wheel(self, event):
        self.text_area.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.text_area.bind_all("<Button-4>", self._on_mouse_wheel)  # For Linux systems
        self.text_area.bind_all("<Button-5>", self._on_mouse_wheel)  # For Linux systems

    def _unbind_mouse_wheel(self, event):
        self.text_area.unbind_all("<MouseWheel>")
        self.text_area.unbind_all("<Button-4>")  # For Linux systems
        self.text_area.unbind_all("<Button-5>")  # For Linux systems

    def _on_mouse_wheel(self, event):
        if event.num == 4:  # For Linux systems
            self.text_area.yview_scroll(-1, "units")
        elif event.num == 5:  # For Linux systems
            self.text_area.yview_scroll(1, "units")
        else:  # For Windows and Mac systems
            self.text_area.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_logs(self):
        """
        Updates the logs in the text area.
        """
        if self.file_handler:
            # Save the current scroll position
            vert_scroll_position = self.text_area.yview()
            horiz_scroll_position = self.text_area.xview()

            # Read the log file
            with open(self.file_handler.baseFilename, "r") as log_file:
                log_content = log_file.read()

            # Update the text area only if the content has changed
            if log_content != self.last_log_content:
                self.last_log_content = log_content

                # Clear the text area and insert new logs
                self.text_area.config(state=tk.NORMAL)
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, log_content)
                self.text_area.config(state=tk.DISABLED)

                # Restore the scroll position
                self.text_area.yview_moveto(vert_scroll_position[0])
                self.text_area.xview_moveto(horiz_scroll_position[0])

        # Schedule the next update
        self.after(Defaults.LOG_UPDATE_INTERVAL, self.update_logs)

