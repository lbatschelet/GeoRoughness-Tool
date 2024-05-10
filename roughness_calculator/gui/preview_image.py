import tkinter as tk

import customtkinter as ctk
from PIL import Image, ImageTk


class PreviewImage(ctk.CTkFrame):
    def __init__(self, parent, main_gui, image=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_gui = main_gui
        self.original_image = image

        # Define the canvas attribute
        self.canvas = tk.Canvas(self, bg='white', highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Define the image_on_canvas attribute
        self.image_on_canvas = None

        if self.original_image is not None:
            self.photo_image = ImageTk.PhotoImage(self.original_image)
            self.image_on_canvas = self.canvas.create_image(0, 0, image=self.photo_image, anchor="nw")

            # Bind the resize event to resize the canvas
            self.canvas.bind("<Configure>", self.resize_image)

    def resize_image(self, *args):
        # Calculate the new size while maintaining the aspect ratio
        original_width, original_height = self.original_image.size
        aspect_ratio = original_height / original_width

        new_width = self.canvas.winfo_width()  # Get the current width of the canvas
        new_height = int(new_width * aspect_ratio)

        # Resize the original image
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas and reposition it
        self.canvas.itemconfig(self.image_on_canvas, image=self.photo_image)
        self.canvas.coords(self.image_on_canvas, 0, 0)  # Anchor the image to the top left corner

        # Adjust the height of the canvas to fit the new image
        self.canvas.config(height=new_height)

    def display_preview(self, preview: Image) -> None:
        """
        Displays the preview image in the GUI.

        Args:
            preview: The preview image to display.
        """
        self.original_image = preview
        self.photo_image = ImageTk.PhotoImage(self.original_image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.photo_image)

        # Resize the image to fit the canvas
        self.resize_image(self.canvas)
