import folium as fl
from streamlit_folium import st_folium
import streamlit as st
from geopy.distance import geodesic
import os
import random
from get_photo_loc import get_exif_data, get_gps_info, get_lat_lng
from config import image_folder, continent, centre, file_types

# set initial location
Test_location = centre[continent]
def get_pos(lat, lng):
    return lat, lng
starting_location = [Test_location["Latitude"], Test_location["Longitude"]]  

# get photos folder
all_files = os.listdir(image_folder)
files = []
for file in all_files:
    files = [file for file in all_files if file.split(".")[1] in file_types]

# initialize parameters
if "num_files" not in st.session_state:
    num_files = len(files)
    st.session_state.num_files = num_files  
if "marker_location" not in st.session_state:
    st.session_state.marker_location = None  # Default location
    st.session_state.zoom = 4  # Default zoom
if "photo_location" not in st.session_state:
    st.session_state.photo_location = None  # Default location
if "remaining_photos" not in st.session_state:
    st.session_state.remaining_photos = files
if "image" not in st.session_state:
    st.session_state.image = files[0]
if "reset" not in st.session_state:
    st.session_state.reset = False

# define function for button click
def get_another_photo():
    st.session_state.marker_location = None
    st.session_state.photo_location = None
    photo_loc = None
    while not photo_loc:
        remaining_photos = st.session_state.remaining_photos
        num_remaining = len(remaining_photos)
        if num_remaining == 0:
            st.session_state.reset = True
            return
        index = random.randint(0,num_remaining-1)
        image = remaining_photos[index]
        image_path = os.path.join(image_folder,image)
        exif_data = get_exif_data(image_path)
        gps_info = get_gps_info(exif_data)
        photo_loc = get_lat_lng(gps_info) #[0] is lat and [1] is long
        st.session_state.remaining_photos.remove(image)

    # only select photos with locations
    st.session_state.image = image

def reset():
    st.session_state.marker_location = None
    st.session_state.photo_location = None
    st.session_state.remaining_photos = files
    st.session_state.image = files[0]
    st.session_state.reset = False

    photo_loc = None
    while not photo_loc:
        remaining_photos = st.session_state.remaining_photos
        num_remaining = len(remaining_photos)
        if num_remaining == 0:
            st.session_state.reset = True
            return
        index = random.randint(0,num_remaining-1)
        image = remaining_photos[index]
        image_path = os.path.join(image_folder,image)
        exif_data = get_exif_data(image_path)
        gps_info = get_gps_info(exif_data)
        photo_loc = get_lat_lng(gps_info) #[0] is lat and [1] is long
        st.session_state.remaining_photos.remove(image)

    # only select photos with locations
    st.session_state.image = image

# get the photo for the current index
image_path = os.path.join(image_folder,st.session_state.image)
exif_data = get_exif_data(image_path)
gps_info = get_gps_info(exif_data)
photo_loc = get_lat_lng(gps_info) #[0] is lat and [1] is long


# Streamlit start
st.set_page_config(layout="wide")
col1, col2 = st.columns([0.4,0.6])
with col1:
    st.title("Welcome to knock-off Geoguessr!!!")
    st.write("Guess the location of this photo!")
    st.image(image_path, caption="Nice photo, eh?",width=500)
    # Get latitude and longitude
    location = get_lat_lng(gps_info)
    lat = location[0]
    long = location[1]
    if not st.session_state.reset:
        st.button(label="Another Photo!",on_click=get_another_photo)
    else:
        st.write("Oops, seems like we ran out of photos!")
        st.button(label="Start Again!",on_click=reset)

with col2:
    # set map location and zoom level
    if st.session_state.marker_location and st.session_state.photo_location:
        # calculate distance
        avg_lat = (st.session_state.marker_location[0] + st.session_state.photo_location[0])/2
        avg_long = (st.session_state.marker_location[1] + st.session_state.photo_location[1])/2
        m = fl.Map(location=[avg_lat,avg_long], zoom_start=4)
        m.fit_bounds([st.session_state.marker_location, st.session_state.photo_location]) 

    else:   
        m = fl.Map(location=starting_location, zoom_start=4)


    #marker = fl.Marker(photo_loc, popup="The photo was taken here!", tooltip="The photo was taken here!").add_to(m)
    #m.add_child(fl.LatLngPopup())
    if st.session_state.marker_location:
        fl.Marker(
            location=st.session_state.marker_location,
            draggable=False
        ).add_to(m)

    if st.session_state.photo_location:
        fl.Marker(
            location=st.session_state.photo_location,
            draggable=False,
            popup="The photo was taken here!",
            tooltip="The photo was taken here!",
            icon=fl.Icon(color="green")
        ).add_to(m)

    if st.session_state.marker_location and st.session_state.photo_location:
        line = fl.PolyLine([st.session_state.marker_location, st.session_state.photo_location], color="#2069bd", weight=2.5, opacity=1)
        m.add_child(line)

    map = st_folium(m, height=700, width=700)

    if map.get("last_clicked"):
        lat, lng = map["last_clicked"]["lat"], map["last_clicked"]["lng"]
        st.session_state.marker_location = [lat, lng]  # Update session state with new marker location
        st.session_state.zoom = map["zoom"]
        st.session_state.photo_location = photo_loc
        # Redraw the map immediately with the new marker location
        avg_lat = (st.session_state.marker_location[0] + st.session_state.photo_location[0])/2
        avg_long = (st.session_state.marker_location[1] + st.session_state.photo_location[1])/2
        m = fl.Map(location=[avg_lat,avg_long], zoom_start=4)
        m.fit_bounds([st.session_state.marker_location, st.session_state.photo_location]) 
        #m = fl.Map(location=st.session_state.marker_location, zoom_start=st.session_state.zoom)
        map = st_folium(m, width=620, height=580, key="folium_map")








