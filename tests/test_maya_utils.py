import pytest
from texture_relink import maya_utils

def test_get_maya_version():
    assert maya_utils.get_maya_version() == 2022

def test_import_pyside():
    QtCore, QtGui, QtWidgets, shiboken = maya_utils.import_pyside()
    assert all(obj is not None for obj in [QtCore, QtGui, QtWidgets, shiboken])

def test_maya_main_window():
    result = maya_utils.maya_main_window()
    assert result is not None

def test_get_file_nodes():
    assert isinstance(maya_utils.get_file_nodes(), list)

def test_get_file_texture_path():
    assert isinstance(maya_utils.get_file_texture_path('dummy_node'), str)

def test_set_file_texture_path():
    maya_utils.set_file_texture_path('dummy_node', '/new/path/texture.jpg')
    # This test just ensures the function runs without error

def test_get_shader_name():
    assert isinstance(maya_utils.get_shader_name('dummy_file_node'), str)

def test_get_file_node_from_shader():
    result = maya_utils.get_file_node_from_shader('dummy_shader')
    assert result is None or isinstance(result, str)