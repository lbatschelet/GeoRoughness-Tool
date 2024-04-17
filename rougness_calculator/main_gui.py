import tkinter as tk
from tkinter import filedialog
from geo_tiff_processor import GeoTIFFProcessor

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Button, um die Eingabedatei auszuwählen
        self.load_file_button = tk.Button(self)
        self.load_file_button["text"] = "Eingabe-GeoTIFF auswählen"
        self.load_file_button["command"] = self.load_input_file
        self.load_file_button.pack(side="top")

        # Button, um die Ausgabedatei festzulegen
        self.save_file_button = tk.Button(self)
        self.save_file_button["text"] = "Ausgabe-GeoTIFF speichern als..."
        self.save_file_button["command"] = self.save_output_file
        self.save_file_button.pack(side="top")

        # Start-Button, um den Verarbeitungsprozess zu starten
        self.start_button = tk.Button(self, text="Verarbeitung starten", command=self.start_processing)
        self.start_button.pack(side="top")

        # Beendet die Anwendung
        self.quit = tk.Button(self, text="Beenden", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def load_input_file(self):
        self.input_path = filedialog.askopenfilename(filetypes=[("TIFF files", "*.tif *.tiff")])
        print("Eingabedatei ausgewählt:", self.input_path)

    def save_output_file(self):
        self.output_path = filedialog.asksaveasfilename(defaultextension=".tif", filetypes=[("TIFF files", "*.tif *.tiff")])
        print("Ausgabedatei festgelegt:", self.output_path)

    def start_processing(self):
        if hasattr(self, 'input_path') and hasattr(self, 'output_path'):
            processor = GeoTIFFProcessor(self.input_path, self.output_path)
            processor.process_tiff()
            print("Verarbeitung abgeschlossen.")
        else:
            print("Bitte wähle sowohl eine Eingabe- als auch eine Ausgabedatei.")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
