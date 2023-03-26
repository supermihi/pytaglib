import pytest


def test_properties_fail_after_close(test_file):
    tf = test_file("r2.mp3")
    tf.close()
    with pytest.raises(ValueError):
        _ = tf.readOnly
    with pytest.raises(ValueError):
        _ = tf.bitrate
    with pytest.raises(ValueError):
        _ = tf.length
    with pytest.raises(ValueError):
        _ = tf.channels
    with pytest.raises(ValueError):
        _ = tf.sampleRate


def test_close_fails_after_close(test_file):
    tf = test_file("r2.mp3")
    tf.close()
    with pytest.raises(ValueError):
        tf.close()
