"""Model for the Texture Relink tool."""

from __future__ import absolute_import, division, print_function

import os

from . import maya_utils


class TextureRelinkModel:
    """Model class for finding and re-linking missing textures in Maya scenes."""

    def __init__(self):
        self.missing_textures = dict()

    def find_missing_textures(self):
        """Finds all missing textures in the scene."""
        self.missing_textures = dict()
        file_nodes = maya_utils.get_file_nodes()
        for node in file_nodes:
            file_texture_path = maya_utils.get_file_texture_path(node)
            if os.path.exists(file_texture_path):
                continue
            shader_name = maya_utils.get_shader_name(node)
            if shader_name not in list(self.missing_textures.keys()):
                self.missing_textures[shader_name] = []
            self.missing_textures[shader_name].append(file_texture_path)
        return self.missing_textures

    def relink_textures(self, new_root_path, recursive=False):
        """Re-links missing textures to a new root path."""
        total_file_nodes = maya_utils.get_file_nodes()
        for i, node in enumerate(total_file_nodes):
            old_path = maya_utils.get_file_texture_path(node)
            file_name = os.path.basename(old_path)
            new_path = self.find_texture(new_root_path, file_name, recursive)

            if new_path:
                maya_utils.set_file_texture_path(node, new_path)
                yield (node, new_path)

            yield (i + 1, len(total_file_nodes))

    @staticmethod
    def find_texture(root_path, file_name, recursive):
        """Finds a texture file in the given root path."""
        for root, dirs, files in os.walk(root_path):
            if file_name in files:
                return os.path.join(root, file_name)
            if not recursive:
                break
        return None
