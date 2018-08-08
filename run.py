from flask_migrate import Migrate
from flask_cors import CORS
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
                TsAppdownDaily=TsAppdownDaily, TsCertReportCount=TsCertReportCount)