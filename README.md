# Framed Movies
Get the average colour of every frame in a video and create a lovely colour timeline.

### Dependencies
* Python >= 3.5
* PIL (`pip install pillow`)
* OpenCV2 (`pip install opencv-python`)
* Numpy (`pip install numpy`)

### Usage
For a single video: put the video in the directory, run `createImage.py`, follow the prompts and enter your resizing and frame skip settings to configure between speed and accuracy. For a directory of video, simply enter the directory when prompted
Your image(s) will then be processed and placed in the same directory as your source.

### Known issues
* Block of black at the end of the image
This is because credits with a black background with white text, when averaged, create a very dark grey, which creates this block.

### Examples
Bee Movie![Bee Movie](https://github.com/Harrison-Mitchell/Framed-Movies/blob/master/examples/Bee%20Movie.png "Bee Movie")
Nemo![Nemo](https://github.com/Harrison-Mitchell/Framed-Movies/blob/master/examples/Nemo.png "Nemo")
Shrek![Shrek](https://github.com/Harrison-Mitchell/Framed-Movies/blob/master/examples/Shrek.png "Shrek")
