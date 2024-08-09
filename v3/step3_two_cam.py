import face_recognition
import cv2
import numpy as np
import io
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType


# files
from core.database import session_maker
from models.fotos_model import FotosModel


def run(params):
    debug = params['debug']
    site = params['site_url']
    field = params['site_field_focus']
    tolerance = float(params['tolerance'])
    usb = params['webcam_usb']

    # Get a reference to webcam #0 (the default one)
    fps = 30
    frame_width = 640
    frame_height = 480
    font = cv2.FONT_HERSHEY_DUPLEX

    known_face_encodings, known_face_names = [], []

    # Recupera a sessão
    db = session_maker()
    registers = db.query(FotosModel).all()
    if not registers:
        print('Nenhum registro encontrado!')
        return

    for r in registers:
        out = io.BytesIO(r.hash_imagem)
        out.seek(0)
        known_face_encodings.append(np.load(out))
        known_face_names.append(str(r.id_pessoa))

    db.close()

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    if debug == 'False':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--kiosk")
        chrome_options.add_argument("--start-fullscreen")
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])

        # if os.path.isfile('/usr/bin/chromedriver'):
        #     service = Service('/usr/bin/chromedriver')
        # else:
        #     try:
        #         service = Service(ChromeDriverManager().install())
        #     except:
        #         service = Service(ChromeDriverManager(
        #             chrome_type=ChromeType.CHROMIUM).install())

        service = Service(ChromeDriverManager(
            chrome_type=ChromeType.CHROMIUM).install())
        driver = webdriver.Chrome(options=chrome_options, service=service)
        driver.get(site)
        driver.fullscreen_window()

        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'lb_porteiro')))
        except:
            driver.quit()
        finally:
            driver.implicitly_wait(100)
            search_box = driver.find_element(by=By.ID, value=field)

    if usb == 'True':
        video_capture0 = cv2.VideoCapture(0, apiPreference=cv2.CAP_V4L2)
        video_capture1 = cv2.VideoCapture(2, apiPreference=cv2.CAP_V4L2)
    else:
        video_capture0 = cv2.VideoCapture(0)
        video_capture1 = cv2.VideoCapture(2)

    # video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    # video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    # video_capture.set(cv2.CAP_PROP_FPS, fps)

    while True:
        # Grab a single frame of video
        ret0, frame0 = video_capture0.read()
        ret1, frame1 = video_capture1.read()
        if not ret0 or not ret1:
            break

        frame = cv2.hconcat([frame0, frame1])

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
                    known_face_encodings, face_encoding, tolerance=tolerance)

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
            if debug == 'True':
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35),
                              (right, bottom), (0, 0, 255), cv2.FILLED)

                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6),
                            font, 0.8, (255, 255, 255), 1)

            elif name != 'None' and element.get_property('innerHTML') != 'Porteiro?':
                # Escreve no navegador
                search_box.send_keys(name)
                search_box.send_keys(Keys.ENTER)

        # Display the resulting image
        if debug == 'True':
            cv2.namedWindow('Video', cv2.WINDOW_FULLSCREEN)
            cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) == ord('q'):
            break

    # Release handle to the webcam
    video_capture0.release()
    video_capture1.release()
    cv2.destroyAllWindows()
    # driver.quit()
