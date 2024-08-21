import pytest
import os
from texture_relink.texture_relink_model import TextureRelinkModel


class MockMayaUtils:
    def get_file_nodes(self):
        return ["file1", "file2"]

    def get_file_texture_path(self, node):
        paths = {
            "file1": "/path/to/texture1.jpg",
            "file2": "/path/to/texture2.jpg"
        }
        return paths.get(node, "")

    def get_shader_name(self, node):
        shaders = {
            "file1": "shader1",
            "file2": "shader2"
        }
        return shaders.get(node, "")

    def get_file_node_from_shader(self, shader):
        return "file_node"

    def set_file_texture_path(self, node, path):
        pass


@pytest.fixture
def mock_maya_utils(monkeypatch):
    mock_utils = MockMayaUtils()
    monkeypatch.setattr("texture_relink.texture_relink_model.maya_utils", mock_utils)
    return mock_utils


@pytest.fixture
def texture_relink_model():
    return TextureRelinkModel()


def test_find_missing_textures(texture_relink_model, monkeypatch, mock_maya_utils):
    def mock_exists(path):
        return path == "/path/to/texture2.jpg"

    monkeypatch.setattr(os.path, "exists", mock_exists)

    result = texture_relink_model.find_missing_textures()
    assert result == {"shader1": ["/path/to/texture1.jpg"]}


def test_relink_textures(monkeypatch, texture_relink_model, mock_maya_utils):
    def mock_find_missing_textures(self):
        return {
            "shader1": ["/old/path/texture1.jpg"],
            "shader2": ["/old/path/texture2.jpg", "/old/path/texture3.jpg"]
        }

    def mock_find_texture(self, root_path, file_name, recursive):
        if file_name == "texture1.jpg":
            return "/new/path/texture1.jpg"
        elif file_name == "texture2.jpg":
            return "/new/path/texture2.jpg"
        else:
            return None

    monkeypatch.setattr(TextureRelinkModel, "find_missing_textures", mock_find_missing_textures)
    monkeypatch.setattr(TextureRelinkModel, "find_texture", mock_find_texture)

    result = list(texture_relink_model.relink_textures("/new/path", recursive=True))
    print(result)
    assert result == [("file1", "/new/path/texture1.jpg"),
                      (1, 2),
                      ("file2", "/new/path/texture2.jpg"),
                      (2, 2)]


def test_find_texture(texture_relink_model, tmp_path):
    # Create a temporary directory structure
    sub_dir = tmp_path / "subdir"
    sub_dir.mkdir()
    (tmp_path / "texture1.jpg").touch()
    (sub_dir / "texture2.jpg").touch()

    # Test finding a texture in the root directory
    result = texture_relink_model.find_texture(str(tmp_path), "texture1.jpg", False)
    assert result == str(tmp_path / "texture1.jpg")

    # Test finding a texture in a subdirectory with recursive search
    result = texture_relink_model.find_texture(str(tmp_path), "texture2.jpg", True)
    assert result == str(sub_dir / "texture2.jpg")

    # Test not finding a texture
    result = texture_relink_model.find_texture(str(tmp_path), "nonexistent.jpg", True)
    assert result is None

    # Test non-recursive search doesn"t find texture in subdirectory
    result = texture_relink_model.find_texture(str(tmp_path), "texture2.jpg", False)
    assert result is None
