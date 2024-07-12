#!/usr/local/bin/python3
import cv2
import numpy as np

classFace = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
classOlhos = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

camera = cv2.VideoCapture(0)
amostra, numAmostras = 1, 25
largura, altura = 220, 220
id = input('Digite seu identificador: ')
print('Capturando as faces...')


while True:
    conectado, imagem = camera.read()
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    facesDetectadas = classFace.detectMultiScale(imagemCinza,
                                               scaleFactor=1.5,
                                               minSize=(100,100))
    
    for (x, y, l, a) in facesDetectadas:
        cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)
        regiao = imagem[y:y + a, x:x + l]
        regiaoCinzaOlho = cv2.cvtColor(regiao, cv2.COLOR_BGR2GRAY)
        olhosDetectados = classOlhos.detectMultiScale(regiaoCinzaOlho)

        for (ox, oy, ol, oa) in olhosDetectados:
            cv2.rectangle(regiao, (ox, oy), (ox + ol, oy + oa), (0, 255, 0), 2)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                if np.average(imagemCinza) > 110:
                    imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
                    cv2.imwrite(f'fotos/p.{id}.{amostra:02}.jpg', imagemFace)
                    print(f'Foto {amostra:02} capturada com sucesso')
                    amostra += 1


    cv2.imshow("Face", imagem)
    cv2.waitKey(1)
    if amostra >= sum((numAmostras, 1)):
        break

print('Faces capturadas com sucesso')
camera.release()
cv2.destroyAllWindows()