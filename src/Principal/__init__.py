from flask import Flask
from prometheus_flask_exporter import  PrometheusMetrics


app = Flask(__name__)

app.config.from_object("config")


metrics = PrometheusMetrics(app)

from .views import *


