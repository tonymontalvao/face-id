import requests
import os
import shutil
import numpy
import cv2
from PIL import Image
from io import BytesIO

classFace = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def get_images(params) -> dict:
    print('Baixando lista de imagens...')

    # Variables
    url = params['images_url']
    path = params['images_path']

    # Baixa imagens
    response = requests.get(url)
    if response.status_code != 200:
        print('Não foi possível baixar as imagens. Confira a URL e tente novamente')
        return None

    registers = response.json()
    registers = registers[0]['Rows']
    if not registers:
        print('Nenhuma imagem encontrada! Confira o endpoint e tente novamente!')
        return None

    # Remove imagnes
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)

    os.mkdir(path)

    for r in registers:
        # Variables
        person_id = r['matricula_id']
        image_id = r['indice']
        photo = r['foto']
        image_name = f"p.{person_id}.{image_id}.jpg"

        response_image = requests.get(photo)

        try:
            image_content = BytesIO(response_image.content)
            image_content = Image.open(image_content).convert('L')
            image_content = numpy.array(image_content, 'uint8')

            faces_detecteds = classFace.detectMultiScale(image_content,
                                                         scaleFactor=1.5,
                                                         minSize=(100, 100))

            if len(faces_detecteds) == 0:
                print(f"Não foi detectada face na imagem {image_id} - {photo}")

            for (x, y, w, h) in faces_detecteds:
                image_face = cv2.resize(
                    image_content[y:y + h, x:x + w], (220, 220))

                cv2.imwrite(f"{path}/{image_name}", image_face)

        except:
            print(f"Não foi possível baixar a imagem {image_id} - {photo}")

    return True
