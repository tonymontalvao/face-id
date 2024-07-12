import os

file_path = '_parameters.txt'

parameters = {
    'path_images': 'images',
    'url_site': 'https://www.google.com',
    'field_focus': 'q',
    'url_images': 'http://natuflores.ddns.com.br:8082/bis_painel/api/produtos?id_rep=5',
    'header': '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9yZXAiOiI1In0.VhmYuDWknA9neYqL9tddOzLW1pmwLo2Lok1G4c2yMY4"}',
    'field_id': 'id_produto',
    'field_image': 'url_image1',
    'component': 'eigen',
    'threshold': 3500,
    'debug': False,
}

legenda = f"""\n\n\nLegenda:
    path_images = Caminho local para gravação das imagens
    url_site = Endereço para abertura do programa
    field_focus = Nome do campo de foco no site
    url_images = End point onde estão as imagens.
    header = Header para passar na requisição
    field_id = O nome do campo no json da url_images que representa o id da pessoa no sistema
    field_image = O nome do campo no json da url_images que representa o link da imagem
    component = Nome do component a ser usado para o reconhecimento. Valores 'eigen', 'fisher', 'lbph'
    threshold = Grau de confiança do reconhecimento da face, depende do componente a ser testado, podendo variar de 0 pouco confiável a 9000 muito confiável, valor padrão 3500
    debug = Se marcado como True, testa componente e grau de confiança, False abre o programa, padrão False
"""


def read() -> dict:
    if not os.path.isfile(file_path):
        print('Gerando arquivo de parametros...')

        with open(file_path, 'w') as file:
            for register, value in parameters.items():
                file.write(f'{register}=={value}\n')

            file.write(legenda)

            print('Ajuste os parametros e rode o programa novamente!')

        return None
    else:
        print('Lendo arquivo de parametros...')

        with open(file_path, 'r') as file:
            for line in file:
                register = line.strip().split('==')

                if register[0] == '':
                    break
                else:
                    parameters[register[0]] = register[1]

        return parameters
