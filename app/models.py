from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from .exceptions import ValidationError
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR, ENUM, INTEGER, TEXT, DATETIME, CHAR, SMALLINT, BIGINT
from . import db

class Role(db.Model):
    __tablename__ = 'tc_role'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    code = db.Column(TINYINT(4), unique=True)
    name_kr = db.Column(VARCHAR(45), nullable=False)
    name_en = db.Column(VARCHAR(45), default='NULL')
    name_zh = db.Column(VARCHAR(45), default='NULL')
    name_kr_forAccount = db.Column(VARCHAR(45), default='NULL')
    name_en_forAccount = db.Column(VARCHAR(45), default='NULL')
    name_zh_forAccount = db.Column(VARCHAR(45), default='NULL')
    state = db.Column(ENUM('Registered','Deleted','Paused'), nullable=False)
    description = db.Column(TEXT, default='NULL')
    dtRegistered = db.Column(DATETIME, nullable=False)
    dtModified = db.Column(DATETIME, nullable=False)
    isIcraft = db.Column(TINYINT(1), nullable=False, default=0)
    icraft_role = db.relationship('ICraftAccount', backref='role', lazy='dynamic')
    customer_role = db.relationship('CustomerAccount', backref='role', lazy='dynamic')




class LoginResult(db.Model):
    __tablename__ = 'tc_result'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    code = db.Column(CHAR(4), unique=True, nullable=False)
    msg_kr = db.Column(VARCHAR(200), nullable=False)
    msg_en = db.Column(VARCHAR(200), default='NULL')
    msg_zh= db.Column(VARCHAR(200), default='NULL')
    msg = db.Column(TEXT, nullable=False)



class Serviceterm(db.Model):
    __tablename__ = 'td_service_term'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    appTagType = db.Column(CHAR(1), nullable=False, default='H')
    version = db.Column(VARCHAR(20), nullable=False, unique=True)
    title = db.Column(VARCHAR(255), nullable=False)
    termUrl = db.Column(VARCHAR(45), nullable=False)
    state = db.Column(ENUM('Registered', 'Deleted', 'Published'), nullable=False)
    dtRegistered = db.Column(DATETIME, default='NULL')
    dtPublished = db.Column(DATETIME, default='NULL')
    dtDeleted = db.Column(DATETIME)
    device_serviceTermVersion = db.relationship('Device', backref='serviceTermVersion', lazy='dynamic')



class Locationterm(db.Model):
    __tablename__ = 'td_location_term'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    version = db.Column(VARCHAR(20), nullable=False, unique=True)
    title = db.Column(VARCHAR(255), nullable=False)
    termUrl = db.Column(VARCHAR(45), nullable=False)
    state = db.Column(ENUM('Registered', 'Deleted', 'Published'), nullable=False)
    dtRegistered = db.Column(DATETIME, default='NULL')
    dtPublished = db.Column(DATETIME, default='NULL')
    dtDeleted = db.Column(DATETIME)
    device_locationTermVersion = db.relationship('Device', backref='locationTermVersion', lazy='dynamic')



class DeviceModel(db.Model):
    __tablename__ = 'td_model'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    name= db.Column(VARCHAR(50), nullable=False, unique=True, index=True)
    osType = db.Column(ENUM('iOS', 'Android', 'Unknown'), nullable=False, index=True)
    resolution = db.Column(TEXT, default='NULL')
    dtRegistered = db.Column(DATETIME, nullable=False)
    dtModified = db.Column(DATETIME, nullable=False)



