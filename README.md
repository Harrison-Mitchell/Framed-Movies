# Framed-Movies
Get the average color of every frame in a video and create a lovely color timeline

# Dependencies
* Python >= 3.5
* PIL
> pip install Pillow
* OpenCV2
> pip install opencv-python

# Usage
Put your desired video in the directory, run the python script, drag your file into the command window, then pick your scaling and frame skip settings or leave blank for default.
Your image will then be processed and placed in the same directory.

# Known issues
* Block of black at the end of the image
This is because credits with a black background with white text, when averaged, create a very dark grey, which creates this block.

# Examples
