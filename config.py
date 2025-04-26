# config.py
import os

# Chemins
CONTENT_DIR = os.path.join(os.path.dirname(__file__), 'static_content')

# Sécurité
# SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-key-à-remplacer')
SESSION_COOKIE_SECURE = True
