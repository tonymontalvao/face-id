import os
import requests

file_path = '_parameters.txt'

parameters = {
    'images_url': '',
    'images_path': 'imagens',
    'images_folder': 'False',
    'site_url': '',
    'site_field_focus': '',
    'debug': True,
}


def read() -> dict:
    if not os.path.isfile(file_path):
        print('Gerando arquivo de parametros...')

        with open(file_path, 'w') as file:
            for register, value in parameters.items():
                file.write(f'{register}=={value}\n')

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
