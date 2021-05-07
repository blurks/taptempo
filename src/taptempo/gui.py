import tkinter as tk
from tkinter import ttk

from taptempo.midi import MidiInterface
from taptempo.taptempo import TapTempo
    

class MidiStatusBar(ttk.Frame):
    """Status bar that shows info about the MIDI interface and provides
    some configuration options."""
    def __init__(self, master, midiInterface):
        ttk.Frame.__init__(self, master, padding=(4,0,4,0), borderwidth=2, relief="sunken")
        self.midi = midiInterface

        ttk.Label(self, text="MIDI:").grid(row=0, column=0)
        self.midiStatusLabel = ttk.Label(self, text=self.midi.portName)
        self.midiStatusLabel.grid(row=0, column=1, sticky="nwse")

        self.optionsButton = ttk.Button(self, text="⚙", width=-1,
                                        command=self.showOptions)
        self.optionsButton.grid(row=0, column=2, sticky="e")
        self.grid_columnconfigure(1, weight=1)

    def update(self):
        self.midiStatusLabel["text"] = self.midi.portName

    def showOptions(self):
        # TODO: split up into multiple methods
        optionsDialog = tk.Toplevel(self)
        optionsDialog.title("Chose a midi port")
        optionsFrame = ttk.Frame(optionsDialog, padding=(4,4,4,4))
        optionsFrame.grid(row=0, column=0, sticky="nwse")
        ttk.Label(optionsFrame, text="Chose a midi port").grid(column=0, row=0, columnspan=2)

        rbtnFrame = ttk.Frame(optionsFrame)
        portVar = tk.IntVar()
        portVar.set(self.midi.portNumber)

        ports = self.midi.getPorts()
        for pNum in ports.keys():
            rbtn = tk.Radiobutton(rbtnFrame, text=ports[pNum],
                                  variable=portVar, value=pNum)
            rbtn.grid(sticky="W")
        rbtnFrame.grid(row=1, column=0, columnspan=2, sticky="W")

        def ok():
            # TODO: get rid of this uglyness
            if self.midi.portNumber != portVar.get():
                self.midi.closePort()
                self.midi.openPort(portVar.get())
            self.update()
            optionsDialog.destroy()
            
        okButton = ttk.Button(optionsFrame, text="Ok", command=ok)
        okButton.grid(row=2, column=0)

        cancelButton = ttk.Button(optionsFrame, text="Cancel", command=optionsDialog.destroy)
        cancelButton.grid(row=2, column=1)

class TapTempoGui:
    """Tk-App to tap-in a tempo."""
    def __init__(self, root, tempo=TapTempo()):
        """Build the Gui."""
        # Model and Stingvariables
        self.tempo = tempo
        self.strBPM = tk.StringVar()
        self.strBPMAVG = tk.StringVar()
        self.update()

        self.root = root

        # main app
        self.mainframe = ttk.Frame(self.root, padding="4 4 4 4")
        self.mainframe.grid(column=0, row=0)

        self.midi = MidiInterface(self.tap)
        self.midi.openPort(0)
        self.statusBar = MidiStatusBar(self.root, self.midi)
        self.statusBar.grid(column=0, row=1, sticky="nwse")
        
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