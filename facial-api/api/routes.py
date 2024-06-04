from flask import Flask, request
import os

UPLOAD_FOLDER = os.path.abspath('api/upload/')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload", methods = ['POST']) 
def upload_file():
    if 'file' not in request.files:
        return 'Não foi possível encontrar o arquivo.', 400
    
    file = request.files['file']

    if file.filename == '':
        return 'Nenhum arquivo selecionado.', 400 
    
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return 'ok', 201

if __name__ == '__main__':
    app.run(port=5000)