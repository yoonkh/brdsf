from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from .exceptions import ValidationError
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR, ENUM, INTEGER, TEXT, DATETIME, CHAR, SMALLINT, BIGINT
from . import db


# class Role(db.Model):
#     __tablename__ = 'tc_role'
#     idx = db.Column(INTEGER(11), primary_key=True)
#     code = db.Column(TINYINT(4), unique=True, default='NULL')
#     name_kr = db.Column(VARCHAR(45), default='NULL')
#     name_en = db.Column(VARCHAR(45), default='NULL')
#     name_zh = db.Column(VARCHAR(45), default='NULL')
#     name_kr_forAccount = db.Column(VARCHAR(45), default='NULL')
#     name_en_forAccount = db.Column(VARCHAR(45), default='NULL')
#     name_zh_forAccount = db.Column(VARCHAR(45), default='NULL')
#     state = db.Column(ENUM('Registered','Deleted','Paused'), default='NULL')
#     description = db.Column(TEXT, default='NULL')
#     dtRegistered = db.Column(DATETIME, default='NULL')
#     dtModified = db.Column(DATETIME, default='NULL')
#     isIcraft = db.Column(TINYINT(1), default=0)
#     icraft_role = db.relationship('ICraftAccount', backref='role', lazy='dynamic')
#     customer_role = db.relationship('CustomerAccount', backref='role', lazy='dynamic')
#
#
# class LoginResult(db.Model):
#     __tablename__ = 'tc_result'
#     idx = db.Column(db.Integer, primary_key=True)
#     code = db.Column(VARCHAR(20), unique=True)
#     msg_kr = db.Column(VARCHAR(20))
#     msg_en = db.Column(VARCHAR(20), default='NULL')
#     msg_zh= db.Column(VARCHAR(20), default='NULL')
#     msg = db.Column(VARCHAR(20))
#
#
# class App(db.Model):
#     __tablename__ = 'td_app'
#     idx = db.Column(db.Integer, primary_key=True)
#     code = db.Column(VARCHAR(20), default='NULL')
#     name_kr = db.Column(VARCHAR(20), default='NULL')
#     name_en = db.Column(VARCHAR(20), default='NULL')
#     name_zh = db.Column(VARCHAR(20), default='NULL')
#     version = db.Column(VARCHAR(20))
#     type = db.Column(VARCHAR(20))
#     tagType = db.Column(VARCHAR(20))
#     companyCode = db.Column(VARCHAR(20), db.ForeignKey('td_company.code'))
#     registrant = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'))
#     dtRegistered = db.Column(VARCHAR(20))
#     modifier = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'))
#     dtModified = db.Column(VARCHAR(20))
#     note = db.Column(VARCHAR(20), default='NULL')
#     dtPublished = db.Column(VARCHAR(20), default='NULL')
#     attachedPath = db.Column(VARCHAR(20), default='NULL')
#     osType = db.Column(VARCHAR(20))
#     state = db.Column(VARCHAR(20), default='Disable')
#     description = db.Column(VARCHAR(20), default='NULL')
#     limitCertHour = db.Column(VARCHAR(20), default='8')
#     limitCertCnt = db.Column(VARCHAR(20), default='50')
#     updateUrl = db.Column(VARCHAR(20), default='NULL')
#
#
# class Serviceterm(db.Model):
#     __tablename__ = 'td_service_term'
#     idx = db.Column(db.Integer, primary_key=True)
#     appTagType = db.Column(VARCHAR(20), default='H')
#     version = db.Column(VARCHAR(20), unique=True)
#     title = db.Column(VARCHAR(20))
#     termUrl = db.Column(VARCHAR(20))
#     state = db.Column(VARCHAR(20))
#     dtRegistered = db.Column(VARCHAR(20), default='NULL')
#     dtPublished = db.Column(VARCHAR(20), default='NULL')
#     dtDeleted = db.Column(VARCHAR(20))
#
#
# class Locationterm(db.Model):
#     __tablename__ = 'td_location_term'
#     idx = db.Column(db.Integer, primary_key=True)
#     version = db.Column(VARCHAR(20), unique=True)
#     title = db.Column(VARCHAR(20))
#     termUrl = db.Column(VARCHAR(20))
#     state = db.Column(VARCHAR(20))
#     dtRegistered = db.Column(VARCHAR(20), default='NULL')
#     dtPublished = db.Column(VARCHAR(20), default='NULL')
#     dtDeleted = db.Column(VARCHAR(20))
#
#
# class DeviceModel(db.Model):
#     __tablename__ = 'td_model'
#     idx = db.Column(db.Integer, primary_key=True)
#     name= db.Column(VARCHAR(20), unique=True)
#     osType = db.Column(VARCHAR(20))
#     resolution = db.Column(VARCHAR(20), default='NULL')
#     dtRegistered = db.Column(VARCHAR(20))
#     dtModified = db.Column(VARCHAR(20))
#
#
# class Device(db.Model):
#     __tablename__ = 'td_device'
#     idx = db.Column(db.Integer, primary_key=True)
#     pushToken = db.Column(VARCHAR(20))
#     model = db.Column(VARCHAR(20))
#     osVersion = db.Column(VARCHAR(20))
#     appVersion = db.Column(VARCHAR(20))
#     appCode = db.Column(VARCHAR(20), db.Foreingnkey('td_app.code'), default='NULL')
#     appTagType = db.Column(VARCHAR(20), default='H')
#     agreeTerm = db.Column(db.Integer, default=0)
#     agreeGPS = db.Column(db.Integer, default=0)
#     useBackground = db.Column(db.Integer, default=1)
#     language = db.Column(VARCHAR(20))
#     languageCode = db.Column(VARCHAR(20), default='NULL')
#     serverName = db.Column(VARCHAR(20), default='NULL')
#     state = db.Column(VARCHAR(20))
#     dtRegistered = db.Column(VARCHAR(20))
#     dtLastConnected = db.Column(VARCHAR(20))
#     dtTermAgreement = db.Column(VARCHAR(20), default='NULL')
#     serviceTermVersion = db.Column(VARCHAR(20), db.Freingkey('td_servive_term.version'), default='NULL')
#     locationTermVersion = db.Column(VARCHAR(20), db.Freingkey('td_location_term.version'), default='NULL')
#     ipAddr = db.Column(VARCHAR(20), default='NULL')
#
#
# class ICraftAccount(db.Model):
#     __tablename__ = 'td_admin'
#     idx = db.Column(INTEGER(11), primary_key=True)
#     id = db.Column(VARCHAR(20), unique=True)
#     pwd = db.Column(VARCHAR(45))
#     email = db.Column(VARCHAR(100), nullable=False)
#     name = db.Column(VARCHAR(40), nullable=False)
#     phone = db.Column(VARCHAR(20))
#     telephone = db.Column(VARCHAR(20))
#     role = db.Column(TINYINT(4), db.ForeignKey('tc_role.code'), index=True)
#     position = db.Column(VARCHAR(20), default='NULL')
#     department = db.Column(VARCHAR(45), default='NULL')
#     state = db.Column(ENUM('Registered','Deleted','Paused'))
#     registrant = db.Column(VARCHAR(20), default='NULL')
#     dtRegistered = db.Column(DATETIME)
#     modifier = db.Column(VARCHAR(20), default='NULL')
#     dtModified = db.Column(DATETIME)
#     dtLastConnected = db.Column(DATETIME, default='NULL')
#     note = db.Column(TEXT, default='NULL')
#     failCount = db.Column(SMALLINT(6), default=0)
#     company_registrant = db.relationship('CustomerCompany', backref='registrant', lazy='dynamic')
#     company_modifier = db.relationship('CustomerCompany', backref='modifier', lazy='dynamic')
#
#
# class Holotageimage(db.Model):
#     __tablename__ = 'ti_holotag'
#     idx = db.Column(db.Integer, primary_key=True)
#     name = db.Column(VARCHAR(20), unique=True)
#     tagIdx = db.Column(db.Integer, db.ForeignKey('td_holotag.idx'))
#     path = db.Column(VARCHAR(20))
#     state = db.Column(VARCHAR(20))
#     registarant = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'))
#     dtRegistered = db.Column(VARCHAR(20))
#     modigier = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'))
#     dtModified = db.Column(VARCHAR(20))
#     note = db.Column(VARCHAR(20),default='NULL')
#
#
#
# class CustomerCompany(db.Model):
#     __tablename__ = 'td_company'
#     idx = db.Column(INTEGER(11), primary_key=True)
#     code = db.Column(VARCHAR(10), unique=True)
#     name_kr = db.Column(VARCHAR(100))
#     name_en = db.Column(VARCHAR(100), default='NULL')
#     name_zh = db.Column(VARCHAR(100), default='NULL')
#     registrationNumber = db.Column(VARCHAR(45))
#     businessRegistrationUrl = db.Column(VARCHAR(64), default='NULL')
#     addr_kr = db.Column(TEXT)
#     addr_en = db.Column(TEXT, default='NULL')
#     addr_zh = db.Column(TEXT, default='NULL')
#     telephone = db.Column(VARCHAR(20), default='NULL')
#     fax=db.Column(VARCHAR(20), default='NULL')
#     delegator_kr = db.Column(VARCHAR(40))
#     delegator_en = db.Column(VARCHAR(45), default='NULL')
#     delegator_zh = db.Column(VARCHAR(45), default='NULL')
#     state = db.Column(ENUM('Registered','Deleted','Paused'))
#     registrant = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), index=True)
#     dtRegistered = db.Column(DATETIME)
#     modifier = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), index=True)
#     dtModified = db.Column(DATETIME)
#     note = db.Column(TEXT, default='NULL')
#     ci = db.Column(TEXT)
#     url = db.Column(TEXT)
#     description_kr = db.Column(TEXT, default='NULL')
#     description_en = db.Column(TEXT, default='NULL')
#     description_zh = db.Column(TEXT, default='NULL')
#     tntLogoImgUrl = db.Column(VARCHAR(64))
#     customer_companycode = db.relationship('CustomerAccount', backref='companyCode', lazy='dynamic')


