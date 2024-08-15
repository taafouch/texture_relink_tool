from setuptools import setup, find_packages

setup(
    name="TextureRelinkTool",
    version="1.0.0",
    author="Your Name",
    author_email="med.wafi@gmail.com",
    description="A tool for finding and relinking missing textures in Maya",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/taafouch/texture_relink_tool",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=2.7",
    install_requires=[
        # Add any dependencies here. 
        # Note: typically, you wouldn't include Maya-specific libraries
        # as they're provided by the Maya environment.
    ],
    entry_points={
        "console_scripts": [
            "texture_relink=texture_relink.main:main",
        ],
    },
)
