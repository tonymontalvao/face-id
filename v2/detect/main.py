# virtualenv: face-id
import step1
import step2
import step3
import step4


if __name__ == '__main__':
    # Declara variáveis
    params, images, training = None, None, None

    # Faz leitura do arquivo parametros
    params = step1.read()
    if params:
        images = step2.get_images(params)

    # Treina imagens
    if images:
        training = step3.run(params)

    # Abre programa
    if training:
        step4.run(params)
