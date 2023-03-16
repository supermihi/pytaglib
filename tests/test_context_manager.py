import taglib


def test_exit_closes_file(test_file):
    with test_file("r2.mp3") as f:
        assert not f.is_closed
    assert f.is_closed


def test_exit_saves_if_requested(test_data):
    file = test_data("r2.mp3")
    with taglib.File(file, save_on_exit=True) as f:
        f.tags["ARTIST"] = ["overridden"]
    with taglib.File(file) as f:
        assert f.tags["ARTIST"] == ["overridden"]


def test_exit_does_not_save_if_not_requested(test_data):
    file = test_data("r2.mp3")
    with taglib.File(file, save_on_exit=False) as f:
        f.tags["ARTIST"] = ["overridden"]
    with taglib.File(file) as f:
        assert "ARTIST" not in f.tags
