import logging
import webbrowser
from typing import Any
from PIL import Image
import customtkinter as ctk
from .defaults import DEFAULTS
import os

# Set up logging
logger = logging.getLogger(__name__)

class HeaderFrame(ctk.CTkFrame):
    """
    A class used to create the header frame of the GUI.

    Attributes
    ----------
    main_gui : Any
        The main GUI object.
    banner_image : ctk.CTkImage
        The image object that displays the banner.
    banner_label : ctk.CTkLabel
        The label to display the banner image.
    toggle_button : ctk.CTkButton
        The button to toggle advanced options.
    help_button : ctk.CTkButton
        The button to open the help wiki.
    resize_timer : int
        The timer used to throttle resize events.
    current_size : tuple
        The current size of the banner image.
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
        self.resize_timer = None
        self.current_size = (0, 0)

        # Configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure([0,1], weight=1)

        # Load the original images
        script_dir = os.path.dirname(__file__)
        self.original_light_image = Image.open(os.path.join(script_dir, "resources", "GeoRoughness-Banner-lang-Light.png"))
        self.original_dark_image = Image.open(os.path.join(script_dir, "resources", "GeoRoughness-Banner-lang-dark.png"))

        # Create the banner label
        self.banner_label = ctk.CTkLabel(self, text="")
        self.banner_label.grid(row=0, column=0, padx=DEFAULTS.PADX, pady=(DEFAULTS.PADY, 0), sticky="nsw", rowspan=2)
        logger.info("Banner label created")

        # Create the help button
        self.help_button = ctk.CTkButton(self, text="Help", command=self.open_help)
        self.help_button.grid(row=0, column=1, padx=(DEFAULTS.PADX, DEFAULTS.PADX * 2), pady=(DEFAULTS.PADY, DEFAULTS.PADY * 0.5), sticky="e")
        logger.info("Help button created")

        # Create the toggle button
        self.toggle_button = ctk.CTkButton(self, text="Show Advanced", command=self.toggle_advanced_options)
        self.toggle_button.grid(row=1, column=1, padx=(DEFAULTS.PADX, DEFAULTS.PADX * 2), pady=(DEFAULTS.PADY * 0.5, 0), sticky="e")
        logger.info("Toggle button created")

        # Bind the resize event to update the image size
        self.bind("<Configure>", self.on_resize)

        # Initial image setup
        self.update_banner_image()

    def update_banner_image(self):
        width = self.winfo_width()
        if width <= 1:
            # Sometimes winfo_width returns 1 initially, so we ignore it
            return

        # Calculate the new size
        new_width = int(width * 0.6)
        max_width = 600  # Set a maximum width for the banner
        if new_width > max_width:
            new_width = max_width

        aspect_ratio = self.original_light_image.width / self.original_light_image.height
        new_height = int(new_width / aspect_ratio)

        # Ensure width and height are greater than 0 and differ from the current size
        if new_width > 0 and new_height > 0 and (new_width, new_height) != self.current_size:
            logger.info(f"Resizing banner image to {new_width}x{new_height}")

            # Resize images
            resized_light_image = self.original_light_image.resize((new_width, new_height), Image.LANCZOS)
            resized_dark_image = self.original_dark_image.resize((new_width, new_height), Image.LANCZOS)

            # Update the CTkImage
            self.banner_image = ctk.CTkImage(light_image=resized_light_image, dark_image=resized_dark_image,
                                             size=(new_width, new_height))

            # Update the banner label
            self.banner_label.configure(image=self.banner_image)

            # Update the current size
            self.current_size = (new_width, new_height)

    def on_resize(self, event):
        # Cancel the previous timer if it exists
        if self.resize_timer:
            self.after_cancel(self.resize_timer)
        # Set a new timer to delay the resize operation
        self.resize_timer = self.after(200, self.update_banner_image)

    def toggle_advanced_options(self):
        self.main_gui.toggle_advanced_options()
        if self.main_gui.show_advanced_options:
            self.toggle_button.configure(text="Hide Advanced")
        else:
            self.toggle_button.configure(text="Show Advanced")

    def open_help(self):
        webbrowser.open("https://github.com/lbatschelet/GeoRoughness-Tool/wiki")
