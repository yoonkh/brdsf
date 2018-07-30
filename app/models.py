from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from .exceptions import ValidationError
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR, ENUM, INTEGER, TEXT, DATETIME, CHAR, SMALLINT
from . import db

class CustomerCompany(db.Model):
    __tablename__ = 'td_company'
    idx = db.Column(INTEGER(11), primary_key=True)
    code = db.Column(VARCHAR(10), unique=True)
    name_kr = db.Column(VARCHAR(100))
    name_en = db.Column(VARCHAR(100), default='NULL')
    name_zh = db.Column(VARCHAR(100), default='NULL')
    registrationNumber = db.Column(VARCHAR(45))
    businessRegistrationUrl = db.Column(VARCHAR(64), default='NULL')
    addr_kr = db.Column(TEXT)
    addr_en = db.Column(TEXT, default='NULL')
    addr_zh = db.Column(TEXT, default='NULL')
    telephone = db.Column(VARCHAR(20), default='NULL')
    fax=db.Column(VARCHAR(20), default='NULL')
    delegator_kr = db.Column(VARCHAR(40))
    delegator_en = db.Column(VARCHAR(45), default='NULL')
    delegator_zh = db.Column(VARCHAR(45), default='NULL')
    state = db.Column(ENUM('Registered','Deleted','Paused'))
    registrant = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), index=True)
    dtRegistered = db.Column(DATETIME)
    modifier = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), index=True)
    dtModified = db.Column(DATETIME)
    note = db.Column(TEXT, default='NULL')
    ci = db.Column(TEXT)
    url = db.Column(TEXT)
    description_kr = db.Column(TEXT, default='NULL')
    description_en = db.Column(TEXT, default='NULL')
    description_zh = db.Column(TEXT, default='NULL')
    tntLogoImgUrl = db.Column(VARCHAR(64))
    customer_companycode = db.relationship("CustomerAccount", backref='companyCode', lazy='dynamic')


class Role(db.Model):
    __tablename__ = 'tc_role'
    idx = db.Column(INTEGER(11), primary_key=True)
    code = db.Column(TINYINT(4), unique=True, default='NULL')
    name_kr = db.Column(VARCHAR(45), default='NULL')
    name_en = db.Column(VARCHAR(45), default='NULL')
    name_zh = db.Column(VARCHAR(45), default='NULL')
    name_kr_forAccount = db.Column(VARCHAR(45), default='NULL')
    name_en_forAccount = db.Column(VARCHAR(45), default='NULL')
    name_zh_forAccount = db.Column(VARCHAR(45), default='NULL')
    state = db.Column(ENUM('Registered','Deleted','Paused'), default='NULL')
    description = db.Column(TEXT, default='NULL')
    dtRegistered = db.Column(DATETIME, default='NULL')
    dtModified = db.Column(DATETIME, default='NULL')
    isIcraft = db.Column(TINYINT(1), default=0)
    icraft_role = db.relationship("ICraftAccount", backref='role', lazy='dynamic')
    customer_role = db.relationship("CustomerAccount", backref='role', lazy='dynamic')


