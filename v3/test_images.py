import face_recognition
import io
import numpy as np

# Files
from core.database import session_maker
from models.fotos_model import FotosModel
import step1

db = session_maker()
registers = db.query(FotosModel).all()
file_path = '_parameters.txt'

if not registers:
    print('Nenhum registro encontrado!')

else:
    parameters = step1.read()
    photos, known_face_encodings, known_face_names = [], [], []

    for r in registers:
        out = io.BytesIO(r.hash_imagem)
        out.seek(0)
        encode = np.load(out)
        known_face_encodings.append(encode)

        photo = {'id': None, 'index': None, 'encoding': None}
        photo['encoding'] = encode
        photo['id'] = r.id_pessoa
        photo['index'] = r.idx_imagem
        photo['reconhecido'] = None
        photos.append(photo)

    for photo in photos:
        keys = []

        # attempt to match each face in the input image to our known encodings
        matches = face_recognition.compare_faces(
            known_face_encodings, photo['encoding'], tolerance=float(parameters['tolerance']))

        regs = 0
        for reg in matches:
            if reg == True:
                regs += 1

        if regs == 0:
            print(f"Foto da pessoa: {photo['id']
                                     }-{photo['link']} não encontrada!")
        elif regs > 1:
            print(f"Foto da pessoa: {
                  photo['id']}-{photo['link']} encontrada {regs} vezes!")
