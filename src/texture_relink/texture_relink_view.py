"""View for the Texture Relink tool."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os.path

from . import maya_utils, texture_relink_controller, texture_relink_model


QtCore, QtGui, QtWidgets, shiboken = maya_utils.import_pyside()


class TextureRelinkView(QtWidgets.QWidget):
    """View class for the Texture Relink tool."""

    def __init__(self, parent=None):
        super(TextureRelinkView, self).__init__(parent)
        self.model = texture_relink_model.TextureRelinkModel()
        self.controller = texture_relink_controller.TextureRelinkController(self.model, self)
        self.init_ui()

    def init_ui(self):
        """Initializes the user interface."""
        layout = QtWidgets.QVBoxLayout(self)

        self.find_button = QtWidgets.QPushButton("Find Missing Textures")
        self.find_button.clicked.connect(self.controller.find_missing_textures)
        layout.addWidget(self.find_button)

        browse_widget = QtWidgets.QWidget(self)
        browse_layout = QtWidgets.QHBoxLayout(browse_widget)
        self.folder_input = QtWidgets.QLineEdit()
        browse_layout.addWidget(self.folder_input)
        self.browse_button = QtWidgets.QPushButton("Browse")
        self.browse_button.clicked.connect(self._browse_folder)
        browse_layout.addWidget(self.browse_button)
        layout.addWidget(browse_widget)

        self.recursive_checkbox = QtWidgets.QCheckBox("Search subfolders recursively")
        layout.addWidget(self.recursive_checkbox)

        self.relink_button = QtWidgets.QPushButton("Relink Textures")
        self.relink_button.clicked.connect(self.relink_textures)
        layout.addWidget(self.relink_button)

        self.result_text = QtWidgets.QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.progress_bar = QtWidgets.QProgressBar()
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.setWindowTitle("Texture Relink")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

    def _browse_folder(self):
        """Open a folder browser dialog."""
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select New Texture Root Directory")
        if folder:
            self.folder_input.setText(os.path.normpath(folder))

    def relink_textures(self):
        """Initiates the texture relinking process."""
        new_root_path = self.folder_input.text()
        if not os.path.exists(new_root_path):
            self._browse_folder()
            new_root_path = self.folder_input.text()

        if new_root_path:
            recursive = self.recursive_checkbox.isChecked()
            self.controller.relink_textures(new_root_path, recursive)

    def display_missing_textures(self, count):
        """Displays the count of missing textures."""
        self.result_text.setText("Found missing textures:\n{0}".format(json.dumps(count, indent=4)))
        self.relink_button.setEnabled(True)

    def update_progress(self, value):
        """Updates the progress bar."""
        self.progress_bar.setValue(value)

    def display_relinked_textures(self, relinked_textures):
        """Displays the results of the relinking process."""
        result = "Relinked {0} textures:\n\n".format(len(relinked_textures))
        for node, new_path in relinked_textures:
            result += "\t-{0}: {1}\n".format(node, new_path)
        self.result_text.setText(result)
