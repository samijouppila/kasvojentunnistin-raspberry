# import the necessary packages

from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image

import imutils
import face_recognition
import pickle
import cv2
import time


# construct the argument parser and parse the arguments

#Initialize camera

def recognizeUser(fileName):
	camera = PiCamera()
	rawCapture = PiRGBArray(camera)



	# Detection method: hog or cnn, hog for performance reasons
	detection_method = "hog"

	# load face encodings
	print("[INFO] loading encodings and face detector...")
	data = pickle.loads(open("encodings.pickle", "rb").read())
	# OpenCV's Haar Cascade for face detection
	detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

	# Use a picture taken from PiCamera
	print("[INFO] taking picture...")
	time.sleep(0.1)
	camera.capture(rawCapture, format = "rgb")
	camera.close()
	image = rawCapture.array
	resized = imutils.resize(image, width=500)

	# Gray color for face detection, rgb for face recognition
	gray = cv2.cvtColor(resized, cv2.COLOR_RGB2GRAY)
	rgb = resized

	# Detect using Haar Cascade, then convert bounding box to (top, right, bottom, left) format
	print("[INFO] recognizing faces...")
	rects = detector.detectMultiScale(gray, scaleFactor=1.1,
			minNeighbors=5, minSize=(30, 30),
			flags=cv2.CASCADE_SCALE_IMAGE)
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
	encodings = face_recognition.face_encodings(rgb, boxes)

	# initialize the list of names for each face detected
	names = []

	# loop over the facial embeddings
	for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown"

		# check to see if we have found a match
		if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number of
			# votes (note: in the event of an unlikely tie Python will
			# select first entry in the dictionary)
			name = max(counts, key=counts.get)

		# update the list of names
		names.append(name)

	# Save image

	# Save username
	if len(names) > 0:
		username = names[0]
		im = Image.fromarray(rgb)
		savepath = "images/" + fileName
		im.save(savepath, "JPEG")
		return username
	else:
		im = Image.fromarray(rgb)
		savepath = "images/" + fileName
		im.save(savepath, "JPEG")
		return "Tunnistamaton käyttäjä"