class ICraftAccount(db.Model):
    __tablename__ = 'td_admin'
    idx = db.Column(INTEGER(11), primary_key=True)
    id = db.Column(VARCHAR(20), unique=True)
    pwd = db.Column(VARCHAR(45))
    email = db.Column(VARCHAR(100), nullable=False)
    name = db.Column(VARCHAR(40), nullable=False)
    phone = db.Column(VARCHAR(20))
    telephone = db.Column(VARCHAR(20))
    role = db.Column(TINYINT(4), db.ForeignKey('tc_role.code'), index=True)
    position = db.Column(VARCHAR(20), default='NULL')
    department = db.Column(VARCHAR(45), default='NULL')
    state = db.Column(ENUM('Registered','Deleted','Paused'))
    registrant = db.Column(VARCHAR(20), default='NULL')
    dtRegistered = db.Column(DATETIME)
    modifier = db.Column(VARCHAR(20), default='NULL')
    dtModified = db.Column(DATETIME)
    dtLastConnected = db.Column(DATETIME, default='NULL')
    note = db.Column(TEXT, default='NULL')
    failCount = db.Column(SMALLINT(6), default=0)
    company_registrant = db.relationship("CustomerCompany", backref='registrant', lazy='dynamic')
    company_modifier = db.relationship("CustomerCompany", backref='modifier', lazy='dynamic')


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
# #
# class ProductManagement(db.Model):
#     __tablename__ = 'td_holotage'
#     idx = db.Column(db.Integer, primary_key=True)
#     code = db.Column(VARCHAR(20), nuique=True)
#     name_kr = db.Column(VARCHAR(20))
#     name_en = db.Column(VARCHAR(20), default='NULL')
#     name_zh = db.Column(VARCHAR(20), default='NULL')
#     companyCode = db.Column(db.Integer, db.ForeignKey('td_company.code'), default='NULL')
#     state = db.Column(VARCHAR(20))
#     attachType = db.Column(VARCHAR(20))
#     certOverCnt = db.Column(db.Integer)
#     certOverManyCnt = db.Column(db.Integer)
#     registrant = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'))
#     dtRegistered = db.Column(VARCHAR(20))
#     modifier = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'))
#     dtModified = db.Column(VARCHAR(20))
#     sourceImage = db.Column(VARCHAR(20))
#     note = db.Column(VARCHAR(20), default='NULL')
#     mappingCode = db.Column(VARCHAR(20), default='NULL')
#     sqrUrl = db.Column(VARCHAR(20), default='NULL')
#     hVersion = db.Column(VARCHAR(20), db.ForeignKey('td_tag_version.id'))
#     sqrVer = db.Column(db.Integer)
#
#
#
#
# class TagtypeManagement(db.Model):
#     __tablename__ = 'td_tag_version'
#     idx = db.Column(db.Integer, primary_key=True)
#     version = db.Column(VARCHAR(20), unique=True)
#     type = db.Column(VARCHAR(20))
#     name_kr = db.Column(VARCHAR(20))
#     name_en = db.Column(VARCHAR(20))
#     name_zh = db.Column(VARCHAR(20))
#     state = db.Column(VARCHAR(20), default='Disable')
#     width = db.Column(db.Integer)
#     height =db.Column(db.Integer)
#     description = db.Column(VARCHAR(20))
#     registrant = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'))
#     dtRegistered = db.Column(VARCHAR(20))
#     modifier = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'))
#     dtModified = db.Column(VARCHAR(20))
#     sourceImage = db.Column(VARCHAR(20))
#     note = db.Column(VARCHAR(20), default='NULL')
#
#
#
#
# class ProductCertification(db.Model):
#     __tablename__ = 'th_certification'
#     idx = db.Column(db.Integer, primary_key=True)
#     deviceID = db.Column(VARCHAR(20))
#     companyCode = db.Column(VARCHAR(20), db.ForeignKey('td_company.code'), default='NULL')
#     tagType = db.Column(VARCHAR(20), default='NULL')
#     tagCode = db.Column(VARCHAR(20), default='NULL')
#     hVersion = db.Column(VARCHAR(20), db.ForeignKey('td_tag_vesion.version'), default='NULL')
#     mappingCode = db.Column(VARCHAR(20), default='NULL')
#     image = db.Colmn(VARCHAR(20), default='NULL')
#     result = db.Colmn(VARCHAR(20))
#     resultDetail = db.Colmn(db.Integer, default=0)
#     osType = db.Colmn(VARCHAR(20))
#     dtCertificate = db.Column(VARCHAR(20))
#     longitude = db.Column(VARCHAR(20), default='NULL')
#     latitude = db.Column(VARCHAR(20), default='NULL')
#     regionIdx = db.Column(db.Integer, default=-1)
#     random = db.Column(VARCHAR(20), default='NULL')
#     randomCnt = db.Column(db.Integer, default=0)
#     retailerID = db.Column(VARCHAR(20), default='NULL')
#     mode = db.Column(VARCHAR(20), default='NULL')
#     data = db.Column(VARCHAR(20), default='NULL')
#
#
#
# class Report(db.Model):
#     __tablename__ = 'th_report'
#     idx = db.Column(db.Integer, primary_key=True)
#     deviceID = db.Column(VARCHAR(20), db.ForeignKey('td_device.pushToken'))
#     companyCode = db.Column(VARCHAR(20), db.ForeignKey('td_company.code'), default='NULL')
#     tagCode = db.Column(VARCHAR(20), default='NULL')
#     hVersion = db.Column(VARCHAR(20), db.ForeignKey('td_tag_vesion.version'), default='NULL')
#     image = db.Colmn(VARCHAR(20))
#     imageProduct = db.Colmn(VARCHAR(20), default='NULL')
#     latitude = db.Colmn(VARCHAR(20), default='NULL')
#     longitude = db.Colmn(VARCHAR(20), default='NULL')
#     address = db.Colmn(VARCHAR(20), default='NULL')
#     dtCreated = db.Colmn(VARCHAR(20))
#     email = db.Colmn(VARCHAR(20), default='NULL')
#     content = db.Colmn(VARCHAR(20), default='NULL')
#     category = db.Colmn(db.Integer, default='NULL')
#     contact = db.Colmn(VARCHAR(20), default='NULL')
#     contactType = db.Colmn(VARCHAR(20), default='NULL')
#     purchasePlace = db.Colmn(VARCHAR(20), default='NULL')
#     onlinePurchasePlace = db.Colmn(VARCHAR(20), default='NULL')
#     purchaseDate = db.Colmn(VARCHAR(20), default='NULL')
#     type = db.Colmn(VARCHAR(20))
#     tagType = db.Column(VARCHAR(20), default='NULL')
#     mappingCode = db.Column(VARCHAR(20), default='NULL')
#     random = db.Colmn(VARCHAR(20), default='NULL')
#     retailerID = db.Colmn(VARCHAR(20), default='NULL')
#     state = db.Colmn(VARCHAR(20), default='Question')
#     answerer = db.Column(VARCHAR(20), db.ForeignKey('td_admin.id'), default='NULL')
#     dtAnswer = db.Column(VARCHAR(20), default='NULL')
#     aContent = db.Column(VARCHAR(20), default='NULL')
#     osType = db.Colmn(VARCHAR(20))
#     memo = db.Colmn(VARCHAR(20), default='NULL')
#     certificationIdx = db.Column(db.Integer, default=-1)
#     importantYN = db.Colmn(VARCHAR(20), default='N')
#     codeState = db.Colmn(VARCHAR(20), default='NULL')
#     codeChannel = db.Colmn(VARCHAR(20), default='NULL')
#     resultDetail = db.Column(db.Integer, default=0)
#     data = db.Colmn(VARCHAR(20), default='NULL')
#
# class Loginlog(db.Model):
#     __tablename__ = 'tl_login'
#     idx = db.Column(db.Integer, primary_key=True)
#     id = db.Column(VARCHAR(20))
#     resultCode = db.Column(VARCHAR(20))
#     dtAttempted = db.Column(VARCHAR(20))
#     remoteAddr = db.Column(VARCHAR(20))
#
# class Blacklist(db.Model):
#     __tablename__ = 'td_black_list'
#     idx= db.Column(db.Integer, primary_key=True)
#     pushToken  = db.Colmn(VARCHAR(20))
#     blType
#     delYN
#     dtRegistered
#     registrant
#     dtModified
#     modifier
