#!/usr/bin/env python
# coding: utf-8

# In[1]:


import face_recognition
import cv2
import numpy as np
import scipy as sp
import pandas as pd


# In[ ]:





# In[ ]:


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


# In[1]:


# Create list of known face names
known_face_names = []

# load text file of student names
with open('Students/student_names.txt', 'r') as names_file:
    
    cnt = 0
    while True:
        student_name = names_file.readline().strip()
        
        # Break if end of file reached
        if student_name == "":
            break
            
        # Append to list
        else:
            known_face_names.append(student_name)
            cnt += 1

            
# Define number of students constant
NUM_STUDENTS = cnt


# In[ ]:


# Define Student ID, assumes no. of students < 100

def id(num):
    string = ""
    
    if num < 10:
        string = "0" + str(num)
    else:
        string = str(num)
    
    return string


# In[ ]:


# Create list of known face encodings 
known_face_encodings = []

for i in range(0, NUM_STUDENTS):
    
    # Path takes into account ID
    student_img = face_recognition.load_image_file("Students/img_" + id(i+1) + ".jpg")
    
    # Convert into encoding
    student_face_encoding = face_recognition.face_encodings(student_img)[0]
    
    # Append to list
    known_face_encodings.append(student_face_encoding)


# In[1]:


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Initialize Register
students_present = [False] * NUM_STUDENTS

# Initialize how long students were seen
recognized_frames = [0] * NUM_STUDENTS

# Initialize window of 3 seconds, at 30 frames per second
# Note that 0 represents unknown identity
# window = pd.Series(np.zeros(30*3), dtype=int)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    if len(frame.shape) == 2:
        frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)

        
    # Check if no frame
    if frame is None:
        continue

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations, num_jitters = 1, model='small')

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance = 0.48)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                
                # add number of frames
                recognized_frames[best_match_index] += 2
                
                
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations 
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

# output
print("\nRegister\n")

for i in range(0, NUM_STUDENTS):
    
    if(recognized_frames[i] >= 10):
        students_present[i] = True
    
    print(known_face_names[i], ' '*(40 -  len(known_face_names[i])), students_present[i])


# In[2]:


# return a list of students present
def get_register():
    return [known_face_names, students_present]


# In[ ]:


# return number of students
def get_num_students():
    return NUM_STUDENTS

