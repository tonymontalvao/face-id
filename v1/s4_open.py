import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def run(params):
    detectorFace = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    if params['component'] == 'eigen':
        recognizer = cv2.face.EigenFaceRecognizer_create()
    elif params['component'] == 'fisher':
        recognizer = cv2.face.FisherFaceRecognizer_create()
    elif params['component'] == 'lbph':
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    else:
        print('Não foi possível selecionar componente para reconhecimento...')
        return None

    try:
        recognizer.read("classifier.yml")
        width, height = 220, 220

        font = cv2.FONT_HERSHEY_DUPLEX
        camera = cv2.VideoCapture(0)
    except:
        print('Não foi possível definir parametros para configuração de abertura!')
        return None

    # if params['debug'] == 'False':
    #     service = Service(ChromeDriverManager().install())
    #     driver = webdriver.Chrome(service=service)
    #     driver.fullscreen_window()
    #     driver.get(params['url_site'])

    #     search_box = driver.find_element(
    #         by=By.NAME, value=f"{params['field_focus']}")

    navigator = False

    while True:
        connect, image = camera.read()
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detectedFaces = detectorFace.detectMultiScale(grayImage,
                                                      scaleFactor=1.5,
                                                      minSize=(30, 30))

        for (x, y, w, h) in detectedFaces:
            imageFace = cv2.resize(
                grayImage[y:y + h, x:x + w], (width, height))

            id, threshold = recognizer.predict(imageFace)

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            cv2.putText(image, str(id), (x, y + (w + 30)),
                        font, 0.8, (0, 0, 255), 2, cv2.LINE_AA, False)

            cv2.putText(image, str(threshold), (x, y + (h + 50)),
                        font, 0.5, (0, 0, 255), 2, cv2.LINE_AA, False)

            if float(params['threshold']) >= threshold and str(params['debug']) == 'False':
                search_box.send_keys(id)

        cv2.imshow("Face", image)

        if params['debug'] == 'False':
            if navigator is False:
                navigator = True
                chrome_options = webdriver.ChromeOptions()

                chrome_options.add_experimental_option(
                    "useAutomationExtension", False)

                chrome_options.add_experimental_option(
                    "excludeSwitches", ["enable-automation"])

                service = Service(ChromeDriverManager().install())

                driver = webdriver.Chrome(
                    options=chrome_options, service=service)

                driver.get(params['url_site'])

                search_box = driver.find_element(
                    by=By.NAME, value=f"{params['field_focus']}")

            driver.fullscreen_window()

        if cv2.waitKey(1) == ord('q'):
            break

    # End

    camera.release()
    cv2.destroyAllWindows()
