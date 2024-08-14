# Texture Relink Tool for Maya

## Overview

The Texture Relink Tool is a Python-based utility for Autodesk Maya that helps artists find and re-link missing textures in a scene. It provides both a user-friendly interface and programmatic access to locate missing textures, display them grouped by shader, and update their paths in the Maya scene.

## Features

- Find missing textures in the current Maya scene
- Display missing textures grouped by shader
- Browse for a new texture root directory
- Relink missing textures to the new directory
- Option to search subfolders recursively
- Progress bar to track the relinking process
- Compatible with Maya 2016 and later
- Programmatic access to core functionality

## Installation

1. Clone or download this repository to your local machine.
2. Copy the `texture_relink` folder to your Maya scripts directory:
   - Windows: `C:\Users\<username>\Documents\maya\<version>\scripts`
   - macOS: `/Users/<username>/Library/Preferences/Autodesk/maya/<version>/scripts`
   - Linux: `/home/<username>/maya/<version>/scripts`

## Usage

### Using the GUI

1. In Maya, open the Script Editor and run the following Python code:

```python
from texture_relink import main
main.main()
```

2. The Texture Relink Tool window will appear.
3. Click "Find Missing Textures" to locate missing textures in the scene.
4. Browse for the new texture root directory.
5. (Optional) Check "Search subfolders recursively" if your textures are in subdirectories.
6. Click "Relink Textures" to update the texture paths.
7. The tool will display the results of the relinking process.

### Programmatic Usage

You can also use the core functionality of the Texture Relink Tool without the GUI. Here's how to use it programmatically:

```python
from texture_relink.texture_relink_model import TextureRelinkModel

# Create an instance of the model
model = TextureRelinkModel()

# Find missing textures
missing_textures = model.find_missing_textures()
print("Missing textures:", missing_textures)

# Relink textures
new_root_path = "/path/to/new/texture/directory"
recursive = True  # Set to False if you don't want to search subdirectories

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
```

This script demonstrates how to:
1. Find missing textures using `find_missing_textures()`
2. Relink textures using `relink_textures()`
3. Process the results, including handling progress updates

You can integrate this into your own scripts or use it as part of a larger automation process.

## Development

### Prerequisites

- Maya 2016 or later
- Python 2.7 or 3.7+ (depending on Maya version)
- PySide or PySide2 (included with Maya)

### Project Structure

```
texture_relink/
│
├── main.py
├── maya_utils.py
├── texture_relink_controller.py
├── texture_relink_model.py
└── texture_relink_view.py
```

### Running Tests

To run the unit tests in a standalone Python 2.7 environment:

1. Install the required packages:
   ```
   pip install pytest mock
   ```

2. Navigate to the project's test directory.

3. Run the tests using:
   ```
   pytest -v
   ```

Note: The tests use mocks to simulate the Maya environment and can be run without Maya installed.

## Contributing

Contributions to the Texture Relink Tool are welcome! Please feel free to submit a Pull Request.

### Guidelines for contributing:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write tests for your changes.
4. Ensure all tests pass before submitting a pull request.
5. Update the documentation if you're introducing new features or changing functionality.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Autodesk Maya
- PySide/PySide2 for the GUI
- The Maya Python API

## Support

If you encounter any issues or have questions, please file an issue on the GitHub repository.

## Authors

[Mohamed EL Wafi]

---

We hope this tool helps streamline your texture management workflow in Maya. Happy texturing!
