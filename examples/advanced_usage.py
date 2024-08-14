# Advanced usage example for Texture Relink Tool

import maya.cmds as cmds
from texture_relink.texture_relink_model import TextureRelinkModel

def create_sample_scene():
    # Create two polygon spheres
    cmds.polySphere(name='sphere1')
    cmds.polySphere(name='sphere2')
    
    # Create two lambert materials and assign them to the spheres
    for i in range(1, 3):
        shader = cmds.shadingNode('lambert', asShader=True, name=f'lambert{i}')
        cmds.select(f'sphere{i}')
        cmds.hyperShade(assign=shader)
        
        # Create a file node and connect it to the lambert's color
        file_node = cmds.shadingNode('file', asTexture=True, name=f'file{i}')
        cmds.connectAttr(file_node + '.outColor', shader + '.color')
        
        # Set a non-existent texture path
        cmds.setAttr(file_node + '.fileTextureName', f'/non/existent/path/texture{i}.jpg', type='string')

def relink_textures_programmatically():
    model = TextureRelinkModel()
    
    # Find missing textures
    missing_textures = model.find_missing_textures()
    print("Missing textures:", missing_textures)
    
    # Relink textures
    new_root_path = "/path/to/your/texture/directory"  # Update this path
    recursive = True
    
    relink_generator = model.relink_textures(new_root_path, recursive)
    
    # Process the results
    for item in relink_generator:
        if isinstance(item, tuple) and len(item) == 2:
            if isinstance(item[0], int):
                # This is a progress update
                current, total = item
                progress_percentage = (current / total) * 100
                print("Progress: {:.2f}%".format(progress_percentage))
            else:
                # This is a relinked texture
                node, new_path = item
                print("Relinked: {} -> {}".format(node, new_path))
    
    print("Texture relinking complete!")

if __name__ == "__main__":
    create_sample_scene()
    relink_textures_programmatically()
