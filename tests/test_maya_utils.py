import pytest
import mock
from texture_relink import maya_utils


@pytest.fixture(autouse=True)
def mock_maya(monkeypatch):
    mock_cmds = mock.MagicMock()
    mock_cmds.ls.return_value = ["file1", "file2"]
    mock_cmds.getAttr.return_value = "/path/to/texture.jpg"
    mock_cmds.listConnections.side_effect = [["shader1"]]
    mock_cmds.nodeType.return_value = "phong"

    monkeypatch.setattr("texture_relink.maya_utils.cmds", mock_cmds)
    monkeypatch.setattr("texture_relink.maya_utils.omui", mock.MagicMock())


def test_get_maya_version():
    with mock.patch("texture_relink.maya_utils.cmds.about", return_value="2022"):
        assert maya_utils.get_maya_version() == 2022


def test_import_pyside():
    QtCore, QtGui, QtWidgets, shiboken = maya_utils.import_pyside()
    assert all(isinstance(obj, mock.MagicMock) for obj in [QtCore, QtGui, QtWidgets, shiboken])


def test_maya_main_window():
    result = maya_utils.maya_main_window()
    assert isinstance(result, mock.MagicMock)


def test_get_file_nodes():
    result = maya_utils.get_file_nodes()
    assert isinstance(result, list)
    assert result == ["file1", "file2"]


def test_get_file_texture_path():
    result = maya_utils.get_file_texture_path("dummy_node")
    assert isinstance(result, str)
    assert result == "/path/to/texture.jpg"


def test_set_file_texture_path():
    maya_utils.set_file_texture_path("dummy_node", "/new/path/texture.jpg")
    maya_utils.cmds.setAttr.assert_called_once_with("dummy_node.fileTextureName", "/new/path/texture.jpg",
                                                    type="string")


def test_get_shader_name():
    result = maya_utils.get_shader_name("dummy_file_node")
    assert isinstance(result, str)
    assert result == "shader1"


def test_get_file_node_from_shader():
    with mock.patch("texture_relink.maya_utils.cmds.listConnections", return_value=["file1"]):
        result = maya_utils.get_file_node_from_shader("dummy_shader")
        assert isinstance(result, str)
        assert result == "file1"

    # Test the case where no file node is found
    with mock.patch("texture_relink.maya_utils.cmds.listConnections", return_value=[]):
        result = maya_utils.get_file_node_from_shader("dummy_shader")
        assert result is None


if __name__ == "__main__":
    pytest.main(["-v", __file__])
