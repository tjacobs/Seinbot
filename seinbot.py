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
video = VideoFileClip("input.mkv")
for t in range(0, length, 10):
    frame = video.get_frame(t)
    characters = process(frame)
    jerry[t]  = 0.0
    elaine[t] = 0.0
    george[t] = 0.0
    kramer[t] = 0.0
    if 'Jerry'  in characters:  jerry[t] = 100.0
    if 'George' in characters: george[t] = 100.0
    if 'Elaine' in characters: elaine[t] = 100.0
    if 'Kramer' in characters: kramer[t] = 100.0
#    print("%0.1f: {}" % (100.0 * t / length), str(characters))
    print( (t / length), characters)
#x = np.array(x/60.0 for x in range(length))
x = np.array(range(length))

# Start Plotly
plotly.tools.set_credentials_file(username='TomJacobs', api_key='juXJEk8RkE5bfaydkE4A')

# Group data together
hist_data = [jerry, george, elaine, kramer]
group_labels = ['Jerry', 'George', 'Elaine', 'Kramer']

# Add data to create cumulative stacked values
y0_stack=jerry
y1_stack=george
y2_stack=elaine
y3_stack=kramer
#y1_stack=[y0+y1 for y0, y1 in zip(jerry, george)]
#y2_stack=[y0+y1+y2 for y0, y1, y2 in zip(jerry, george, elaine)]
#y3_stack=[y0+y1+y2+y3 for y0, y1, y2, y3 in zip(jerry, george, elaine, kramer)]

# Make original values strings and add % for hover text
y0_txt=[str(y0)+'%' for y0 in jerry]
y1_txt=[str(y1)+'%' for y1 in george]
y2_txt=[str(y2)+'%' for y2 in elaine]
y3_txt=[str(y3)+'%' for y3 in kramer]

jerry = go.Scatter(
    x=x,
    y=y0_stack,
    text="Jerry",
    hoverinfo='x+text',
    mode='lines',
    line=dict(width=0.5, color='rgb(100, 90, 241)'),
    fill='tonexty'
)
trace1 = go.Scatter(
    x=x,
    y=y1_stack,
    text="George",
    hoverinfo='x+text',
    mode='lines',
    line=dict(width=0.5, color='rgb(111, 231, 119)'),
    fill='tonexty'
)
trace2 = go.Scatter(
    x=x,
    y=y2_stack,
    text="Elaine",
    hoverinfo='x+text',
    mode='lines',
    line=dict(width=0.5, color='rgb(224, 47, 12)'),
    fill='tonexty'
)
trace3 = go.Scatter(
    x=x,
    y=y2_stack,
    text="Kramer",
    hoverinfo='x+text',
    mode='lines',
    line=dict(width=0.5, color='rgb(4, 7, 12)'),
    fill='tonexty'
)
data = [jerry, trace1, trace2, trace3]
fig = go.Figure(data=data)

# Plot!
py.iplot(fig, filename='Screen Time')

# Define video function
def create_video(pipeline_in, input_video, output_video):
    # Process video
    video = VideoFileClip( input_video )
    video_processed = video.fl_image( pipeline_in )
    video_processed.write_videofile( output_video, audio=False )
