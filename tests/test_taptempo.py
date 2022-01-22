from taptempo import taptempo


def test_init():
    t = taptempo.TapTempo()
    assert t.firstTap == 0
    assert t.lastTap == 0
    assert t.bpm == 0.0
    assert t.totalTaps == 0
    assert t.bpmAvg == 0.0


def test_tap(mocker):
    mocker.patch("taptempo.taptempo.time.time", side_effect=[0.0, 60.0, 90.0])
    t = taptempo.TapTempo()
    t.tap()
    t.tap()
    t.tap()
    assert t.totalTaps == 3
    assert t.firstTap == 0.0
    assert t.lastTap == 90.0
    assert t.bpm == 2.0
    assert 1.33 < t.bpmAvg < 1.34


def test_reset():
    t = taptempo.TapTempo()
    t.tap()
    t.tap()
    t.reset()
    assert t.firstTap == 0
    assert t.lastTap == 0
    assert t.bpm == 0.0
    assert t.totalTaps == 0
    assert t.bpmAvg == 0.0
