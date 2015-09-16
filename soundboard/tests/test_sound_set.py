from soundboard.sounds import SoundSet, SoundInterface


def test_1():
    s = SoundSet('test')
    assert len(s.sounds) == 4
    assert all(isinstance(s, SoundInterface) for s in s.sounds.values())
