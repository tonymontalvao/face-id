import requests
import os
import shutil
import face_recognition
import numpy
import io

# files
from core.database import session_maker
from models.fotos_model import FotosModel
from main import printProgressBar


def get_images(params) -> dict:
    print('Baixando lista de imagens...')

    # Variables
    url = params['images_url']
    path = params['images_path']
    folder = params['images_folder']
    debug = params['debug']

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

    # Recupera a sessão
    db = session_maker()

    # Baixa os arquivos
    if folder == 'False' or not os.path.isdir(path):
        # Remove imagens
        shutil.rmtree(path, ignore_errors=True)
        os.mkdir(path)

        for i, r in enumerate(registers):
            printProgressBar(i, len(registers), prefix='Progress:',
                             suffix='Complete', autosize=True)

            # Variables
            person_id = r['matricula_id']
            image_id = r['indice']
            photo = r['foto']
            changed = False
            image_name = f"p.{person_id}.{image_id}.jpg"

            register = db.query(FotosModel).filter(
                FotosModel.id_pessoa == person_id and FotosModel.idx_imagem == image_id).one_or_none()

            if changed == True or not register:
                response_image = requests.get(photo)
                if response_image.ok:
                    with open(f"{path}/{image_name}", "wb") as image:
                        image.write(response_image.content)
                else:
                    print(f"Não foi possível baixar a imagem {photo}")

    # Faz a codificação dos arquivos
    files = [os.path.join(path, f)
             for f in os.listdir(path) if not f.startswith('.')]
    files.sort()

    for i, file in enumerate(files, 1):
        try:
            printProgressBar(i, len(files), prefix='Progress:',
                             suffix='Complete', autosize=True)

            image = face_recognition.load_image_file(file)
            encoding = face_recognition.face_encodings(image)[0]
            out = io.BytesIO()
            encoding = numpy.save(out, encoding)
            out.seek(0)

            person_id = os.path.split(file)[1].split('.')[1]
            image_id = os.path.split(file)[1].split('.')[2]

            register = db.query(FotosModel).filter(
                FotosModel.id_pessoa == person_id and FotosModel.idx_imagem == photo).one_or_none()

            if register:
                register.hash_imagem = out.read()
            else:
                register = FotosModel(
                    id_pessoa=person_id,
                    idx_imagem=image_id,
                    hash_imagem=out.read()
                )
                db.add(register)

        except:
            print(f"Não foi possível carregar imagem {file}")

    # Salva alterações no banco de dados
    db.commit()
    db.close()

    # if debug == 'False':
    #     shutil.rmtree(path, ignore_errors=True)

    return True
