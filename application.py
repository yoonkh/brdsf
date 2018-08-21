from flask_migrate import Migrate
from app import create_app, db
from app.models import *

application = create_app()
app = application
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "<h1>Welcome to API</h1>"

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, TcResult=TcResult, TcRole=TcResult, TdAccount= TdAccount, TdAdmin=TdAdmin,
                TdApp=TdApp, TdBanner=TdBanner, TdBlackList=TdBlackList, TdCompany=TdCompany,
                TdDevice=TdDevice, TdHolotag=TdHolotag, TdLocationTerm= TdLocationTerm, TdModel= TdModel,
                TdRetailer=TdRetailer, TdServiceTerm=TdServiceTerm, TdTagVersion=TdTagVersion, ThCertification=ThCertification,
                ThReport=ThReport, TiHolotag=TiHolotag, TlLogin=TlLogin, TsActiveUniqueCount= TsActiveUniqueCount,
                TsAppdownDaily=TsAppdownDaily, TsCertReportCount=TsCertReportCount, BlacklistTong=BlacklistTong)

@app.cli.command()
def deploy():
    """Run deployment tasks"""
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.insert_roles()

    # create or update date types
    DateType.insert_date_types()

    # create or update user department
    Team.insert_teams()

    # create users, projects and worktimes
    # read_user()
    # read_project()