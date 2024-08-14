import os
import sys
import shutil
from os.path import join, dirname, abspath

def get_maya_module_path():
    """Get the Maya modules directory path."""
    if sys.platform == "win32":
        return join(os.environ['USERPROFILE'], "Documents", "maya", "modules")
    elif sys.platform == "darwin":
        return join(os.path.expanduser("~"), "Library", "Preferences", "Autodesk", "maya", "modules")
    else:  # linux
        return join(os.path.expanduser("~"), "maya", "modules")

def create_module_file(module_path, script_dir):
    """Create the .mod file for the Texture Relink Tool."""
    mod_content = f"""+ MAYAVERSION:2016 TextureRelinkTool 1.0 {script_dir}
scripts: {script_dir}"""
    
    with open(join(module_path, "TextureRelinkTool.mod"), "w") as mod_file:
        mod_file.write(mod_content)

def copy_script_files(script_dir):
    """Copy the Texture Relink Tool scripts to the module directory."""
    source_dir = join(dirname(abspath(__file__)), "..", "src", "texture_relink")
    if not os.path.exists(script_dir):
        os.makedirs(script_dir)
    
    for file in os.listdir(source_dir):
        if file.endswith(".py"):
            shutil.copy2(join(source_dir, file), script_dir)

def main():
    maya_module_path = get_maya_module_path()
    if not os.path.exists(maya_module_path):
        os.makedirs(maya_module_path)
    
    script_dir = join(maya_module_path, "TextureRelinkTool", "scripts")
    
    copy_script_files(script_dir)
    create_module_file(maya_module_path, script_dir)
    
    print("Texture Relink Tool has been installed successfully.")
    print(f"Module file created at: {join(maya_module_path, 'TextureRelinkTool.mod')}")
    print(f"Script files copied to: {script_dir}")
    print("Please restart Maya for the changes to take effect.")

if __name__ == "__main__":
    main()
