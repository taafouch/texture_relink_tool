import pytest
import mock
import os

# Mock the maya_utils module
mock_maya_utils = mock.MagicMock()
mock_maya_utils.get_file_nodes.return_value = ['file1', 'file2']
mock_maya_utils.get_file_texture_path.return_value = '/fake/path/texture.jpg'
mock_maya_utils.get_shader_name.return_value = 'shader1'


# Patch the maya_utils import in the texture_relink_model module
@mock.patch('texture_relink.texture_relink_model.maya_utils', mock_maya_utils)
@pytest.fixture
def model():
    from texture_relink.texture_relink_model import TextureRelinkModel
    return TextureRelinkModel()


def test_find_missing_textures(model):
    # Set up the mock to simulate a missing texture
    mock_maya_utils.get_file_texture_path.return_value = '/non/existent/path.jpg'

    result = model.find_missing_textures()
    assert isinstance(result, dict)
    assert 'shader1' in result
    assert '/non/existent/path.jpg' in result['shader1']


def test_relink_textures(model, tmpdir):
    # Create a temporary texture file
    new_root = tmpdir.mkdir("new_textures")
    new_file = new_root.join("texture.jpg")
    new_file.write("dummy content")

    # Set up the mock to simulate finding the new texture
    def mock_find_texture(root_path, file_name, recursive):
        return os.path.join(str(new_root), file_name)

    with mock.patch.object(model, 'find_texture', side_effect=mock_find_texture):
        result = list(model.relink_textures(str(new_root), recursive=True))

    assert len(result) > 0
    assert any(isinstance(item[0], basestring) for item in result)  # Check for relinked textures
    assert any(isinstance(item[0], int) for item in result)  # Check for progress updates


if __name__ == '__main__':
    pytest.main(['-v', __file__])