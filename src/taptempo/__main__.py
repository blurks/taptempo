import tkinter as tk
from taptempo.taptempo import TapTempoGui

root = tk.Tk()
root.title("Tap Tempo")
gui = TapTempoGui(root)
gui.run()
