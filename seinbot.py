import datetime
import numpy as np
import face_recognition
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip
from IPython.display import HTML
from PIL import Image, ImageDraw
import plotly.plotly as py
import plotly.figure_factory as ff
import plotly 

# Init
face_locations = []
face_encodings = []
face_names = []

# Load faces
jerry_image = face_recognition.load_image_file("known_people/Jerry Seinfeld.jpg")
jerry_face_encoding = face_recognition.face_encodings(jerry_image)[0]
george_image = face_recognition.load_image_file("known_people/George Costanza.jpg")
george_face_encoding = face_recognition.face_encodings(george_image)[0]
elaine_image = face_recognition.load_image_file("known_people/Elane Benes.jpg")
elaine_face_encoding = face_recognition.face_encodings(elaine_image)[0]
kramer_image = face_recognition.load_image_file("known_people/Cosmo Kramer.jpg")
kramer_face_encoding = face_recognition.face_encodings(kramer_image)[0]

# Process a frame
def process(image):
    
    # Find faces in this frame
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match1 = face_recognition.compare_faces([jerry_face_encoding], face_encoding)
        match2 = face_recognition.compare_faces([george_face_encoding], face_encoding)
        match3 = face_recognition.compare_faces([elaine_face_encoding], face_encoding)
        match4 = face_recognition.compare_faces([kramer_face_encoding], face_encoding)
        name = "Unknown"
        if match1[0]:
            name = "Jerry"
        if match2[0]:
            name = "George"
        if match3[0]:
            name = "Elaine"
        if match4[0]:
            name = "Kramer"
        face_names.append(name)
    return face_names

# Add histogram data
jerry = np.random.randn(200)-2  
george = np.random.randn(200)+2  
elaine = np.random.randn(200)  
kramer = np.random.randn(200)+4  

# Process video
video = VideoFileClip("input_short.mov")
for t in range(5):
    frame = video.get_frame(t)
    characters = process(frame)
    jerry[t]  = 0.0
    elaine[t] = 0.0
    george[t] = 0.0
    kramer[t] = 0.0
    if 'Jerry'  in characters:  jerry[t] = 1.0
    if 'George' in characters: george[t] = 1.0
    if 'Elaine' in characters: elaine[t] = 1.0
    if 'Kramer' in characters: kramer[t] = 1.0
    print(characters)
    print(jerry)

# Start Plotly
plotly.tools.set_credentials_file(username='TomJacobs', api_key='juXJEk8RkE5bfaydkE4A')

# Group data together
hist_data = [jerry, george, elaine, kramer]
group_labels = ['Jerry', 'George', 'Elaine', 'Kramer']

# Create distplot with custom bin_size
fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)

# Plot!
py.iplot(fig, filename='Screen Time')


# Define video function
def create_video(pipeline_in, input_video, output_video):
    # Process video
    video = VideoFileClip( input_video )
    video_processed = video.fl_image( pipeline_in )
    video_processed.write_videofile( output_video, audio=False )