#
class CustomerAccount(db.Model):
    __tablename__ = 'td_account'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    id = db.Column(VARCHAR(20), nullable=False, unique=True)
    pwd = db.Column(VARCHAR(45), nullable=False)
    email = db.Column(VARCHAR(100), nullable=False)
    name_kr = db.Column(VARCHAR(40), nullable=False, index=True)
    name_en = db.Column(VARCHAR(40), default='NULL')
    name_zh = db.Column(VARCHAR(40), default='NULL')
    phone = db.Column(VARCHAR(20), nullable=False, index=True)
    telephone = db.Column(VARCHAR(20), nullable=False)
    fax = db.Column(VARCHAR(20), default='NULL')
    companyCode = db.Column(CHAR(10), db.ForeignKey('td_company.code'), nullable=False, index=True)
    role = db.Column(TINYINT(4), db.ForeignKey('tc_role.code'), nullable=False, index=True)
    position = db.Column(VARCHAR(20), default='NULL')
    department = db.Column(VARCHAR(40), default='NULL')
    state = db.Column(ENUM('Registered','Deleted','Paused'))
    registrant = db.Column(VARCHAR(20))
    dtRegistered = db.Column(DATETIME)
    modifier = db.Column(VARCHAR(20))
    dtModified = db.Column(DATETIME)
    dtLastConnected = db.Column(DATETIME, default='NULL')
    note = db.Column(TEXT, default='NULL')
    failCount = db.Column(SMALLINT(6), default=0)


