import tkinter as tk
from tkinter import ttk

from taptempo.midi import MidiInterface
from taptempo.taptempo import TapTempo


class MidiOptionsDialog(tk.Toplevel):
    """A dialog window that lets you set midi options."""
    def __init__(self, master, midi, portName):
        tk.Toplevel.__init__(self, master)
        self.title("MIDI Options")

        # set variables
        self.midi = midi
        self.portName = portName

        self.portVar = tk.IntVar()
        self.portVar.set(self.midi.portNumber)

        self.midiOn = tk.IntVar()
        self.midiOn.set(int(self.midi.isConnected))
        # if midi input is switched on/off, enable/disable the
        # radiobuttons for the midi ports
        self.midiOn.trace_add("write", self.setRbtnState)

        # put widgets
        optionsFrame = ttk.Frame(self, padding=(4, 4, 4, 4))
        optionsFrame.grid(row=0, column=0, sticky="nwse")

        # checkbox to enable/disable midi input
        self.midiOnCheck = tk.Checkbutton(optionsFrame,
                                          text="Enable midi input",
                                          variable=self.midiOn)
        self.midiOnCheck.grid(row=0, column=0, columnspan=2, sticky="W")

        # radiobuttons to chose the midiport
        self.rbtnFrame = ttk.Frame(optionsFrame)
        self.rbtnFrame.grid(row=2, column=0, columnspan=2, sticky="W")

        ttk.Label(self.rbtnFrame, text="Chose a midi port").grid()

        ports = self.midi.getPorts()
        for pNum in ports.keys():
            rbtn = tk.Radiobutton(self.rbtnFrame, text=ports[pNum],
                                  variable=self.portVar, value=pNum)
            rbtn.grid(sticky="W")
        self.setRbtnState()

        # ok and cancel buttons
        self.okButton = ttk.Button(optionsFrame, text="Ok", command=self.ok)
        self.okButton.grid(row=3, column=0)

        cancelButton = ttk.Button(optionsFrame, text="Cancel",
                                  command=self.destroy)
        cancelButton.grid(row=3, column=1)

    def setRbtnState(self, *args):
        """Set the state (disabled or normal) of the
        midi-port-radiobuttons. Enable, if midi is enabled, disable
        otherwise."""
        for widget in self.rbtnFrame.winfo_children():
            if self.midiOn.get() == 0:
                widget.configure(state=tk.DISABLED)
            else:
                widget.configure(state=tk.NORMAL)

    def ok(self):
        """Callback for the 'Ok' Button. Sets all options and destroys the
        dialog window."""
        self.midi.reset()
        if self.midiOn.get() == 1:
            self.midi.openPort(self.portVar.get())
            self.portName.set(self.midi.portName)
        else:
            self.portName.set("Off")
        self.destroy()


class MidiStatusBar(ttk.Frame):
    """Status bar that shows info about the MIDI interface and provides
    some configuration options."""
    def __init__(self, master, midiInterface):
        # init frame
        ttk.Frame.__init__(self, master, padding=(4, 0, 0, 0), borderwidth=2,
                           relief="sunken")

        # set variables
        self.midi = midiInterface
        self.portName = tk.StringVar()
        self.portName.set(self.midi.portName
                          if self.midi.isConnected
                          else "Off")

        # put some widgets
        ttk.Label(self, text="MIDI:").grid(row=0, column=0)

        # current portname/midi status
        self.midiStatusLabel = ttk.Label(self, textvariable=self.portName)
        self.midiStatusLabel.grid(row=0, column=1, sticky="nwse")

        # button, that opens a midi options dialog
        self.optionsButton = ttk.Button(self, text="⚙", width=-1,
                                        command=self.showOptions)
        self.optionsButton.grid(row=0, column=2, sticky="e")

        # expand the middle column (containing the midi status)
        self.grid_columnconfigure(1, weight=1)

    def showOptions(self):
        """Show a dialog window that lets you set midi options."""
        dialog = [widget for widget in self.winfo_children()
                  if isinstance(widget, MidiOptionsDialog)]
        if not dialog:
            MidiOptionsDialog(self, self.midi, self.portName)
        else:
            dialog[0].lift()
            dialog[0].focus_set()


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

        # midi status bar
        self.midi = MidiInterface(self.tap)
        self.statusBar = MidiStatusBar(self.root, self.midi)
        self.statusBar.grid(column=0, row=1, sticky="nwse")

        # BPM Labels
        ttk.Label(self.mainframe, text="BPM:", justify="right").grid(column=0,
                                                                     row=0)
        self.labelBPM = ttk.Label(self.mainframe, textvariable=self.strBPM)
        self.labelBPM.grid(column=1, row=0)

        # Average BPM Labels
        ttk.Label(self.mainframe, text="Average BPM:", justify="right"
                  ).grid(column=0, row=1)
        self.labelBPMAVG = ttk.Label(self.mainframe,
                                     textvariable=self.strBPMAVG)
        self.labelBPMAVG.grid(column=1, row=1)

        # Buttons
        self.buttonTap = ttk.Button(self.mainframe, text="Tap")
        # usually a button is clicked after releasing the
        # mousebutton. For tapping the pressing of the button is more
        # appropriate
        self.buttonTap.bind("<ButtonPress-1>", lambda e: self.tap())
        self.buttonTap.grid(column=0, row=2)

        self.buttonReset = ttk.Button(self.mainframe, text="Reset",
                                      command=self.reset)
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
        self.root.mainloop()  # pragma: nocover


if __name__ == "__main__":  # pragma: nocover
    root = tk.Tk()
    root.title("Tap Tempo")
    gui = TapTempoGui(root)
    gui.run()
