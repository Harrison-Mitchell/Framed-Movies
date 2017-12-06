from PIL import Image, ImageDraw
from timeit import default_timer as timer
import cv2, datetime

# ask for video path
src = input("Source: ")
# as we are averaging the color of every single pixel in a frame
# the process can be sped up by downsizing frames, thus less pixels
speed = int(input("Speed (1-32) (Rec:16): "))
# at ~30 frames a second, if every pixel took up a colum, it would
# be a very wide image, so skip every x frames
every = int(input("Every n frames (1-8) (Rec:4): "))
# if left blank, apply defaults
if every == None:
	speed = 16
if every == None:
	every = 4
	
# get the number, width and height of frames and create a blank image
vidcap = cv2.VideoCapture(src)
frames = round(int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) / every)
w = round(int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)) / speed)
h = round(int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)) / speed)
newIm = Image.new("RGB", ((frames + 100),1))
pixels = w * h
everyCount = 0

start = timer()

for i in range(frames * every):
	

	# can't range every x frames as vidcap.read() only gets the next frame
	# so every frame needs to be read regardless of whether we're skipping them
	everyCount += 1
	success, image = vidcap.read()
	if everyCount == every:
		everyCount = 0
		if success:
			avR = 0
			avG = 0
			avB = 0
			# PIL can't read CV2 images, so save it and reopen
			cv2.imwrite("buffer.png", image)
			im = Image.open("buffer.png")
			# we can skip resizing if unneccesary
			if speed != 1:
				im = im.resize((w,h))
			# loop over every pixel and tally the R, G and B values
			for x in range(w):
				for y in range(h):
					avR += im.getpixel((x,y))[0]
					avG += im.getpixel((x,y))[1]
					avB += im.getpixel((x,y))[2]
			newIm.putpixel((round(i / every), 0), (round(avR/pixels), round(avG/pixels), round(avB/pixels)))
			# every so often print our progress
			if (i + 1) % 100 == 0:
				print(str(round(((i + 1) / (frames * every)) * 100, 1)) + "%")
		# if the frame can't be read then we've reached the end of the video
		# it's done this way as frame count can be inaccurate
		else:
			break

# show how long processing took
end = timer()
print("\nDone in", str(datetime.timedelta(seconds = round(end - start))))

# we made the blank image slightly larger than necessary as frame count is innacurate
# so trim black pixels from the left
while sum(newIm.getpixel((0,0))) == 0:
	newIm = newIm.crop((1, 0, newIm.size[0], 1))
# and then from the right
while sum(newIm.getpixel((newIm.size[0] - 1,0))) == 0:
	newIm = newIm.crop((0, 0, newIm.size[0] - 1, 1))
# resize the image to something managable
newIm = newIm.resize((8000, 500))
# save/name our image the same as the source
newIm.save(src.split(".")[0] + ".png")