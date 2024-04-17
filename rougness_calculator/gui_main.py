# TODO: Add docstrings and comments
# TODO: Add progress indication

import tkinter as tk
from tkinter import filedialog
from application_driver import ApplicationDriver


class ApplicationGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("GeoTIFF Processor")
        self.btn_open = tk.Button(master, text="Open TIFF", command=self.open_file)
        self.btn_open.pack()

    @staticmethod
    def open_file():
        input_path = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tif")])
        if input_path:
            output_path = filedialog.asksaveasfilename(defaultextension=".tif",
                                                       filetypes=[("TIFF files", "*.tif")])
            if output_path:
                driver = ApplicationDriver(input_path, output_path)
                driver.run()
                tk.messagebox.showinfo("Success", "Processing completed successfully.")


def main():
    root = tk.Tk()
    app = ApplicationGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
