import cv2
import numpy
from PIL import Image
import os


def run(params):
    print('Treinando reconhecimento...')
    component = params['component']
    threshold = float(params['threshold'])
    path = params['images_path']

    try:
        if component == 'eigen':
            component = cv2.face.EigenFaceRecognizer_create(
                num_components=50, threshold=threshold)
        elif component == 'fisher':
            component = cv2.face.FisherFaceRecognizer_create(
                num_components=50, threshold=threshold)
        elif component == 'lbph':
            component = cv2.face.LBPHFaceRecognizer_create(
                radius=1, neighbors=1, grid_x=5, grid_y=5, threshold=threshold)
        else:
            print('Não foi possível selecionar componente para reconhecimento...')
            return None
    except ValueError:
        print('Não foi possível configurar parametros para reconhecimento...')
        return None

    aImages, aIds, files = [], [], []

    files = [os.path.join(path, f)
             for f in os.listdir(path) if not f.startswith('.')]
    files.sort()

    for file in files:
        image = Image.open(file).convert('L')
        aImages.append(numpy.array(image, 'uint8'))
        aIds.append(int(os.path.split(file)[1].split('.')[1]))

    try:
        component.train(aImages, numpy.array(aIds))
        component.write('classifier.yml')
        return True
    except:
        print('Não foi possível gerar array para treinamento')
        return None