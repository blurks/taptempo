import rtmidi


class MidiInterface:
    """Open a midi port and listen for events. For every Note-On event, call a
    callback."""
    def __init__(self, callback):
        self.tapCallback = callback
        self.midiin = None
        self.reset()

    def reset(self):
        """Reset the midi connection. All ports will be closed."""
        if self.midiin and self.midiin.isPortOpen():
            self.midiin.closePort()
        # we need a new instance of RtMidiIn() everytime after we
        # closed a port. see
        # <https://github.com/patrickkidd/pyrtmidi/issues/22>
        self.midiin = rtmidi.RtMidiIn()
        self.midiin.setCallback(self.midiCallback)
        self.portNumber = 0
        self.portName = ""
        self.isConnected = False

    def getPorts(self):
        """Get a dictionary containing the number of a port as the key and the
        name as value."""
        portN = self.midiin.getPortCount()
        return dict([(i, self.midiin.getPortName(i)) for i in range(portN)])

    def openPort(self, port):
        """Open a port with the corresponding number. Returns True un success,
        False on failure."""
        try:
            self.midiin.openPort(port)
            self.portNumber = port
            self.portName = self.midiin.getPortName(port)
            self.isConnected = True
        except Exception:
            self.portNumber = 0
            self.portName = ""
            self.isConnected = False
        return self.isConnected

    def midiCallback(self, midiE):
        """This is the callback for RtMidiIn. When a Note-On Event occurs,
        call self.tapCallback."""
        if midiE.isNoteOn():
            self.tapCallback()
