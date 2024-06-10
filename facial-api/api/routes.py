from io import BytesIO
from flask import Flask, request, jsonify
import base64
import os
import cv2
import numpy as np
from PIL import Image, ImageOps

UPLOAD_FOLDER = os.path.abspath('api/upload/')
IMAGES_FOLDER = os.path.abspath('./api/images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def detecta_face(network, path_imagem, conf_min=0.7):
    imagem = Image.open(path_imagem).convert("L")
    imagem = np.array(imagem, "uint8")
    imagem = cv2.cvtColor(imagem, cv2.COLOR_GRAY2BGR)
    (h, w) = imagem.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(imagem, (100, 100)), 1.0, (100, 100), (104.0, 117.0, 123.0)
    )
    network.setInput(blob)
    deteccoes = network.forward()

    face = None
    for i in range(0, deteccoes.shape[2]):
        confianca = deteccoes[0, 0, i, 2]
        if confianca > conf_min:
            bbox = deteccoes[0, 0, i, 3:7] * np.array([w, h, w, h])
            (start_x, start_y, end_x, end_y) = bbox.astype("int")
            roi = imagem[start_y:end_y, start_x:end_x]
            roi = cv2.resize(roi, (60, 80))
            cv2.rectangle(imagem, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
            face = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    return face, imagem


def get_image_data():
    network = cv2.dnn.readNetFromCaffe(
        os.path.abspath('./api/content/deploy.prototxt.txt'),
        os.path.abspath('./api/content/res10_300x300_ssd_iter_140000.caffemodel'),
    )
    paths = [
        os.path.join(IMAGES_FOLDER, f)
        for f in os.listdir(IMAGES_FOLDER)
        if f.endswith('.jpg')
    ]
    faces = []
    ids = []
    for path in paths:
        face, imagem = detecta_face(network, path)
        if face is not None:
            # Assumindo que o nome do arquivo contém o ID do indivíduo
            id = int(os.path.split(path)[1].split('.')[0].replace('ra', ''))
            ids.append(id)
            faces.append(face)
    return np.array(ids), faces


@app.route('/train', methods=['POST'])
def train_classifier():
    ids, faces = get_image_data()
    if len(faces) > 0:
        eigen_classifier = cv2.face.EigenFaceRecognizer_create()
        eigen_classifier.train(faces, ids)
        eigen_classifier.write(os.path.abspath('./api/content/gen_classifier.yml'))
        return jsonify({'message': 'Classificador treinado com sucesso.'}), 201
    else:
        return jsonify({'message': 'Nenhuma face detectada para treinamento.'}), 400


@app.route('/upload', methods=['POST'])
def upload_file():
    network = cv2.dnn.readNetFromCaffe(
        os.path.abspath('./api/content/deploy.prototxt.txt'),
        os.path.abspath('./api/content/res10_300x300_ssd_iter_140000.caffemodel'),
    )

    data = request.get_json(force=True)

    if data.get('encodedPicture') is None:
        return jsonify({'message': 'Não foi possível encontrar o arquivo.'}), 400

    picture = data['encodedPicture']

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'student.jpg')
    # Decodifica a imagem Base64 e a redimensiona para 320x243
    image_data = base64.b64decode(picture)
    image = Image.open(BytesIO(image_data))

    # Calcular proporção para corte centralizado
    aspect_ratio = 320 / 243
    img_ratio = image.width / image.height

    if img_ratio > aspect_ratio:
        new_height = image.height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = image.width
        new_height = int(new_width / aspect_ratio)

    left = (image.width - new_width) / 2
    top = (image.height - new_height) / 2
    right = (image.width + new_width) / 2
    bottom = (image.height + new_height) / 2

    # Cortar e redimensionar a imagem
    image = image.crop((left, top, right, bottom))
    image = image.resize((320, 243), Image.LANCZOS)

    image.save(image_path)

    face, imagem_processada = detecta_face(network, image_path)

    if face is not None:
        # Salvar a face detectada
        face_path = os.path.join(app.config['UPLOAD_FOLDER'], 'face.jpg')
        cv2.imwrite(face_path, face)

        # Carregar o classificador treinado
        eigen_classifier = cv2.face.EigenFaceRecognizer_create()
        eigen_classifier.read(os.path.abspath("./api/content/gen_classifier.yml"))

        # Classificar a face
        label, confidence = eigen_classifier.predict(face)

        return (
            jsonify(
                {
                    'message': 'Face detectada e classificada com sucesso.',
                    'label': label,
                    'confidence': confidence,
                }
            ),
            201,
        )
    else:
        return jsonify({'message': 'Nenhuma face detectada.'}), 400


if __name__ == '__main__':
    app.run(port=5000)
