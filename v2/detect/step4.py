import cv2
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def run(params):
    component = params['component']
    threshold = float(params['threshold'])
    debug = params['debug']
    navigator = False
    site = params['site_url']
    field = params['site_field_focus']
    detectorFace = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    if component == 'eigen':
        recognizer = cv2.face.EigenFaceRecognizer_create()
    elif component == 'fisher':
        recognizer = cv2.face.FisherFaceRecognizer_create()
    elif component == 'lbph':
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    else:
        print('Não foi possível selecionar componente para reconhecimento...')
        return None

    try:
        fps = 30
        frame_width = 640
        frame_height = 480

        recognizer.read("classifier.yml")
        width, height = 220, 220
        font = cv2.FONT_HERSHEY_DUPLEX
        camera = cv2.VideoCapture(0, apiPreference=cv2.CAP_V4L2)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        camera.set(cv2.CAP_PROP_FPS, fps)
    except:
        print('Não foi possível definir parametros para configuração de abertura!')
        return None

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

    while True:
        connect, image = camera.read()
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detectedFaces = detectorFace.detectMultiScale(grayImage,
                                                      scaleFactor=1.5,
                                                      minSize=(30, 30))

        for (x, y, w, h) in detectedFaces:
            imageFace = cv2.resize(
                grayImage[y:y + h, x:x + w], (width, height))

            id, confiance = recognizer.predict(imageFace)

            if debug == 'True':
                # Desenha retangulo
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Mostra o id da imagem
                cv2.putText(image, str(id), (x, y + (w + 30)),
                            font, 0.8, (0, 0, 255), 2, cv2.LINE_AA, False)

                # Mostra a confiança da imagem
                cv2.putText(image, str(confiance), (x, y + (h + 50)),
                            font, 0.5, (0, 0, 255), 2, cv2.LINE_AA, False)

                if confiance >= float(threshold):
                    # Mostra o id da imagem
                    cv2.putText(image, 'true', (x, y + (w + 70)),
                                font, 0.5, (0, 0, 255), 2, cv2.LINE_AA, False)
            elif navigator is True and id != -1:
                # Escreve no navegador
                search_box.send_keys(id)
                search_box.send_keys(Keys.ENTER)

        cv2.imshow("Face", image)

        if debug == 'False' and navigator is False:
            cv2.waitKey(5000)
            navigator = True
            driver.fullscreen_window()

        if cv2.waitKey(1) == ord('q'):
            break

    # End
    camera.release()
    cv2.destroyAllWindows()