class ICraftAccount(db.Model):
    __tablename__ = 'td_admin'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    id = db.Column(VARCHAR(20), nullable=False, unique=True)
    pwd = db.Column(VARCHAR(45), nullable=False)
    email = db.Column(VARCHAR(100), nullable=False)
    name = db.Column(VARCHAR(40), nullable=False)
    phone = db.Column(VARCHAR(20), nullable=False)
    telephone = db.Column(VARCHAR(20), nullable=False)
    role = db.Column(TINYINT(4), nullable=False, index=True)
    position = db.Column(VARCHAR(20), default='NULL')
    department = db.Column(VARCHAR(45), default='NULL')
    state = db.Column(ENUM('Registered','Deleted','Paused'), nullable=False)
    registrant = db.Column(VARCHAR(20), default='NULL')
    dtRegistered = db.Column(DATETIME, nullable=False)
    modifier = db.Column(VARCHAR(20), default='NULL')
    dtModified = db.Column(DATETIME, nullable=False)
    dtLastConnected = db.Column(DATETIME, default='NULL')
    note = db.Column(TEXT, default='NULL')
    failCount = db.Column(SMALLINT(6), default=0)
    company_registrant = db.relationship('CustomerCompany', backref='registrant', lazy='dynamic')
    company_modifier = db.relationship('CustomerCompany', backref='modifier', lazy='dynamic')
    app_registrant = db.relationship('App', backref='registrant', lazy='dynamic')
    app_modifier = db.relationship('App', backref='modifier', lazy='dynamic')
    tageimage_registrant = db.relationship('HoloageImage', backref='registrant', lazy='dynamic')
    tageimage_modifier = db.relationship('HoloageImage', backref='modifier', lazy='dynamic')
    holotage_registrant = db.relationship('ProductManagement', backref='registrant', lazy='dynamic')
    holotage_modifier = db.relationship('ProductManagement', backref='modifier', lazy='dynamic')
    tagevesion_registrant = db.relationship('TagtypeManagement', backref='registrant', lazy='dynamic')
    tagevesion_modifier = db.relationship('TagtypeManagement', backref='modifier', lazy='dynamic')
    report_answerer = db.relationship('Report', backref='answerer', lazy='dynamic')
    banner_registrant = db.relationship('Banner', backref='registrant', lazy='dynamic')
    banner_modifier = db.relationship('Banner', backref='modifier', lazy='dynamic')


class Loginlog(db.Model):
    __tablename__ = 'tl_login'
    idx = db.Column(BIGINT(20), primary_key=True, nullable=False, autoincrement=True)
    id = db.Column(VARCHAR(20), nullable=False)
    resultCode = db.Column(CHAR(4), nullable=False)
    dtAttempted = db.Column(DATETIME, nullable=False)
    remoteAddr = db.Column(VARCHAR(23), nullable=False)



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



class Blacklist(db.Model):
    __tablename__ = 'td_black_list'
    idx = db.Column(INTEGER(11), nullable=False, autoincrement=True, index=True)
    pushToken = db.Column(VARCHAR(50), primary_key=True, nullable=False)
    blType = db.Column(ENUM('C', 'O'), nullable=False, default='C')
    delYN = db.Column(VARCHAR(1), nullable=False, default='N')
    dtRegistered = db.Column(DATETIME, nullable=False)
    registrant = db.Column(VARCHAR(50), nullable=False, default='CURRENT_TIMESTAMP')
    dtModified = db.Column(DATETIME, nullable=False, default='CURRENT_TIMESTAMP')
    modifier = db.Column(VARCHAR(50), nullable=False)


class CustomerCompany(db.Model):
    __tablename__ = 'td_company'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    code = db.Column(VARCHAR(10), nullable=False, unique=True)
    name_kr = db.Column(VARCHAR(100), nullable=False)
    name_en = db.Column(VARCHAR(100), default='NULL')
    name_zh = db.Column(VARCHAR(100), default='NULL')
    registrationNumber = db.Column(VARCHAR(45), nullable=False)
    businessRegistrationUrl = db.Column(VARCHAR(64), default='NULL')
    addr_kr = db.Column(TEXT, nullable=False)
    addr_en = db.Column(TEXT, default='NULL')
    addr_zh = db.Column(TEXT, default='NULL')
    telephone = db.Column(VARCHAR(20), default='NULL')
    fax=db.Column(VARCHAR(20), default='NULL')
    delegator_kr = db.Column(VARCHAR(40), nullable=False)
    delegator_en = db.Column(VARCHAR(45), default='NULL')
    delegator_zh = db.Column(VARCHAR(45), default='NULL')
    state = db.Column(ENUM('Registered','Deleted','Paused'), nullable=False, default='Registered')
    registrant = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtRegistered = db.Column(DATETIME, nullable=False)
    modifier = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtModified = db.Column(DATETIME, nullable=False)
    note = db.Column(TEXT, default='NULL')
    ci = db.Column(TEXT, nullable=False)
    url = db.Column(TEXT, nullable=False)
    description_kr = db.Column(TEXT, nullable=False)
    description_en = db.Column(TEXT, default='NULL')
    description_zh = db.Column(TEXT, default='NULL')
    tntLogoImgUrl = db.Column(VARCHAR(64), default='NULL')
    customer_companycode = db.relationship('CustomerAccount', backref='companyCode', lazy='dynamic')
    app_companycode = db.relationship('App', backref='companyCode', lazy='dynamic')
    holotage_companycode = db.relationship('ProductManagement', backref='companyCode', lazy='dynamic')
    certification_companycode = db.relationship('ProductCertification', backref='companyCode', lazy='dynamic')
    report_companycode = db.relationship('Report', backref='companyCode', lazy='dynamic')
    appdowndaily_companycode = db.relationship('AppdownDaily', backref='companyCode', lazy='dynamic')
    retailer_companycode = db.relationship('Retailer', backref='companyCode', lazy='dynamic')



