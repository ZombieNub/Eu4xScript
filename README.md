# Eu4xScript

Hello! This is a python script for Europa Universalis 4 that's intended to make the creation of x2, x5, x10, and x100 mods much easier. I'm doing this as I personally enjoy x10 mods, and also because I need to become more experienced at Python. Currently, the script file is slow and inefficient, but it gets the job done.

Current goals:
1. Replace the filter list or rework how it's handled to make the program run faster without losing functionality
2. Rework how the program finds modifiers to prevent unintended script modifications and trim the filter list
3. Add docstrings and comments to make the script file more readable.

# Script Instructions

Requirements: Python 3

1. Create a folder with each folder you want to modify. Files in subdirectories are also modified.
2. Run the following command in the command prompt:

`python main.py [folder name] [scale]`

Folder name is the name of the folder where the files are stored.

Scale is the factor that each modifier is multiplied by.

The results will be stored in a folder called `output_x[scale]`. To run this, simply copy it's contents into an Eu4 mod folder.