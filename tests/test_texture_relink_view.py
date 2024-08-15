import pytest
import mock


# Mock TextureRelinkView class
class MockTextureRelinkView:
    def __init__(self):
        self.find_button = mock.MagicMock()
        self.folder_input = mock.MagicMock()
        self.browse_button = mock.MagicMock()
        self.recursive_checkbox = mock.MagicMock()
        self.relink_button = mock.MagicMock()
        self.result_text = mock.MagicMock()
        self.progress_bar = mock.MagicMock()
        self._plain_text = ""

    def display_missing_textures(self, missing_textures):
        self._plain_text = str(missing_textures)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def display_relinked_textures(self, relinked_textures):
        self._plain_text = "\n".join(["{node}: {path}".format(node=node, path=path)
                                      for node, path in relinked_textures])


@pytest.fixture
def view():
    return MockTextureRelinkView()


def test_init(view):
    assert hasattr(view, "find_button")
    assert hasattr(view, "folder_input")
    assert hasattr(view, "browse_button")
    assert hasattr(view, "recursive_checkbox")
    assert hasattr(view, "relink_button")
    assert hasattr(view, "result_text")
    assert hasattr(view, "progress_bar")


def test_display_missing_textures(view):
    missing_textures = {"shader1": ["/path/texture1.jpg"]}
    view.display_missing_textures(missing_textures)
    assert "shader1" in view._plain_text
    assert "/path/texture1.jpg" in view._plain_text


def test_update_progress(view):
    view.update_progress(50)
    view.progress_bar.setValue.assert_called_once_with(50)


def test_display_relinked_textures(view):
    relinked_textures = [("file1", "/new/path/texture1.jpg"), ("file2", "/new/path/texture2.jpg")]
    view.display_relinked_textures(relinked_textures)
    assert "file1: /new/path/texture1.jpg" in view._plain_text
    assert "file2: /new/path/texture2.jpg" in view._plain_text
