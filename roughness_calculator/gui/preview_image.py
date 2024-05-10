import tkinter as tk

import customtkinter as ctk
from PIL import Image, ImageTk


class PreviewImage(ctk.CTkFrame):
    def __init__(self, parent, main_gui, image, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_gui = main_gui
        self.original_image = image
        self.photo_image = ImageTk.PhotoImage(image)

        self.canvas = tk.Canvas(self, bg='white', highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.image_on_canvas = self.canvas.create_image(0, 0, image=self.photo_image, anchor="nw")

        # Bind the resize event to resize the canvas
        self.canvas.bind("<Configure>", self.resize_image)

    def resize_image(self, event):
        # Calculate the new size while maintaining the aspect ratio
        original_width, original_height = self.original_image.size
        aspect_ratio = original_width / original_height

        new_width = event.width
        new_height = int(new_width / aspect_ratio)

        # If calculated height exceeds available height, adjust width based on the height
        if new_height > event.height:
            new_height = event.height
            new_width = int(new_height * aspect_ratio)

        # Resize the original image
        resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(resized_image)

        # Update the image on the canvas and reposition it
        self.canvas.itemconfig(self.image_on_canvas, image=self.photo_image)
        self.canvas.coords(self.image_on_canvas, event.width // 2, event.height // 2)  # Center the image
