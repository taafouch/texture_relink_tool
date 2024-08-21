"""Controller for the Texture Relink tool."""

from __future__ import absolute_import, division, print_function


class TextureRelinkController:
    """Controller class for the Texture Relink tool."""

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def find_missing_textures(self):
        """Finds missing textures using the model."""
        missing_textures = self.model.find_missing_textures()
        self.view.display_missing_textures(missing_textures)
        return missing_textures

    def relink_textures(self, new_root_path, recursive=False):
        """Relinks textures using the model."""
        relink_generator = self.model.relink_textures(new_root_path, recursive)
        relinked_textures = []

        for item in relink_generator:
            if isinstance(item, tuple) and len(item) == 2:
                if isinstance(item[0], int):
                    # This is a progress update
                    current, total = item
                    self.view.update_progress(int(current / total * 100))
                else:
                    # This is a relinked texture
                    relinked_textures.append(item)

        self.view.display_relinked_textures(relinked_textures)
        return relinked_textures
