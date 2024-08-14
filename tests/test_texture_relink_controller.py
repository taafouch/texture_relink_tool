import pytest
from texture_relink.texture_relink_controller import TextureRelinkController

@pytest.fixture
def controller(mock_texture_relink_model, mock_texture_relink_view):
    return TextureRelinkController(mock_texture_relink_model, mock_texture_relink_view)

def test_find_missing_textures(controller):
    controller.model.find_missing_textures.return_value = {'shader1': ['/path/texture1.jpg']}
    result = controller.find_missing_textures()
    assert result == {'shader1': ['/path/texture1.jpg']}
    controller.view.display_missing_textures.assert_called_once_with({'shader1': ['/path/texture1.jpg']})

def test_relink_textures(controller):
    def mock_relink_generator():
        yield ('file1', '/new/path/texture1.jpg')
        yield (1, 2)  # Progress update
        yield ('file2', '/new/path/texture2.jpg')
        yield (2, 2)  # Progress update

    controller.model.relink_textures.return_value = mock_relink_generator()
    result = controller.relink_textures('/new/path', False)
    assert result == [('file1', '/new/path/texture1.jpg'), ('file2', '/new/path/texture2.jpg')]
    controller.view.update_progress.assert_called_with(100)
    controller.view.display_relinked_textures.assert_called_once_with([
        ('file1', '/new/path/texture1.jpg'),
        ('file2', '/new/path/texture2.jpg')
    ])