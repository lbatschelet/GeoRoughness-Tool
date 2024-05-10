import customtkinter as ctk
from PIL import Image
from customtkinter import CTkScrollableFrame

from roughness_calculator.gui.defaults import DEFAULTS
from roughness_calculator.gui.encapsulating_frame import EncapsulatingFrame
from roughness_calculator.gui.footer_frame import FooterFrame
from roughness_calculator.gui.header_frame import HeaderFrame
from roughness_calculator.gui.parameter_input import ParameterFrame
from roughness_calculator.gui.path_frame import PathFrame
from roughness_calculator.gui.preview_image import PreviewImage


class MainGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Surface Roughness Calculator")

        self.preview_image = Image.open(r"C:\Users\batsc\PycharmProjects\dem-roughness-calculator\tests\test_data\20231116_DEM_Sammler_Obermad_0.05m.tif")

        # Create Font objects
        self.fonts = {
            "h1": ctk.CTkFont(size=24, weight="bold"),
            "h2": ctk.CTkFont(size=18, weight="bold"),
            "h3": ctk.CTkFont(size=14, weight="bold"),
            "body": ctk.CTkFont(size=13),
            "small": ctk.CTkFont(size=10),
            "tiny": ctk.CTkFont(size=8),
            "monospace": ctk.CTkFont(family="Courier New", size=12)
        }

        # Get screen width and height
        screen_width = int(0.5 * self.winfo_screenwidth())
        screen_height = int(0.5 * self.winfo_screenheight())

        # Set window size to screen size
        self.geometry(f"{screen_width}x{screen_height}")

        # Create a ScrolledFrame
        self.scrolled_frame = CTkScrollableFrame(self)
        self.scrolled_frame.pack(fill="both", expand=True)

        # Make the GUI responsive
        self.scrolled_frame.grid_columnconfigure(0, weight=1)
        self.scrolled_frame.grid_rowconfigure([0, 1, 2, 3], weight=1)

        self.header_frame = EncapsulatingFrame(self.scrolled_frame, HeaderFrame, self)
        self.header_frame.grid(row=0, column=0, padx=DEFAULTS.PADX, pady=(DEFAULTS.PADY, DEFAULTS.PADY * 0.5), sticky="nsew")

        self.path_frame = EncapsulatingFrame(self.scrolled_frame, PathFrame, self)
        self.path_frame.grid(row=1, column=0, padx=DEFAULTS.PADX, pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5), sticky="nsew")

        self.parameter_frame = EncapsulatingFrame(self.scrolled_frame, ParameterFrame, self)
        self.parameter_frame.grid(row=2, column=0, padx=DEFAULTS.PADX, pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5), sticky="nsew")

        self.preview_frame = EncapsulatingFrame(self.scrolled_frame, PreviewImage, self, self.preview_image)
        self.preview_frame.grid(row=3, column=0, padx=DEFAULTS.PADX, pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY * 0.5), sticky="nsew")

        self.footer_frame = EncapsulatingFrame(self.scrolled_frame, FooterFrame, self)
        self.footer_frame.grid(row=4, column=0, padx=DEFAULTS.PADX, pady=(DEFAULTS.PADY * 0.5, DEFAULTS.PADY), sticky="nsew")

if __name__ == "__main__":
    MainGUI().mainloop()