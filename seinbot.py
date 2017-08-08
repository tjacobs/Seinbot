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
import plotly.graph_objs as go


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

# How many seconds?
length = int(22.6 * 60);

# Init
jerry =  [0] * length
george = [0] * length
elaine = [0] * length
kramer = [0] * length

# Process video
video = VideoFileClip("Seinfeld.S03E01.mkv")
for t in range(0, length, 10):
    frame = video.get_frame(t)
    characters = process(frame)
    jerry[t]  = 0.0
    elaine[t] = 0.0
    george[t] = 0.0
    kramer[t] = 0.0
    if 'Jerry'  in characters:  jerry[t] = 100.0
    if 'George' in characters: george[t] = 75.0
    if 'Elaine' in characters: elaine[t] = 50.0
    if 'Kramer' in characters: kramer[t] = 25.0
#    print("%0.1f: {}" % (100.0 * t / length), str(characters))
    print( (t / length), characters)
#x = np.array(x/60.0 for x in range(length))
x = np.array(range(length))
x = x / 60.0

# Start Plotly
plotly.tools.set_credentials_file(username='TomJacobs', api_key='juXJEk8RkE5bfaydkE4A')

width = 30

# Create plot
trace1 = go.Scatter(
    x=x,
    y=jerry,
    name = '<b>Jerry</b>',
    connectgaps=False,
    line = dict(color=('rgb(22,96,167)'), width=width)
)
trace2 = go.Scatter(
    x=x,
    y=george,
    name = 'George',
    connectgaps=False,
    line = dict(color=('rgb(205,12,24)'), width=width)
)
trace3 = go.Scatter(
    x=x,
    y=elaine,
    name = 'Elaine',
    connectgaps=False,
    line = dict(color=('rgb(12,205,204)'), width=width)
)
trace4 = go.Scatter(
    x=x,
    y=kramer,
    name = 'Kramer',
    connectgaps=False,
    line = dict(color=('rgb(25,12,24)'), width=width),
)

# Plot
data = [trace1, trace2, trace3, trace4]
fig = dict(data=data)
py.iplot(fig, filename='Screen Time')


# Define video function
def create_video(pipeline_in, input_video, output_video):
    # Process video
    video = VideoFileClip( input_video )
    video_processed = video.fl_image( pipeline_in )
    video_processed.write_videofile( output_video, audio=False )
