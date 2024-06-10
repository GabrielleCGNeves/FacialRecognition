from io import BytesIO
from flask import Flask, request, jsonify
import base64
import os
import cv2
import numpy as np
from PIL import Image, ImageOps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

UPLOAD_FOLDER = os.path.abspath("api/upload/")
IMAGES_FOLDER = os.path.abspath("./api/images")

db = SQLAlchemy()

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///attendance.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# Tabela de presença
# Modelo de Presença
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Integer, db.ForeignKey("student.label"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# Modelo de Aluno
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    attendances = db.relationship("Attendance", backref="student", lazy=True)


# Inicializar o banco de dados
with app.app_context():
    print("Inicializando banco de dados...")
    db.create_all()

    # Adicionar registros prévios, se não existirem
    if Student.query.count() == 0:
        print("Adicionando registros prévios na tabela Student...")
        students = [
            Student(label=2008, name="ERICK SANTOS SOUSA"),
            Student(label=2013, name="GEOVANNA GABRIELLE"),
            Student(label=2026, name="GABRIELLE C G NEVES"),
        ]
        db.session.bulk_save_objects(students)
        db.session.commit()
        print("Registros adicionados com sucesso.")
    else:
        print("Registros já existem na tabela Student.")


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
        os.path.abspath("./api/content/deploy.prototxt.txt"),
        os.path.abspath("./api/content/res10_300x300_ssd_iter_140000.caffemodel"),
    )
    paths = [
        os.path.join(IMAGES_FOLDER, f)
        for f in os.listdir(IMAGES_FOLDER)
        if f.endswith(".jpg")
    ]
    faces = []
    ids = []
    for path in paths:
        face, imagem = detecta_face(network, path)
        if face is not None:
            # Assumindo que o nome do arquivo contém o ID do indivíduo
            id = int(os.path.split(path)[1].split(".")[0].replace("ra", ""))
            ids.append(id)
            faces.append(face)
    return np.array(ids), faces


@app.route("/train", methods=["POST"])
def train_classifier():
    ids, faces = get_image_data()
    if len(faces) > 0:
        eigen_classifier = cv2.face.EigenFaceRecognizer_create()
        eigen_classifier.train(faces, ids)
        eigen_classifier.write(os.path.abspath("./api/content/gen_classifier.yml"))
        return jsonify({"message": "Classificador treinado com sucesso."}), 201
    else:
        return jsonify({"message": "Nenhuma face detectada para treinamento."}), 400


@app.route("/upload", methods=["POST"])
def upload_file():
    network = cv2.dnn.readNetFromCaffe(
        os.path.abspath("./api/content/deploy.prototxt.txt"),
        os.path.abspath("./api/content/res10_300x300_ssd_iter_140000.caffemodel"),
    )

    data = request.get_json(force=True)

    if data.get("encodedPicture") is None:
        return jsonify({"message": "Não foi possível encontrar o arquivo."}), 400

    picture = data["encodedPicture"]

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], "student.jpg")
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
        face_path = os.path.join(app.config["UPLOAD_FOLDER"], "face.jpg")
        cv2.imwrite(face_path, face)

        # Carregar o classificador treinado
        eigen_classifier = cv2.face.EigenFaceRecognizer_create()
        eigen_classifier.read(os.path.abspath("./api/content/gen_classifier.yml"))

        # Classificar a face
        label, confidence = eigen_classifier.predict(face)

        # Buscar o nome do aluno pelo label
        student = Student.query.filter_by(label=label).first()

        if student:
            name = student.name
            # Buscar a última presença
            last_attendance = (
                Attendance.query.filter_by(label=label)
                .order_by(Attendance.timestamp.desc())
                .first()
            )
            last_attendance_date = (
                last_attendance.timestamp if last_attendance else None
            )
        else:
            name = "Desconhecido"
            last_attendance_date = None

        return (
            jsonify(
                {
                    "message": "Face detectada e classificada com sucesso.",
                    "label": label,
                    "name": name,
                    "confidence": confidence,
                    "last_attendance": last_attendance_date,
                }
            ),
            201,
        )
    else:
        return jsonify({"message": "Nenhuma face detectada."}), 400

@app.route("/attendance", methods=["POST"])
def record_attendance():
    data = request.get_json(force=True)

    if "label" not in data:
        return jsonify({"message": "Label não fornecido."}), 400

    label = data["label"]

    # Registrar presença no banco de dados
    attendance = Attendance(label=label)
    db.session.add(attendance)
    db.session.commit()

    return jsonify({"message": "Presença registrada com sucesso."}), 201

if __name__ == "__main__":
    app.run(port=5000)