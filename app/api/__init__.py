from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, product, users, errors, admin, apps, dashboard