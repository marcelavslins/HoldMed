import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS

# Get the absolute path to the backend directory
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

# Calculate the project root directory (one level up from backend)
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)

# Correct frontend dist path
FRONTEND_DIST = os.path.join(PROJECT_ROOT, 'frontend', 'dist')

app = Flask(__name__, static_folder=FRONTEND_DIST)
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS para permitir requisições do frontend
CORS(app, origins="*")

# Adiciona o diretório do projeto ao PYTHONPATH
sys.path.append(BACKEND_DIR)

from models.user import db
from models.patient import Patient, VitalSigns, LabResults, ClinicalNotes
from routes.user import user_bp
from routes.patient import patient_bp
from routes.ai import ai_bp

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(patient_bp, url_prefix='/api')
app.register_blueprint(ai_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(PROJECT_ROOT, 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # First try to serve the requested file
    requested_path = os.path.join(FRONTEND_DIST, path)
    if path != "" and os.path.exists(requested_path) and not os.path.isdir(requested_path):
        return send_from_directory(FRONTEND_DIST, path)
    
    # Then try to serve index.html
    index_path = os.path.join(FRONTEND_DIST, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(FRONTEND_DIST, 'index.html')
    
    # Detailed error message if index.html is missing
    return f"""
    <h2>index.html não encontrado!</h2>
    <p>Caminho esperado: {index_path}</p>
    
    <h3>Por favor verifique:</h3>
    <ol>
        <li>Você construiu o frontend? (execute <code>npm run build</code> na pasta frontend)</li>
        <li>O diretório de build existe em: {FRONTEND_DIST}</li>
        <li>Estrutura de diretórios esperada:
            <pre>
{PROJECT_ROOT}/
├── frontend/
│   ├── dist/       # ← Deve conter index.html
│   │   ├── index.html
│   │   ├── assets/
│   │   └── ...
├── backend/        # ← Esta aplicação Flask
│   └── app.py
└── database/
            </pre>
        </li>
    </ol>
    
    <h3>Diagnóstico:</h3>
    <ul>
        <li>Diretório do projeto: {PROJECT_ROOT}</li>
        <li>Pasta frontend/dist existe: {os.path.exists(FRONTEND_DIST)}</li>
        <li>index.html existe: {os.path.exists(index_path)}</li>
        <li>Conteúdo de frontend/dist: {os.listdir(FRONTEND_DIST) if os.path.exists(FRONTEND_DIST) else 'DIRETÓRIO NÃO EXISTE'}</li>
    </ul>
    """, 404

if __name__ == '__main__':
    # Print diagnostic information
    print(f"⚙️  Diretório do backend: {BACKEND_DIR}")
    print(f"⚙️  Diretório raiz do projeto: {PROJECT_ROOT}")
    print(f"⚙️  Pasta do frontend: {FRONTEND_DIST}")
    print(f"⚙️  index.html existe: {os.path.exists(os.path.join(FRONTEND_DIST, 'index.html'))}")
    
    if os.path.exists(FRONTEND_DIST):
        print(f"📂 Conteúdo de frontend/dist:")
        for item in os.listdir(FRONTEND_DIST):
            print(f"    - {item}")
    else:
        print(f"❌ Diretório frontend/dist não encontrado em: {FRONTEND_DIST}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)