import requests
import os
import shutil


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
            if response_image.ok:
                with open(f"{path}/{image_name}", "wb") as image:
                    image.write(response_image.content)
            else:
                print(f"Não foi possível baixar a imagem {image_id} - {photo}")
        except:
            print(f"Não foi possível baixar a imagem {image_id} - {photo}")

    return True