class App(db.Model):
    __tablename__ = 'td_app'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    code = db.Column(CHAR(10), default='NULL', index=True)
    name_kr = db.Column(VARCHAR(64), default='NULL')
    name_en = db.Column(VARCHAR(64), default='NULL')
    name_zh = db.Column(VARCHAR(64), default='NULL')
    version = db.Column(CHAR(11), nullable=False)
    type = db.Column(ENUM('LIB', 'APP'), nullable=False)
    tagType = db.Column(ENUM('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG', 'RANDOMTAG', 'SQRTAG'), default='NULL')
    companyCode = db.Column(CHAR(10), db.ForeignKey('td_company.code'), nullable=False, index=True)
    registrant = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtRegistered = db.Column(DATETIME, nullable=False)
    modifier = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtModified = db.Column(DATETIME, nullable=False)
    note = db.Column(TEXT, default='NULL')
    dtPublished = db.Column(DATETIME, default='NULL')
    attachedPath = db.Column(TEXT, default='NULL')
    osType = db.Column(ENUM('iOS', 'Android', 'All'), nullable=False)
    state = db.Column(ENUM('Enable', 'Disable', 'Deleted'), nullable=False, default='Disable')
    description = db.Column(TEXT, default='NULL')
    limitCertHour = db.Column(VARCHAR(50), default='8')
    limitCertCnt = db.Column(VARCHAR(50), nullable=False, default='50')
    updateUrl = db.Column(VARCHAR(128), default='NULL')
    device_appcode = db.relationship('Device', backref='appCode', lazy='dynamic')


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
    dtRegistered = db.Column(DATETIME, nullable=False)
    modifier = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), nullable=False)
    dtModified = db.Column(DATETIME, default='NULL')
    note = db.Column(TEXT)
    tag_version = db.relationship('ProductManagement', backref='hVersion', lazy='dynamic')
    tag_certification = db.relationship('ProductCertification', backref='hVersion', lazy='dynamic')
    tag_report = db.relationship('Report', backref='hVersion', lazy='dynamic')



class Device(db.Model):
    __tablename__ = 'td_device'
    idx = db.Column(BIGINT(20), primary_key=True, nullable=False, autoincrement=True)
    pushToken = db.Column(VARCHAR(50), nullable=False, unique=True)
    model = db.Column(VARCHAR(50), nullable=False, index=True)
    osVersion = db.Column(VARCHAR(20), nullable=False)
    appVersion = db.Column(CHAR(11), nullable=False)
    appCode = db.Column(CHAR(10), db.ForeignKey('td_app.code'), default='NULL', index=True)
    appTagType = db.Column(CHAR(1), nullable=False, default='H')
    agreeTerm = db.Column(TINYINT(1), nullable=False, default=0)
    agreeGPS = db.Column(TINYINT(1), nullable=False, default=0)
    useBackground = db.Column(TINYINT(1), nullable=False, default=1)
    language = db.Column(VARCHAR(4), nullable=False)
    languageCode = db.Column(ENUM('Korean', 'English', 'Chinese'), default='NULL')
    serverName = db.Column(VARCHAR(32), default='NULL')
    state = db.Column(ENUM('Registered', 'Deleted', 'Paused'), nullable=False)
    dtRegistered = db.Column(DATETIME, nullable=False)
    dtLastConnected = db.Column(DATETIME, nullable=False)
    dtTermAgreement = db.Column(DATETIME, default='NULL')
    ipAddr = db.Column(VARCHAR(24), default='NULL')
    serviceTermVersion = db.Column(VARCHAR(20), db.ForeignKey('td_service_term.version'), default='NULL', index=True)
    locationTermVersion = db.Column(VARCHAR(20), db.ForeignKey('td_location_term.version'), default='NULL', index=True)
    report_deviceid = db.relationship('Report', backref='deviceID', lazy='dynamic')





