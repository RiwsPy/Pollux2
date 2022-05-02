from flask import Flask
import os
from maps import Configs

app = Flask(__name__)
app.debug = os.getenv('ENV_DEV') == 'DVLP'
CONFIGS = Configs()
CONFIGS.load()

from . import views
