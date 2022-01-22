import pytest
import _tkinter
import tkinter as tk

from taptempo import gui, taptempo


@pytest.fixture
def mocked_gui(mocker):
    mocker.patch("taptempo.taptempo.time.time", side_effect=[0.0, 60.0, 90.0])

    class MockedGui(gui.TapTempoGui):
        def pump_events(self):
            while self.root.dooneevent(_tkinter.ALL_EVENTS |
                                       _tkinter.DONT_WAIT):
                pass

    root = tk.Tk()
    g = MockedGui(root, tempo=taptempo.TapTempo())
    g.pump_events()
    yield g
    root.destroy()


def test_TapTempoGui_tap_reset(mocked_gui):
    mocked_gui.buttonTap.event_generate("<ButtonPress-1>")
    mocked_gui.buttonTap.event_generate("<ButtonRelease-1>")
    mocked_gui.buttonTap.event_generate("<ButtonPress-1>")
    mocked_gui.buttonTap.event_generate("<ButtonRelease-1>")
    mocked_gui.buttonTap.event_generate("<ButtonPress-1>")
    mocked_gui.buttonTap.event_generate("<ButtonRelease-1>")
    mocked_gui.pump_events()
    assert mocked_gui.labelBPM["text"] == "2.00"
    assert mocked_gui.labelBPMAVG["text"] == "1.33"

    mocked_gui.buttonReset.event_generate("<ButtonPress-1>")
    mocked_gui.buttonReset.event_generate("<ButtonRelease-1>")
    mocked_gui.pump_events()
    assert mocked_gui.labelBPM["text"] == "0.00"


def test_TapTempo_midiOptions(mocked_gui, mocker):
    # switch midi on
    mocked_gui.statusBar.optionsButton.event_generate("<ButtonPress-1>")
    mocked_gui.statusBar.optionsButton.event_generate("<ButtonRelease-1>")
    dialog = [widget for widget in mocked_gui.statusBar.winfo_children()
              if isinstance(widget, gui.MidiOptionsDialog)][0]
    mocked_gui.pump_events()

    for widget in dialog.rbtnFrame.winfo_children():
        assert str(widget["state"]) == tk.DISABLED

    dialog.midiOnCheck.event_generate("<ButtonPress-1>")
    dialog.midiOnCheck.event_generate("<ButtonRelease-1>")
    mocked_gui.pump_events()

    for widget in dialog.rbtnFrame.winfo_children():
        assert str(widget["state"]) == tk.NORMAL

    dialog.okButton.event_generate("<ButtonPress-1>")
    dialog.okButton.event_generate("<ButtonRelease-1>")
    mocked_gui.pump_events()

    assert mocked_gui.statusBar.portName.get() != "Off"

    # switch midi off again
    mocked_gui.statusBar.optionsButton.event_generate("<ButtonPress-1>")
    mocked_gui.statusBar.optionsButton.event_generate("<ButtonRelease-1>")
    dialog = [widget for widget in mocked_gui.statusBar.winfo_children()
              if isinstance(widget, gui.MidiOptionsDialog)][0]
    mocked_gui.pump_events()

    dialog.midiOnCheck.event_generate("<ButtonPress-1>")
    dialog.midiOnCheck.event_generate("<ButtonRelease-1>")
    dialog.okButton.event_generate("<ButtonPress-1>")
    dialog.okButton.event_generate("<ButtonRelease-1>")
    mocked_gui.pump_events()

    assert mocked_gui.statusBar.portName.get() == "Off"