class ProductManagement(db.Model):
    __tablename__ = 'td_holotag'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    code = db.Column(CHAR(10), unique=True, nullable=False)
    name_kr = db.Column(VARCHAR(100), nullable=False)
    name_en = db.Column(VARCHAR(45), default='NULL')
    name_zh = db.Column(VARCHAR(45), default='NULL')
    companyCode = db.Column(CHAR(10), db.ForeignKey('td_company.code'), unique=True, default='NULL', index=True)
    state = db.Column(ENUM('Registered','Deleted','Paused'), nullable=False)
    attachType = db.Column(ENUM('LABELBOX','POUCH','POUCH_PRINT'), default='NULL')
    certOverCnt = db.Column(INTEGER(11), default='NULL')
    certOverManyCnt = db.Column(INTEGER(11), default='NULL')
    registrant = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtRegistered = db.Column(DATETIME, nullable=False)
    modifier = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtModified = db.Column(DATETIME, nullable=False)
    sourceImage = db.Column(TEXT, nullable=False)
    note = db.Column(TEXT, default='NULL')
    hVersion = db.Column(CHAR(11), db.ForeignKey('td_tag_version.version'), default='NULL', index=True)
    mappingCode = db.Column(VARCHAR(10), default='NULL', index=True)
    sqrUrl = db.Column(VARCHAR(32), default='NULL')
    sqrVer = db.Column(INTEGER(2), nullable=False, default=0)
    tageimage_tagidx = db.relationship('HolotagImage', backref='tagIdx', lazy='dynamic')


class HoloageImage(db.Model):
    __tablename__ = 'ti_holotag'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(VARCHAR(45), nullable=False)
    tagIdx = db.Column(INTEGER(11), db.ForeignKey('td_holotag.idx'), nullable=False, index=True)
    path = db.Column(TEXT, nullable=False)
    state = db.Column(ENUM('Registered', 'Deleted', 'Paused'), nullable=False)
    registarant = db.Column(VARCHAR(45), db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtRegistered = db.Column(DATETIME, nullable=False)
    modifier = db.Column(VARCHAR(45), db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtModified = db.Column(DATETIME, nullable=False)
    note = db.Column(TEXT, default='NULL')



class CustomerAccount(db.Model):
    __tablename__ = 'td_account'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    id = db.Column(VARCHAR(20), primary_key=True, nullable=False, unique=True)
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




class ProductCertification(db.Model):
    __tablename__ = 'th_certification'
    idx = db.Column(BIGINT(20), primary_key=True, nullable=False, autoincrement=True)
    deviceID = db.Column(VARCHAR(50), nullable=False)
    companyCode = db.Column(CHAR(10), db.ForeignKey('td_company.code'), default='NULL')
    tagType = db.Column(ENUM('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG', 'RANDOMTAG', 'SQRTAG'), default='NULL')
    tagCode = db.Column(CHAR(10), default='NULL')
    hVersion = db.Column(CHAR(11), db.ForeignKey('td_tag_version.version'), default='NULL')
    mappingCode = db.Column(VARCHAR(10), default='NULL')
    image = db.Column(VARCHAR(128), default='NULL')
    result = db.Column(ENUM('Geunine', 'Counterfeit', 'Revalidation', 'Exprired', 'Invalid', 'Retry', 'OverCert', 'DifferentQR', 'CommonQR', 'NotiOverCert'), nullable=False)
    resultDetail = db.Column(INTEGER(4), default=0)
    osType = db.Column(ENUM('iOS', 'Android', 'Unknown', 'Web'), nullable=False)
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
    companyCode = db.Column(CHAR(10), db.ForeignKey('td_company.code'), default='NULL', index=True)
    tagCode = db.Column(CHAR(10), default='NULL', index=True)
    hVersion = db.Column(CHAR(11), db.ForeignKey('td_tag_version.version'), default='NULL', index=True)
    image = db.Column(TEXT, nullable=False)
    imageProduct = db.Column(TEXT, default='NULL')
    latitude = db.Column(VARCHAR(45), default='NULL')
    longitude = db.Column(VARCHAR(45), default='NULL')
    address = db.Column(VARCHAR(256), default='NULL')
    dtCreated = db.Column(DATETIME, nullable=False, index=True)
    email = db.Column(VARCHAR(100), default='NULL')
    content = db.Column(TEXT, default='NULL')
    category = db.Column(INTEGER(11), default='NULL')
    contact = db.Column(VARCHAR(64), default='NULL')
    contactType = db.Column(ENUM('CONTACT_NUM', 'WECHAT', 'LINE', 'KAKAOTALK'), default='NULL')
    purchasePlace = db.Column(VARCHAR(120), default='NULL')
    onlinePurchasePlace = db.Column(VARCHAR(220), default='NULL')
    purchaseDate = db.Column(VARCHAR(8), default='NULL')
    type = db.Column(ENUM('Report', 'Expire', 'Share', 'Invalid'), nullable=False)
    tagType = db.Column(ENUM('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG', 'RANDOMTAG', 'SQRTAG'), default='NULL')
    mappingCode = db.Column(VARCHAR(10), default='NULL')
    random = db.Column(VARCHAR(16), default='NULL')
    retailerID = db.Column(VARCHAR(10), default='NULL')
    state = db.Column(ENUM('Question', 'Answer', 'Holding'), nullable=False, default='Question')
    answerer = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), default='NULL', index=True)
    dtAnswer = db.Column(DATETIME, default='NULL')
    aContent = db.Column(TEXT, default='NULL')
    osType = db.Column(ENUM('iOS', 'Android', 'Unknown'), nullable=False)
    memo = db.Column(TEXT, default='NULL')
    certificationIdx = db.Column(BIGINT(20), default=-1)
    importantYN = db.Column(ENUM('Y', 'N'), nullable=False, default='N')
    codeState = db.Column(VARCHAR(6), default='NULL')
    codeChannel = db.Column(VARCHAR(6), default='NULL')
    resultDetail = db.Column(INTEGER(4), nullable=False, default=0)
    data = db.Column(VARCHAR(64), default='NULL')



