from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from app.models import TdAccount
from . import api
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = TdAccount.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = TdAccount.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    # if not g.current_user.is_anonymous:
    #     return forbidden('Unconfirmed account')
    pass


@api.route('/tokens/', methods=['POST'])
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials2')
    return jsonify({
      'token': g.current_user.generate_auth_token(expiration=432000),
      'user': g.current_user.to_json()
    })
