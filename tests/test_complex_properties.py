import taglib
from taglib import Picture


def test_mp3_multiple_complex_properties(test_data, tiny_png):
    """Test writing and reading multiple pictures AND GEOB objects.

    Migrated from TagLib's testReadWriteMultipleProperties.
    Tests that different complex property types coexist correctly.
    """
    path = test_data("xing.mp3")

    geob1 = {
        'data': b'First',
        'mimeType': 'text/plain',
        'description': 'Object 1',
        'fileName': 'test1.txt'
    }
    geob2 = {
        'data': b'Second',
        'mimeType': 'text/plain',
        'description': 'Object 2',
        'fileName': 'test2.txt'
    }

    # Write pictures and GEOB objects
    with taglib.File(path) as f:
        assert list(f.complex_property_keys) == []
        f.pictures = [
            Picture(data=tiny_png, mime_type='image/png', description='Cover 1'),
            Picture(data=tiny_png, mime_type='image/png', description='Cover 2',
                    picture_type='Back Cover')
        ]
        f.set_complex_properties('GENERALOBJECT', [geob1, geob2])
        f.save()

    # Read back and verify both types
    with taglib.File(path) as f:
        keys = f.complex_property_keys
        assert 'PICTURE' in keys
        assert 'GENERALOBJECT' in keys

        # Check pictures
        assert len(f.pictures) == 2
        assert f.pictures[0].description == 'Cover 1'
        assert f.pictures[1].description == 'Cover 2'

        # Check GEOB objects
        geobs = f.complex_properties('GENERALOBJECT')
        assert len(geobs) == 2
        assert geobs[0]['data'] == b'First'
        assert geobs[0]['fileName'] == 'test1.txt'
        assert geobs[1]['data'] == b'Second'
        assert geobs[1]['fileName'] == 'test2.txt'


def test_mp3_geob_write_read(test_data):
    """Test writing and reading GEOB (General Encapsulated Object) in MP3.

    Migrated from TagLib's testSetGetId3Geob.
    GEOB frames store arbitrary binary data with MIME type, description, and filename.
    This tests the lower-level complex_properties API with non-picture data.
    """
    path = test_data("xing.mp3")

    geob = {
        'data': b'Just a test',
        'mimeType': 'text/plain',
        'description': 'Embedded object',
        'fileName': 'test.txt'
    }

    # Write GEOB
    with taglib.File(path) as f:
        assert 'GENERALOBJECT' not in f.complex_property_keys
        assert f.complex_properties('GENERALOBJECT') == []
        f.set_complex_properties('GENERALOBJECT', [geob])
        f.save()

    # Read back and verify
    with taglib.File(path) as f:
        assert 'GENERALOBJECT' in f.complex_property_keys
        props = f.complex_properties('GENERALOBJECT')
        assert len(props) == 1
        stored = props[0]
        assert stored['data'] == b'Just a test'
        assert stored['mimeType'] == 'text/plain'
        assert stored['description'] == 'Embedded object'
        assert stored['fileName'] == 'test.txt'
