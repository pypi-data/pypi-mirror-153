import time

import numpy as np
import pytest

from stimuli.audio import BaseSound


def test_check_volume():
    """Check the volume static checker."""
    volume = BaseSound._check_volume(50)
    assert np.allclose(volume, np.array([50, 50]))
    volume = BaseSound._check_volume((25, 50))
    assert np.allclose(volume, np.array([25, 50]))
    volume = BaseSound._check_volume((0, 100))
    assert np.allclose(volume, np.array([0, 100]))
    with pytest.raises(
        TypeError, match="must be an instance of numeric or tuple"
    ):
        BaseSound._check_volume([25, 50])
    with pytest.raises(AssertionError):
        volume = BaseSound._check_volume((25, 50, 75))
    with pytest.raises(TypeError, match="must be an instance of numeric"):
        volume = BaseSound._check_volume(("25", 50))
    with pytest.raises(AssertionError):
        volume = BaseSound._check_volume((25, 101))
    with pytest.raises(AssertionError):
        volume = BaseSound._check_volume((-25, 100))


def test_check_sample_rate():
    """Check the sample rate static checker."""
    fs = BaseSound._check_sample_rate(44100)
    assert fs == 44100
    with pytest.raises(TypeError, match="must be an instance of int"):
        BaseSound._check_sample_rate(44100.0)
    with pytest.raises(AssertionError):
        BaseSound._check_sample_rate(-101)


def test_check_duration():
    """Check the duration static checker."""
    duration = BaseSound._check_duration(101)
    assert duration == 101
    duration = BaseSound._check_duration(101.01)
    assert duration == 101.01
    with pytest.raises(TypeError, match="must be an instance of numeric"):
        BaseSound._check_duration([101])
    with pytest.raises(AssertionError):
        BaseSound._check_sample_rate(-101)


def _test_base(Sound):
    """Test base functionalities with a Sound class."""
    sound = Sound(10, duration=0.2)

    # test play/stop
    sound.play()
    time.sleep(0.2)

    duration = 1
    sound = Sound(10, duration=duration)
    sound.play(blocking=True)

    start = time.time()
    sound.play(blocking=False)
    sound.stop()
    assert time.time() - start <= duration

    # test volume setter
    assert np.isclose(np.max(np.abs(sound.signal)), sound.volume / 100)
    sound.volume = 20
    assert sound.volume == 20
    assert np.isclose(np.max(np.abs(sound.signal)), sound.volume / 100)
    sound.volume = (20, 100)
    assert sound.volume == (20, 100)
    assert np.allclose(
        np.max(np.abs(sound.signal), axis=0), np.array(sound.volume) / 100
    )

    # test sample rate and duration setter
    assert sound.sample_rate == 44100
    assert sound.duration == duration
    assert sound.times.size == sound.sample_rate * sound.duration
    sound.sample_rate = 48000
    assert sound.sample_rate == 48000
    assert sound.duration == duration
    assert sound.times.size == sound.sample_rate * sound.duration
    sound.duration = 0.5
    assert sound.sample_rate == 48000
    assert sound.duration == 0.5
    assert sound.times.size == sound.sample_rate * sound.duration


def _test_no_volume(Sound):
    """Test signal if volume is set to 0."""
    sound = Sound(0)
    assert np.allclose(sound.signal, np.zeros(sound.signal.shape))
