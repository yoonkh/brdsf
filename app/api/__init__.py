from flask import Blueprint

api = Blueprint('api', __name__)

from . import admin, apps, authentication, decorators, errors, product