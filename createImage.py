from PIL import Image, ImageDraw
from timeit import default_timer as timer
import cv2, datetime, os
import numpy as np

# ask for video path
src = input("Source: ")
# as we are averaging the color of every single pixel in a frame
# the process can be sped up by downsizing frames, thus less pixels
speed = input("Speed (1-32) [16]: ")
# at ~30 frames a second, if every pixel took up a column, it would
# be a very wide image, so skip every x frames
every = input("Every n frames (1-8) [4]: ")
# if left blank, apply defaults
speed = 16 if speed == "" else int(speed)
every = 4 if every == "" else int(every)
	
def makeImage (src):
	# get the number, width and height of frames and create a blank image
	vidcap = cv2.VideoCapture(src)
	frames = round(int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) / every)
	newIm = Image.new("RGB", ((frames + 100),1))
	everyCount = 0

	start = timer()
	print(frames, "frames to process")
	for i in range(frames * every):
		# can't range every x frames as vidcap.read() only gets the next frame
		# so every frame needs to be read regardless of whether we're skipping them
		everyCount += 1
		success, image = vidcap.read()
		if everyCount % every == 0:
			if not success: break # break if we reach the end of the video
			image = cv2.resize(image, (0,0), fx=1/speed, fy=1/speed) 
			avR, avG, avB = np.mean(image, axis=(0, 1))
			newIm.putpixel((int(i / every), 0), (int(avR),int(avG),int(avB)))
			# every so often print our progress
			if (i + 1) % 2500 == 0: print(str(round(((i + 1) / (frames * every)) * 100, 1)) + "%")

	# show how long processing took
	end = timer()
	print("\nDone in", str(datetime.timedelta(seconds = round(end - start))))

	# we made the blank image slightly larger than necessary as frame count is innacurate
	# so trim black pixels from the left
	while sum(newIm.getpixel((0,0))) == 0: newIm = newIm.crop((1, 0, newIm.size[0], 1))
	# and then from the right
	while sum(newIm.getpixel((newIm.size[0] - 1,0))) == 0: newIm = newIm.crop((0, 0, newIm.size[0] - 1, 1))
	# resize the image to something managable
	newIm = newIm.resize((8000, 500))
	# save/name our image the same as the source
	newIm.save(src.split(".")[0] + ".png")

# if provided a single file, otherwise
if "." in src: makeImage(src)
else:
	src = src + "/" if src[-1] != "/" else src # ensure directory / is there
	for mov in os.listdir(src): makeImage(src + mov) # create image for each video