#
class ProductManagement(db.Model):
    __tablename__ = 'td_holotage'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    code = db.Column(CHAR(10), nuique=True, nullable=False)
    name_kr = db.Column(VARCHAR(100), nullable=False)
    name_en = db.Column(VARCHAR(45), default='NULL')
    name_zh = db.Column(VARCHAR(45), default='NULL')
    companyCode = db.Column(CHAR(10), db.ForeignKey('td_company.code'), nuique=True, default='NULL', index=True)
    #레퍼런스 달아야함
    state = db.Column(ENUM('Registered','Deleted','Paused'), nullable=False)
    attachType = db.Column(ENUM('LABELBOX','POUCH','POUCH_PRINT'), default='NULL')
    certOverCnt = db.Column(INTEGER(11), default='NULL')
    certOverManyCnt = db.Column(INTEGER(11), default='NULL')
    registrant = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), nullable=False, index=True)
    # 레퍼런스 달아야함
    dtRegistered = db.Column(DATETIME, nullable=False)
    modifier = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), nullable=False, index=True)
    # 레퍼런스 달아야함
    dtModified = db.Column(DATETIME, nullable=False)
    sourceImage = db.Column(TEXT, nullable=False)
    note = db.Column(TEXT, default='NULL')
    mappingCode = db.Column(CHAR(11), nullable=False, index=True)
    sqrUrl = db.Column(VARCHAR(10), default='NULL')
    hVersion = db.Column(VARCHAR(32), db.ForeignKey('td_tag_version.version'), default='NULL', index=True)
    sqrVer = db.Column(INTEGER(2), nullable=False, default=0)

