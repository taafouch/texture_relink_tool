"""Utility functions for Maya operations."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from maya import cmds
    import maya.OpenMayaUI as omui

    MAYA_AVAILABLE = True
except ImportError:
    import mock

    cmds = mock.MagicMock()
    omui = mock.MagicMock()
    MAYA_AVAILABLE = False


def get_maya_version():
    """Get the current Maya version."""
    if MAYA_AVAILABLE:
        return int(cmds.about(version=True))
    else:
        return 2022  # Default to a recent version for testing


def import_pyside():
    """Import the appropriate PySide and Shiboken modules based on Maya version."""
    maya_version = get_maya_version()

    if not MAYA_AVAILABLE:
        # Mock PySide and Shiboken for testing
        mock_pyside = mock.MagicMock()
        mock_shiboken = mock.MagicMock()
        return mock_pyside, mock_pyside, mock_pyside, mock_shiboken

    if maya_version < 2017:
        # Maya 2016 and earlier use PySide and Shiboken
        from PySide import QtCore, QtGui
        import shiboken
        QtWidgets = QtGui
        print("Using PySide and Shiboken with Maya {}".format(maya_version))
    elif 2017 <= maya_version < 2022:
        # Maya 2017-2021 use PySide2 and Shiboken2
        from PySide2 import QtCore, QtGui, QtWidgets
        import shiboken2 as shiboken
        print("Using PySide2 and Shiboken2 with Maya {}".format(maya_version))
    else:
        # Maya 2022 and later use PySide6 and Shiboken6
        from PySide6 import QtCore, QtGui, QtWidgets
        import shiboken6 as shiboken
        print("Using PySide6 and Shiboken6 with Maya {}".format(maya_version))

    return QtCore, QtGui, QtWidgets, shiboken


def maya_main_window():
    """Return the Maya main window widget as a Python object."""
    if not MAYA_AVAILABLE:
        return mock.MagicMock()  # Return a mock object for testing

    QtCore, QtGui, QtWidgets, shiboken = import_pyside()
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


def get_file_nodes():
    """Returns all file nodes in the scene."""
    return cmds.ls(type='file')


def get_file_texture_path(node):
    """Returns the texture path for a given file node."""
    return cmds.getAttr('{0}.fileTextureName'.format(node))


def set_file_texture_path(node, path):
    """Sets the texture path for a given file node."""
    cmds.setAttr('{0}.fileTextureName'.format(node), path, type='string')


def get_shader_name(file_node):
    """Returns the name of the shader connected to the file node."""
    connections = cmds.listConnections(file_node, plugs=True, source=False, destination=True)

    if not connections:
        return "Unknown Shader"
    for conn in connections:
        connected_node = conn.split('.')[0]  # Extract the node name from the connection
        node_type = cmds.nodeType(connected_node)

        # Check if the connected node is a shader
        if node_type in ["lambert", "blinn", "phong", "phongE", "surfaceShader", "aiStandardSurface"]:
            return connected_node
    return "Unknown Shader"


def get_file_node_from_shader(shader_name):
    """Returns the file node connected to the given shader."""
    connections = cmds.listConnections(shader_name, type='file')
    if connections:
        return connections[0]
    return None
