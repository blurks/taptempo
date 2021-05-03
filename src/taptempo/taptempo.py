import time
import tkinter as tk
from tkinter import ttk


class TapTempo:
    """Model to tap in a tempo."""
    def __init__(self):
        self.reset()
        
    def tap(self):
        """Perform a single tap and calculate the bpm and averate bpm."""
        tap = time.time()
        if self.totalTaps <= 0:
            # if this is the first tap
            self.firstTap = tap
            self.lastTap = tap
        else:
            self.bpm = 60.0 / (tap - self.lastTap)
            self.bpmAvg = 60.0 / ((tap - self.firstTap) / self.totalTaps)

        self.totalTaps += 1
        self.lastTap = tap
        return self.bpm

    def reset(self):
        """Set everything to zero."""
        self.firstTap = 0
        self.lastTap = 0
        self.bpm = 0.0
        self.totalTaps = 0
        self.bpmAvg = 0.0


class TapTempoGui:
    """Tk-App to tap-in a tempo."""
    def __init__(self, root, tempo=TapTempo()):
        """Build the Gui."""
        # Model and Stingvariables
        self.tempo = tempo
        self.strBPM = tk.StringVar()
        self.strBPMAVG = tk.StringVar()
        self.update()

        # Root and Mainframe
        self.root = root

        self.mainframe = ttk.Frame(self.root, padding="4 4 4 4")
        self.mainframe.grid(column=0, row=0)

        # BPM Labels
        ttk.Label(self.mainframe, text="BPM:", justify="right").grid(column=0, row=0)
        self.labelBPM = ttk.Label(self.mainframe, textvariable=self.strBPM)
        self.labelBPM.grid(column=1, row=0)

        # Average BPM Labels
        ttk.Label(self.mainframe, text="Average BPM:", justify="right").grid(column=0, row=1)
        self.labelBPMAVG = ttk.Label(self.mainframe, textvariable=self.strBPMAVG)
        self.labelBPMAVG.grid(column=1, row=1)

        # Buttons
        self.buttonTap = ttk.Button(self.mainframe, text="Tap")
        # usually a button is clicked after releasing the
        # mousebutton. For tapping the pressing of the button is more
        # appropriate
        self.buttonTap.bind("<ButtonPress-1>", lambda e: self.tap())
        self.buttonTap.grid(column=0, row=2)

        self.buttonReset = ttk.Button(self.mainframe, text="Reset", command=self.reset)
        self.buttonReset.grid(column=1, row=2)

        # polish
        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    def update(self):
        """Update all labels."""
        self.strBPM.set("{:.2f}".format(self.tempo.bpm))
        self.strBPMAVG.set("{:.2f}".format(self.tempo.bpmAvg))

    def tap(self):
        """Perform a single tap and update the tempo labels."""
        self.tempo.tap()
        self.update()

    def reset(self):
        """Reset everything to zero."""
        self.tempo.reset()
        self.update()
    
    def run(self):
        """Run TK-Mainloop."""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tap Tempo")
    gui = TapTempoGui(root)
    gui.run()
