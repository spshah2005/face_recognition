# -*- coding: utf-8 -*-
"""face_recognition_coherence.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vmmeJFnKxz0iw8xDsKJjwNV_qfDSGAhw
"""

!pip install face_recognition

from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode
from IPython.display import Image
import cv2
import face_recognition
from google.colab.patches import cv2_imshow
import numpy as np

def take_photo(filename='photo.jpg', quality=0.8):
  js = Javascript('''
    async function takePhoto(quality) {
      const div = document.createElement('div');
      const capture = document.createElement('button');
      capture.textContent = 'Capture';
      div.appendChild(capture);

      const video = document.createElement('video');
      video.style.display = 'block';
      const stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);
      video.srcObject = stream;
      await video.play();

      // Resize the output to fit the video element.
      google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

      // Wait for Capture to be clicked.
      await new Promise((resolve) => capture.onclick = resolve);

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getVideoTracks()[0].stop();
      div.remove();
      return canvas.toDataURL('image/jpeg', quality);
    }
    ''')
  display(js)
  data = eval_js('takePhoto({})'.format(quality))
  binary = b64decode(data.split(',')[1])
  with open(filename, 'wb') as f:
    f.write(binary)
  return filename

def vidToEncoding(videoFile):
  vid = cv2.VideoCapture(videoFile)
  fes = []
  count = 0
  while True:
    suc, im = vid.read()
    count += 1
    try:
      if count % 10 == 0:
        fes.append(face_recognition.face_encodings(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))[0])
    except:
      return fes

def imageToEncoding(imageFile):
  img = cv2.VideoCapture(imageFile)
  fes = []
  suc, im = img.read()
  fes.append(face_recognition.face_encodings(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))[0])
  return fes

shruti_im = face_recognition.load_image_file("shruti.jpg")  #ADD ENCODINGS HERE
shruti_fe = face_recognition.face_encodings(shruti_im)[0]


dhruv_im = face_recognition.load_image_file("dhruv.jpg")
dhruv_fe = face_recognition.face_encodings(dhruv_im)[0]

# Create arrays of known face encodings and their names

all_names = []
known_face_encodings = [shruti_fe, dhruv_fe]
known_face_names = ['shruti', 'dhruv']

# videoFiles = ["jay.mp4"]

# for videoFile in videoFiles:
#   fes = vidToEncoding(videoFile)
#   known_face_encodings += fes
#   name = videoFile.split('.')[0]
#   all_names.append(name)
#   known_face_names += [name for i in fes]

# import glob
# path = "/content/*"
# imageFiles = [filen for filen in glob.glob(path)]
# print(imageFiles)
# print(imageFiles)
# for imageFile in imageFiles:
#   fes = imageToEncoding(imageFile)
#   known_face_encodings += fes
#   name = imageFile.split('.')[0].split('/')[-1]
#   all_names.append(name)
#   known_face_names += [name for i in fes]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

video_capture = cv2.VideoCapture(take_photo())
ret, frame = video_capture.read()

# Resize frame of video to 1/4 size for faster face recognition processing (UNCOMMENT BELOW LINE)

# frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Find all the faces and face encodings in the current frame of video
face_locations = face_recognition.face_locations(rgb_frame)
face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

face_names = []
for face_encoding in face_encodings:
    # See if the face is a match for the known face(s)
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = "Unknown"

    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]

    face_names.append(name)

# Display the results
for (top, right, bottom, left), name in zip(face_locations, face_names):
    # Scale back up face locations since the frame we detected in was scaled to 1/4 size (UNCOMMENT BELOW)

    # top *= 4
    # right *= 4
    # bottom *= 4
    # left *= 4

    # Draw a box around the face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Draw a label with a name below the face
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
cv2_imshow(frame)

    # Hit 'q' on the keyboard to quit!
if cv2.waitKey(1) & 0xFF == ord('q'):
# Release handle to the webcam
  video_capture.release()
  cv2.destroyAllWindows()

attendance = {}
for name in all_names:
  attendance[name] = False

for name in face_names:
  if name in attendance:
    attendance[name] = True

for student in attendance:
  print(student, "- Present" if attendance[student] else "- Absent")