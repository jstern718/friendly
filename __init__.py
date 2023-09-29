from flask import Flask
from .views.admin import admin

app = Flask(__name__)


# Registering blueprints
app.register_blueprint(admin)