#
class TagtypeManagement(db.Model):
    __tablename__ = 'td_tag_version'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    version = db.Column(CHAR(11), unique=True, nullable=False)
    type = db.Column(ENUM('HOLOTAG_ONLY','HOLOTAG_BARCODE','HYBRIDTAG','RANDOMTAG','SQRTAG'), nullable=False)
    name_kr = db.Column(VARCHAR(60), nullable=False)
    name_en = db.Column(VARCHAR(60), nullable=False)
    name_zh = db.Column(VARCHAR(60), nullable=False)
    state = db.Column(ENUM('Enalbe','Disable','Deleted'), default='Disable', nullable=False)
    width = db.Column(INTEGER(11), nullable=False)
    height =db.Column(INTEGER(11), nullable=False)
    description = db.Column(TEXT, nullable=False)
    registrant = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), nullable=False)
    # 레퍼런스 달아야함
    dtRegistered = db.Column(DATETIME, nullable=False)
    modifier = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), nullable=False)
    # 레퍼런스 달아야함
    dtModified = db.Column(DATETIME, default='NULL')
    note = db.Column(TEXT)
    tag_version = db.relationship('td_holotag', backref='hVersion', lazy='dynamic')
    tag_certification = db.relationship('td_certification', backref='hVersion', lazy='dynamic')
    tag_report = db.relationship('th_report', backref='hVersion', lazy='dynamic')

class ProductCertification(db.Model):
    __tablename__ = 'th_certification'
    idx = db.Column(BIGINT(20), primary_key=True, nullable=False, autoincrement=True)
    deviceID = db.Column(VARCHAR(50), nullable=False)
    companyCode = db.Column(CHAR(10), db.ForeignKey('td_company.code'), default='NULL')
    #ref need
    tagType = db.Column(ENUM('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG', 'RANDOMTAG', 'SQRTAG'), default='NULL')
    tagCode = db.Column(CHAR(10), default='NULL')
    hVersion = db.Column(CHAR(11), db.ForeignKey('td_tag_vesion.version'), default='NULL')
    mappingCode = db.Column(VARCHAR(10), default='NULL')
    image = db.Colmn(VARCHAR(128), default='NULL')
    result = db.Colmn(ENUM('Genuine', 'Counterfeit', 'Revalidation', 'Exprired', 'Invalid', 'Retry', 'OverCert', 'DifferentQR', 'CommonQR', 'NotiOverCert'), nullable=False)
    resultDetail = db.Colmn(INTEGER(4), default=0)
    osType = db.Colmn(ENUM('iOS', 'Android', 'Unknown', 'Web'), nullable=False)
    dtCertificate = db.Column(DATETIME, nullable=False)
    longitude = db.Column(VARCHAR(45), default='NULL')
    latitude = db.Column(VARCHAR(45), default='NULL')
    regionIdx = db.Column(BIGINT(10), nullable=False, default=-1)
    random = db.Column(CHAR(16), default='NULL')
    randomCnt = db.Column(INTEGER(10), default=0)
    retailerID = db.Column(VARCHAR(10), default='NULL')
    mode = db.Column(ENUM('V', 'P'), default='NULL')
    data = db.Column(VARCHAR(64), default='NULL')



