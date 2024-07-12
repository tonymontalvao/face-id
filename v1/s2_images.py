import requests
import json
import os
import shutil
import cv2
from PIL import Image
from io import BytesIO
import numpy

classFace = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

classEyes = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml')


def get_images(params) -> dict:
    print('Baixando lista de imagens...')

    try:
        header = json.loads(params['header'])
    except Exception:
        print('Não foi possível converter cabeçalho(header) da requisição em formato json')
        return None

    response = requests.get(params['url_images'], headers=header)
    if response.status_code == 200 or response.status_code == 202:
        if os.path.isdir(params['path_images']):
            shutil.rmtree(params['path_images'], ignore_errors=True)

        os.mkdir(params['path_images'])

        for i in response.json():
            response_image = requests.get(i[params['field_image']])

            if response_image.status_code == 200 or response_image.status_code == 202:
                path_images = f'{params['path_images']}/'
                image_name = f'p.{i[params['field_id']]}.01.jpg'

                while True:
                    if os.path.isfile(path_images + image_name):
                        seq = int(image_name.split('.')[2]) + 1
                        image_name = f'p.{i[params['field_id']]}.{seq:02}.jpg'
                    else:
                        break

                image_name = path_images + image_name

                image_content = Image.open(
                    BytesIO(response_image.content)).convert('L')

                image_content = numpy.array(image_content, 'uint8')

                faces_detecteds = classFace.detectMultiScale(image_content,
                                                             scaleFactor=1.5,
                                                             minSize=(100, 100))

                for (x, y, w, h) in faces_detecteds:
                    image_face = cv2.resize(
                        image_content[y:y + h, x:x + w], (220, 220))

                    cv2.imwrite(image_name, image_face)
            else:
                print(f'Não foi possível baixar imagem {
                      i[params['field_image']]}')
