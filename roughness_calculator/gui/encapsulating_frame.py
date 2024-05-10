import logging
from typing import Type, Optional, Any

import customtkinter as ctk

# Set up logging
logger = logging.getLogger(__name__)


class EncapsulatingFrame(ctk.CTkFrame):
    """
    A class used to encapsulate a frame within another frame.

    Attributes
    ----------
    child_frame : ctk.CTkFrame
        The child frame that is encapsulated within this frame.

    Methods
    -------
    get_parameters():
        Returns the parameters of the child frame.
    """

    def __init__(self,
                 parent: ctk.CTk,
                 frame_class: Type[ctk.CTkFrame],
                 main_gui: Any,
                 image: Optional[Any] = None, **kwargs: Any):
        """
        Constructs all the necessary attributes for the EncapsulatingFrame object.

        Parameters
        ----------
            parent : ctk.CTk
                The parent widget.
            frame_class : Type[ctk.CTkFrame]
                The class of the child frame.
            main_gui : Any
                The main GUI object.
            image : Optional[Any], optional
                The image to be displayed in the child frame, if any.
            **kwargs : Any
                Additional keyword arguments.
        """
        super().__init__(parent, **kwargs)
        logger.info("Initializing EncapsulatingFrame")

        # Configure the grid to make the GUI responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create the child frame
        if image is not None:
            self.child_frame = frame_class(self, main_gui, image)
            logger.info("Child frame created with image")
        else:
            self.child_frame = frame_class(self, main_gui)
            logger.info("Child frame created without image")
        self.child_frame.grid(row=0, column=0, sticky="nsew")

    def get_parameters(self) -> Any:
        """
        Returns the parameters of the child frame.

        Returns
        -------
            Any
                The parameters of the child frame.
        """
        logger.info("Getting parameters from child frame")
        return self.child_frame.get_parameters()