class Report(db.Model):
    __tablename__ = 'th_report'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    deviceID = db.Column(VARCHAR(50), db.ForeignKey('td_device.pushToken'), nullable=False, index=True)
    #ref need
    companyCode = db.Column(CHAR(10), db.ForeignKey('td_company.code'), default='NULL', index=True)
    # ref need
    tagCode = db.Column(CHAR(10), default='NULL', index=True)
    hVersion = db.Column(CHAR(11), db.ForeignKey('td_tag_vesion.version'), default='NULL, index=True')
    image = db.Colmn(TEXT, nullable=False)
    imageProduct = db.Colmn(TEXT, default='NULL')
    latitude = db.Colmn(VARCHAR(45), default='NULL')
    longitude = db.Colmn(VARCHAR(45), default='NULL')
    address = db.Colmn(VARCHAR(256), default='NULL')
    dtCreated = db.Colmn(DATETIME, nullable=False, index=True)
    email = db.Colmn(VARCHAR(100), default='NULL')
    content = db.Colmn(TEXT, default='NULL')
    category = db.Colmn(INTEGER(11), default='NULL')
    contact = db.Colmn(VARCHAR(64), default='NULL')
    contactType = db.Colmn(ENUM('CONTACT_NUM', 'WECHAT', 'LINE', 'KAKAOTALK'), default='NULL')
    purchasePlace = db.Colmn(VARCHAR(120), default='NULL')
    onlinePurchasePlace = db.Colmn(VARCHAR(220), default='NULL')
    purchaseDate = db.Colmn(VARCHAR(8), default='NULL')
    type = db.Colmn(ENUM('Report', 'Expire', 'Share', 'Invalid'), nullable=False)
    tagType = db.Column(ENUM('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG', 'RANDOMTAG', 'SQRTAG'), default='NULL')
    mappingCode = db.Column(VARCHAR(10), default='NULL')
    random = db.Colmn(VARCHAR(16), default='NULL')
    retailerID = db.Colmn(VARCHAR(10), default='NULL')
    state = db.Colmn(ENUM('Question', 'Answer', 'Holding'), nullable=False, default='Question')
    answerer = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), default='NULL', index=True)
    # ref need
    dtAnswer = db.Column(DATETIME, default='NULL')
    aContent = db.Column(TEXT, default='NULL')
    osType = db.Colmn(ENUM('iOS', 'Android', 'Unknown'), nullable=False)
    memo = db.Colmn(TEXT, default='NULL')
    certificationIdx = db.Column(BIGINT(20), default=-1)
    importantYN = db.Colmn(ENUM('Y', 'N'), nullable=False, default='N')
    codeState = db.Colmn(VARCHAR(6), default='NULL')
    codeChannel = db.Colmn(VARCHAR(6), default='NULL')
    resultDetail = db.Column(INTEGER(4), nullable=False, default=0)
    data = db.Colmn(VARCHAR(64), default='NULL')

class Loginlog(db.Model):
    __tablename__ = 'tl_login'
    idx = db.Column(BIGINT(20), primary_key=True, nullable=False, autoincrement=True)
    id = db.Column(VARCHAR(20), nullable=False)
    resultCode = db.Column(CHAR(4), nullable=False)
    dtAttempted = db.Column(DATETIME, nullable=False)
    remoteAddr = db.Column(VARCHAR(23), nullable=False)

