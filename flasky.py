from flask_migrate import Migrate
from app import create_app, db
from app.models import CustomerAccount, CustomerCompany, Role

app = create_app()
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, CustomerCompany=CustomerCompany, CustomerAccount=CustomerAccount, Role=Role)



# @app.cli.command()
# def deploy():
#     """Run deployment tasks."""
#     # migrate database to latest revision
#     upgrade()
#
#     # create or update user roles
#     Role.insert_roles()
#
#     # ensure all users are following themselves
#     User.add_self_follows()
