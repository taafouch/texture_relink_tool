# Basic usage example for Texture Relink Tool

import maya.cmds as cmds
from texture_relink import main

def create_sample_scene():
    # Create a simple polygon sphere
    cmds.polySphere()
    
    # Create a lambert material and assign it to the sphere
    shader = cmds.shadingNode('lambert', asShader=True)
    cmds.select('pSphere1')
    cmds.hyperShade(assign=shader)
    
    # Create a file node and connect it to the lambert's color
    file_node = cmds.shadingNode('file', asTexture=True)
    cmds.connectAttr(file_node + '.outColor', shader + '.color')
    
    # Set a non-existent texture path
    cmds.setAttr(file_node + '.fileTextureName', '/non/existent/path/texture.jpg', type='string')

def run_texture_relink_tool():
    main.main()

if __name__ == "__main__":
    create_sample_scene()
    run_texture_relink_tool()
    print("Now use the Texture Relink Tool GUI to find and relink the missing texture.")