class AppdownDaily(db.Model):
    __tablename__ = 'ts_appdown_daily'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    date = db.Column(CHAR(8), nullable=False)
    companyCode = db.Column(VARCHAR(10), db.ForeignKey('td_company.code'), default='NULL', index=True)
    osType = db.Column(ENUM('iOS', 'Android', 'Unknown'), nullable=False)
    tagType = db.Column(ENUM('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG'), default='NULL')
    downloadCount = db.Column(INTEGER(11), nullable=False, default=0)



class Retailer(db.Model):
    __tablename__ = 'td_retailer'
    idx = db.Column(INTEGER(11), primary_key=True, nullable=False, autoincrement=True)
    rtid = db.Column(CHAR(10), nullable=False, index=True)
    name_kr = db.Column(VARCHAR(100), nullable=False)
    name_en = db.Column(VARCHAR(45), default='NULL')
    name_zh = db.Column(VARCHAR(45), default='NULL')
    companyCode = db.Column(CHAR(10), db.ForeignKey('td_company.code'), default='NULL', index=True)
    state = db.Column(ENUM('Registered', 'Deleted', 'Paused'), default='Registered')
    note = db.Column(VARCHAR(512), default='NULL')
    headerquarterYN = db.Column(ENUM('Y', 'N'), nullable=False, default='N')
    registrant = db.Column(VARCHAR(20), nullable=False)
    dtRegistered = db.Column(DATETIME, nullable=False, default='CURRENT_TIMESTAMP')
    modifier = db.Column(VARCHAR(20), default='NULL')
    dtModified = db.Column(DATETIME, default='NULL')


class Banner(db.Model):
    __tablename__ = 'td_banner'
    idx = db.Column(INTEGER(10), primary_key=True, nullable=False, autoincrement=True)
    bannerID = db.Column(CHAR(10), nullable=False)
    bannerName = db.Column(VARCHAR(128), nullable=False)
    sizeType = db.Column(ENUM('DEFAULT', 'WXGA'), nullable=False)
    imageUrl = db.Column(VARCHAR(256), nullable=False)
    linkUrl = db.Column(VARCHAR(512), nullable=False)
    interval = db.Column(INTEGER(6), nullable=False)
    dtStart = db.Column(DATETIME, nullable=False)
    dtEnd = db.Column(DATETIME, nullable=False)
    registrant = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), nullable=False)
    dtRegistered = db.Column(DATETIME, nullable=False)
    modifier = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), nullable=False)
    dtModified  = db.Column(DATETIME, nullable=False)
