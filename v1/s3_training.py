import cv2
import numpy
from PIL import Image
import os


def training(params):
    print('Treinando reconhecimento...')

    try:
        if params['component'] == 'eigen':
            component = cv2.face.EigenFaceRecognizer_create(
                num_components=50, threshold=float(params['threshold']))
        elif params['component'] == 'fisher':
            component = cv2.face.FisherFaceRecognizer_create(
                num_components=50, threshold=float(params['threshold']))
        elif params['component'] == 'lbph':
            component = cv2.face.LBPHFaceRecognizer_create(
                radius=1, neighbors=1, grid_x=5, grid_y=5, threshold=float(params['threshold']))
        else:
            print('Não foi possível selecionar componente para reconhecimento...')
            return None
    except ValueError:
        print('Não foi possível passar parametros para reconhecimento...')
        return None

    aImages, aIds = [], []

    files = [os.path.join(params['path_images'], f)
             for f in os.listdir(params['path_images']) if not f.startswith('.')]

    files.sort()

    for file in files:
        image = Image.open(file).convert('L')
        aImages.append(numpy.array(image, 'uint8'))
        aIds.append(int(os.path.split(file)[1].split('.')[1]))

    try:
        component.train(aImages, numpy.array(aIds))
        component.write('classifier.yml')
    except:
        print('Não foi possível converter array para treinamento')
        return None
