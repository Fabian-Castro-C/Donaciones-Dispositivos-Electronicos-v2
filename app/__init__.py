from flask import Flask
from app.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

from app import routes  # Importa las rutas

print(os.path.abspath(app.template_folder))