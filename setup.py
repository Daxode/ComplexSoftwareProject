from setuptools import setup, find_packages
import version
from Cython.Build import cythonize

setup(
    name='Nodes Compiling',
    ext_modules=cythonize("Blobtory/Scripts/planet_former/Nodes.pyx"),
    zip_safe=False,
)

# setup(
#     name='A Star Compiling',
#     ext_modules=cythonize("Blobtory/Scripts/planet_former/AStarC.pyx", "Blobtory/Scripts/planet_former/Nodes.pyx"),
#     zip_safe=False,
# )

setup(
    name="Blobtory",
    version=version.version,
    packages=find_packages(include=['Blobtory', 'Blobtory.*']),
    install_requires=[
        'panda3d>=1.10.7',
        'numpy>=1.19.2',
        'setuptools>=50.3.0',
        'multipledispatch>=0.6.0',
        'pip>=20.2.3',
        'six>=1.15.0',
        'cython'
    ],
    options={
        "build_apps": {
            # Files that we want to include. Specifically:
            #  * All of our image-files (.png)
            #  * All of our sound- and music-files (.ogg)
            #  * All of our text-files (.txt)
            #  * All of our 3D models (.egg)
            #    - These will be automatically converted
            #      to .bam files
            #  * And all of our font-files (in the "Font" folder)
            "include_patterns": [
                "**/*.png",
                "**/*.ogg",
                "**/*.txt",
                "**/*.egg",
                "**/*.vert",
                "**/*.frag",
                "**/*.glsl",
                "**/*.ico"
            ],
            # We want a gui-app, and our "main" Python file
            # is "Game.py"
            "gui_apps": {
                "Blobtory": "Blobtory/Scripts/Main.py"
            },
            'log_filename': '$USER_APPDATA/Blobtory/output.log',
            'log_append': False,
            # Plugins that we're using. Specifically,
            # we're using OpenGL, and OpenAL audio
            "plugins": [
                "pandagl",
                "p3openal_audio"
            ],
            # Platforms that we're building for.
            # Remove those that you don't want.
            "platforms": [
                # 'manylinux1_x86_64',
                # 'macosx_10_6_x86_64',
                'win_amd64',
                # 'win32',
            ]
        }
    }
)
