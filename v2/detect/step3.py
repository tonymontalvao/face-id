import cv2
import numpy
from PIL import Image
import os
import shutil


def run(params):
    print('Treinando reconhecimento...')
    component = params['component']
    threshold = float(params['threshold'])
    path = params['images_path']
    debug = params['debug']
    folder = params['images_folder']

    try:
        if component == 'eigen':
            component = cv2.face.EigenFaceRecognizer_create()
        elif component == 'fisher':
            component = cv2.face.FisherFaceRecognizer_create()
        elif component == 'lbph':
            component = cv2.face.LBPHFaceRecognizer_create()
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
        if debug == 'False' and folder == 'False':
            shutil.rmtree(path, ignore_errors=True)

        return True
    except:
        print('Não foi possível gerar array para treinamento')
        return None
