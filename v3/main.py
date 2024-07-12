# virtualenv: face-id
import step1
import step2
import step3


if __name__ == '__main__':
    # Declara variáveis
    params, images = None, None

    # Faz leitura do arquivo parametros
    params = step1.read()
    if params:
        if params['images_folder'] == 'False':
            images = step2.get_images(params)
        else:
            images = True

    # Abre programa
    if images:
        pass
        # step3.run(params)
