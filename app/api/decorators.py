from functools import wraps
from flask import g
from .errors import forbidden
from ..models import TdAccount

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def accessible_oneself():
    def decorator(f):
        @wraps(f)
        def wrapper(id, *args, **kwargs):
            user = TdAccount.query.get_or_404(id)
            g.user = user
            if g.current_user is not user:
                return forbidden('Insufficient permissions')
            return f(id, *args, **kwargs)
        return wrapper
    return decorator