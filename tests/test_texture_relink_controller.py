import pytest
import mock
from texture_relink.texture_relink_controller import TextureRelinkController


@pytest.fixture
def mock_model():
    model = mock.MagicMock()
    model.find_missing_textures.return_value = {'shader1': ['/path/texture1.jpg']}

    def mock_relink_generator():
        yield ('file1', '/new/path/texture1.jpg')
        yield (1, 2)  # Progress update
        yield ('file2', '/new/path/texture2.jpg')
        yield (2, 2)  # Progress update

    model.relink_textures.return_value = mock_relink_generator()
    return model


@pytest.fixture
def mock_view():
    return mock.MagicMock()


@pytest.fixture
def controller(mock_model, mock_view):
    return TextureRelinkController(mock_model, mock_view)


def test_find_missing_textures(controller, mock_model, mock_view):
    result = controller.find_missing_textures()
    assert result == {'shader1': ['/path/texture1.jpg']}
    mock_view.display_missing_textures.assert_called_once_with({'shader1': ['/path/texture1.jpg']})


def test_relink_textures(controller, mock_model, mock_view):
    result = controller.relink_textures('/new/path', False)
    assert result == [('file1', '/new/path/texture1.jpg'), ('file2', '/new/path/texture2.jpg')]
    mock_view.update_progress.assert_called_with(100)
    mock_view.display_relinked_textures.assert_called_once_with([
        ('file1', '/new/path/texture1.jpg'),
        ('file2', '/new/path/texture2.jpg')
    ])


if __name__ == '__main__':
    pytest.main(['-v', __file__])