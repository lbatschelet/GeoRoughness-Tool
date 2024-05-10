import customtkinter as ctk


class EncapsulatingFrame(ctk.CTkFrame):
    def __init__(self, parent, frame_class, main_gui, image=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Make the GUI responsive
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        if image is not None:
            self.child_frame = frame_class(self, main_gui, image)
        else:
            self.child_frame = frame_class(self, main_gui)
        self.child_frame.grid(row=0, column=0, sticky="nsew")