class Blacklist(db.Model):
    __tablename__ = 'td_black_list'
    idx = db.Column(INTEGER(11), nullable=False, autoincrement=True, index=True)
    pushToken = db.Colmn(VARCHAR(50), primary_key=True, nullable=False)
    blType = db.Colmn(ENUM('C', 'O'), nullable=False, default='C')
    delYN = db.Colmn(VARCHAR(1), nullable=False, default='N')
    dtRegistered = db.Colmn(DATETIME, nullable=False)
    registrant = db.Colmn(VARCHAR(50), nullable=False, default='CURRENT_TIMESTAMP')
    dtModified = db.Colmn(DATETIME, nullable=False, default='CURRENT_TIMESTAMP')
    modifier = db.Colmn(VARCHAR(50), nullable=False)


class ActiveUniqueCount(db.Model):
    __tablename__ = 'ts_active_unique_count'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    companyCode = db.Column(VARCHAR(10), default='NULL', index=True)
    appTagType = db.Column(CHAR(1), nullable=False, default='H')
    osType = db.Column(ENUM('iOS', 'Android', 'Unknown'), nullable=False, index=True)
    date = db.Column(CHAR(8), nullable=False, index=True)
    active_count = db.Column(INTEGER(11), nullable=False, default=0)
    unique_count = db.Column(INTEGER(11), nullable=False, default=0)
    cert_unique_count = db.Column(INTEGER(11), nullable=False, default=0)
    regApp_count = db.Column(INTEGER(11), default='N')
    registerDt = db.Column(DATETIME, default='CURRENT_TIMESTAMP')

class AppdownDaily(db.Model):
    __tablename__ = 'ts_appdown_daily'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    date = db.Column(CHAR(8), nullable=False)
    companyCode = db.Column(VARCHAR(10), db.ForeignKey('td_company.code'), default='NULL', index=True)
    #ref need
    osType = db.Column(ENUM('iOS', 'Android', 'Unknown'), nullable=False)
    tagType = db.Column(ENUM('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG'), default='NULL')
    downloadCount = db.Column(INTEGER(11), nullable=False, default=0)


class CertReportCount(db.Model):
    __tablename__ = 'ts_cert_report_count'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    companyCode = db.Column(VARCHAR(10), default='NULL', index=True)
    tagType = db.Column(ENUM('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG', 'RANDOMTAG', 'SQRTAG'), default='NULL')
    tagCode = db.Column(VARCHAR(10), default='NULL', index=True)
    osType = db.Column(ENUM('iOS', 'Android', 'Unknown'), nullable=False, index=True)
    type = db.Column(VARCHAR(30), nullable=False, index=True)
    date = db.Column(CHAR(8), nullable=False, index=True)
    count = db.Column(INTEGER(11), default=0, nullable=False)
    registerDt = db.Column(DATETIME, default='NULL')


class Retailer(db.Model):
    __tablename__ = 'td_retailer'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    rtid = db.Column(CHAR(10), nullable=False, index=True)
    name_kr = db.Column(VARCHAR(100), nullable=False)
    name_en = db.Column(VARCHAR(45), default='NULL')
    name_zh = db.Column(VARCHAR(45), default='NULL')
    companyCode = db.Column(CHAR(10), db.ForeignKey('td_company.code'), default='NULL', index=True)
    #ref need
    state = db.Column(ENUM('Registered', 'Deleted', 'Paused'), default='Registered')
    note = db.Column(VARCHAR(512), default='NULL')
    headerquarterYN = db.Column(ENUM('Y', 'N'), nullable=False, default='N')
    registrant = db.Column(VARCHAR(20), nullable=False)
    dtRegistered = db.Column(DATETIME, nullable=False, default='CURRENT_TIMESTAMP')
    modifier = db.Column(VARCHAR(20), default='NULL')
    dtModified = db.Column(DATETIME, default='NULL')
