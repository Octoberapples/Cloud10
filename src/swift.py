from swiftclient.service import SwiftService, SwiftUploadObject


class SwiftException(Exception):
    pass


def _ensure_success(responses):
    """
    Helper function for ensuring that all the responses
    succeeded, and if not, raising appriopiate exceptions.
    """
    for r in responses:
        if not r['success']:
            raise SwiftException('Swift error: {}'.format(r['error']))


def upload_object(container, object_name, f):
    """Uploads the file object `f` to a Swift `container` as `object_name`."""
    with SwiftService() as swift:
        objs = [
            SwiftUploadObject(
                f, object_name=object_name
            )
        ]
        responses = swift.upload(container, objs)
        _ensure_success(responses)


def search_for_object(container, object_name):
    """Search for object in container, returns true if found"""
    with SwiftService() as swift:

        list_gen = swift.list(container=container)
        for page in list_gen:
            if page["success"]:
                for item in page["listing"]:
                    if object_name == item["name"]:
                        return True
            else:
                raise SwiftException('Error')
    return False


def download_object(container, object_name):
    """Downloads object `object_name` from a Swift `container`."""
    with SwiftService() as swift:
        responses = swift.download(container, [object_name])
        _ensure_success(responses)


def delete_object(container, object_name):
    """Removes object `object_name` from a Swift `container`."""
    with SwiftService() as swift:
        responses = swift.delete(container, [object_name])
        _ensure_success(responses)


if __name__ == '__main__':
    import tempfile
    import os

    with tempfile.NamedTemporaryFile() as f:
        f.write('randomcontent')
        f.seek(0)
        upload_object('container1337', 'testfile', f)

    assert search_for_object('container1337', 'testfile')

    download_object('container1337', 'testfile')
    assert os.path.exists('testfile')

    with open('testfile') as f:
        assert f.read() == 'randomcontent'

    delete_object('container1337', 'testfile')
