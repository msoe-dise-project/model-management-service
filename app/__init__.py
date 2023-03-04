#!/usr/bin/env python

import datetime as dt
import os
import sys

from flask import Flask
from flask import request
from flask.json import jsonify

import psycopg2
from psycopg2.extras import Json

import app.database as db
from app.parameter_sets import blueprint as parameter_sets_blueprint
from app.projects import blueprint as projects_blueprint
from app.trained_models import blueprint as trained_models_blueprint

# this is effectively the main method
def create_app():
    app = Flask(__name__)
    
    db.check_environment_parameters()
    
    app.register_blueprint(parameter_sets_blueprint)
    app.register_blueprint(projects_blueprint)
    app.register_blueprint(trained_models_blueprint)

    return app
