from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, product, company, errors, admin, apps, dashboard

