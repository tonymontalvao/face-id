# virtualenv: face-id
import s1_parametrs
import s2_images
import s3_training
import s4_open

if __name__ == '__main__':
    # Declara variáveis
    params, images = None, None

    # Faz leitura do arquivo parametros
    params = s1_parametrs.read()

    if params != None:
        # Baixa imagens da url informada
        s2_images.get_images(params)

        # Treina as imagens
        s3_training.training(params)

        # Abre programa
        s4_open.run(params)
