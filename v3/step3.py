import face_recognition
import cv2
import numpy as np
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def run(params):
    path = params['images_path']
    debug = params['debug']
    site = params['site_url']
    field = params['site_field_focus']
    navigator = False

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    known_face_encodings, known_face_names, files = [], [], []

    files = [os.path.join(path, f)
             for f in os.listdir(path) if not f.startswith('.')]
    files.sort()

    for file in files:
        image = face_recognition.load_image_file(file)
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.split(file)[1].split('.')[1])

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    if debug == 'False':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])

        if os.path.isfile('/usr/bin/chromedriver'):
            service = Service('/usr/bin/chromedriver')
        else:
            service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(options=chrome_options, service=service)
        driver.get(site)
        search_box = driver.find_element(by=By.ID, value=field)

    while video_capture.isOpened():
        # Grab a single frame of video
        ret, frame = video_capture.read()
        if not ret:
            break

        # resize
        frame = cv2.resize(frame, (600, 400))

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                name = "None"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)

            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 0.8, (255, 255, 255), 1)

            # Escreve no navegador
            if debug == 'False' and navigator is True and name != 'None':
                search_box.send_keys(name)
                search_box.send_keys(Keys.ENTER)

        # Display the resulting image
        cv2.imshow('Video', frame)

        if debug == 'False' and navigator is False:
            navigator = True
            driver.fullscreen_window()
            cv2.waitKey(5000)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
