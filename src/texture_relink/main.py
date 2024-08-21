"""Main file to launch the Texture Relink tool."""

from __future__ import absolute_import, division, print_function


from . import maya_utils, texture_relink_view


QtCore, QtGui, QtWidgets, shiboken = maya_utils.import_pyside()


class TextureRelinkWindow(QtWidgets.QDialog):
    """Singleton window for Texture Relink."""

    _instance = None

    @classmethod
    def get_instance(cls, parent=None):
        if not cls._instance:
            cls._instance = TextureRelinkWindow(parent)
        return cls._instance

    def __init__(self, parent=None):
        super(TextureRelinkWindow, self).__init__(parent)
        self.view = texture_relink_view.TextureRelinkView(self)
        self.setLayout(self.view.layout())
        self.setWindowTitle(self.view.windowTitle())
        self.setMinimumSize(self.view.minimumSize())

    def closeEvent(self, event):
        """Override close event to delete the instance."""
        TextureRelinkWindow._instance = None
        super(TextureRelinkWindow, self).closeEvent(event)


def main():
    """Main function to run the Texture Relink tool."""
    parent = maya_utils.maya_main_window()
    dialog = TextureRelinkWindow.get_instance(parent)
    dialog.show()
    dialog.raise_()
    dialog.activateWindow()


if __name__ == "__main__":
    main()
