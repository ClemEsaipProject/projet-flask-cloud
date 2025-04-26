# app.py
from flask import Flask, jsonify, render_template, request
from marshmallow import Schema, fields, ValidationError
import yaml
import json
import os
import logging
from functools import lru_cache
from dotenv import load_dotenv

# Chargement de la configuration
load_dotenv()
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# Schémas de validation Marshmallow
# --------------------------------------------------

class EventSchema(Schema):
    titre = fields.Str(required=True)
    date = fields.Date(required=True)
    lieu = fields.Str(required=True)
    description = fields.Str()

class NewsSchema(Schema):
    titre = fields.Str(required=True)
    contenu = fields.Str(required=True)
    auteur = fields.Str(required=True)
    date_publication = fields.Date()

# --------------------------------------------------
# Fonctions de chargement avec cache et gestion d'erreurs
# --------------------------------------------------

@lru_cache(maxsize=32)
def load_static_content(filename):
    """Charge les fichiers statiques avec cache et gestion d'erreurs"""
    try:
        content_path = os.path.join(app.config['CONTENT_DIR'], filename)
        logger.info(f"Tentative de chargement de {content_path}")
        
        if not os.path.exists(content_path):
            logger.error(f"Fichier non trouvé: {content_path}")
            return []  # Retourne une liste vide plutôt que None
            
        with open(content_path, 'r', encoding='utf-8') as f:
            if filename.endswith('.yaml'):
                data = yaml.safe_load(f)
            else:
                data = json.load(f)
                
            return data
            
    except Exception as e:
        logger.error(f"Erreur de chargement {filename}: {str(e)}")
        return []  # Retourne une liste vide en cas d'exception


# --------------------------------------------------
# Endpoints API
# --------------------------------------------------

@app.route('/api/events', methods=['GET'])
def get_events():
    """Endpoint pour les événements"""
    events = load_static_content('events.json')
    return jsonify(events)  # Retourne toujours une réponse JSON valide


@app.route('/api/news', methods=['GET'])
def get_news():
    """Endpoint pour les actualités"""
    news = load_static_content('news.yaml')
    return jsonify(news) if news else ('Fichier news.yaml non trouvé ou invalide', 404)

# --------------------------------------------------
# Interface utilisateur
# --------------------------------------------------

@app.route('/')
def dashboard():
    """Dashboard de visualisation des données"""
    events = load_static_content('events.json') or []
    news = load_static_content('news.yaml') or []
    return render_template('dashboard.html', events=events, news=news)


# --------------------------------------------------
# Gestion des erreurs
# --------------------------------------------------

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({"error": "Données invalides", "details": e.messages}), 400

# --------------------------------------------------
# Configuration et exécution
# --------------------------------------------------

if __name__ == '__main__':
    # Mode production avec Gunicorn
    if os.getenv('FLASK_ENV') == 'production':
        app.run(host='0.0.0.0', port=5000)
    else:
        # Mode développement avec rechargement automatique
        app.run(debug=True, host='0.0.0.0', port=5000)
