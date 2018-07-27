from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from .exceptions import ValidationError
from . import db

class Customercompany(db.Model):
    __tablename__ = 'td_company'
    idx = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True)
    name_kr = db.Column(db.String(128))
    name_en = db.Column(db.String(128), nullable=True)
    name_zh = db.Column(db.String(128), nullable=True)
    registrationNumber = db.Column(db.String(64))
    businessRegistrationUrl = db.Column(db.String(64), nullable=True)
    addr_kr = db.Column(db.String(64))
    addr_en = db.Column(db.String(64), nullable=True)
    addr_zh = db.Column(db.String(64), nullable=True)
    telephone = db.Column(db.String(64), nullable=True)
    fax=db.Column(db.String(64), nullable=True)
    delegator_kr = db.Column(db.String(64))
    delegator_en = db.Column(db.String(64), nullable=True)
    delegator_zh = db.Column(db.String(64), nullable=True)
    permissions = db.Column(db.Integer, default='Registerd')
    state = db.Column(db.String(64))
    dtRegistered = db.Column(db.String(64))
    dtModified = db.Column(db.String(64))
    note = db.Column(db.Integer, nullable=True)
    ci = db.Column(db.String(128))
    url = db.Column(db.String(128))
    description_kr = db.Column(db.String(128), nullable=True)
    description_en = db.Column(db.String(128), nullable=True)
    description_zh = db.Column(db.String(128), nullable=True)
    tntLogoImgUrl = db.Column(db.String(128))
    registrant = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    modigier = db.Column(db.string(64), db.ForeignKey('td_admin.id'))


class Role(db.Model):
    __tablename__ = 'tc_role'
    idx = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    name_kr = db.Column(db.String(64), unique=True)
    name_en = db.Column(db.String(64), nullable=True)
    name_zh = db.Column(db.String(64), nullable=True)
    name_kr_forAccount = db.Column(db.String(64), nullable=True)
    name_en_forAccount = db.Column(db.String(64), nullable=True)
    name_zh_forAccount = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(64))
    description = db.Column(db.String(128), nullable=True)
    dtRegistered = db.Column(db.String(64))
    dtModified = db.Column(db.String(64))
    isIcraft = db.Column(db.Integer)
#
#
#
# class LoginResult(db.Model):
#     __tablename__ = 'tc_result'
#     idx = db.Column(db.Integer, primary_key=True)
#     code = db.Column(db.String(32), unique=True)
#     msg_kr = db.Column(db.String(128))
#     msg_en = db.Column(db.String(128), nullable=True)
#     msg_zh= db.Column(db.String(128), nullable=True)
#     msg = db.Column(db.String(128))
#
#
#
# class App(db.Model):
#     __tablename__ = 'td_app'
#     idx = db.Column(db.Integer, primary_key=True)
#     code = db.Column(db.String(64), nullable=True)
#     name_kr = db.Column(db.String(64), nullable=True)
#     name_en = db.Column(db.String(64), nullable=True)
#     name_zh = db.Column(db.String(64), nullable=True)
#     version = db.Column(db.String(64))
#     type = db.Column(db.String(64))
#     tagType = db.Column(db.String(64))
#     companyCode = db.Column(db.String(64), db.ForeignKey('td_company.code'))
#     registrant = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
#     dtRegistered = db.Column(db.string(64))
#     modifier = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
#     dtModified = db.Column(db.string(64))
#     note = db.Column(db.String(128), nullable=True)
#     dtPublished = db.Column(db.string(64), nullable=True)
#     attachedPath = db.Column(db.String(128), nullable=True)
#     osType = db.Column(db.String(32))
#     state = db.Column(db.String(32), default='Disable')
#     description = db.Column(db.String(128), nullable=True)
#     limitCertHour = db.Column(db.String(64), default='8')
#     limitCertCnt = db.Column(db.String(64), default='50')
#     updateUrl = db.Column(db.String(128), nullable=True)
#
#
#
# class Serviceterm(db.Model):
#     __tablename__ = 'td_service_term'
#     idx = db.Column(db.Integer, primary_key=True)
#     appTagType = db.Column(db.String(32), default='H')
#     version = db.Column(db.String(64), unique=True)
#     title = db.Column(db.String(128))
#     termUrl = db.Column(db.String(64))
#     state = db.Column(db.String(32))
#     dtRegistered = db.Column(db.string(64), nullable=True)
#     dtPublished = db.Column(db.string(64), nullable=True)
#     dtDeleted = db.Column(db.string(64))
#
# class Locationterm(db.Model):
#     __tablename__ = 'td_location_term'
#     idx = db.Column(db.Integer, primary_key=True)
#     version = db.Column(db.String(64), unique=True)
#     title = db.Column(db.String(128))
#     termUrl = db.Column(db.String(64))
#     state = db.Column(db.String(32))
#     dtRegistered = db.Column(db.string(64), nullable=True)
#     dtPublished = db.Column(db.string(64), nullable=True)
#     dtDeleted = db.Column(db.string(64))
#
# class DeviceModel(db.Model):
#     __tablename__ = 'td_model'
#     idx = db.Column(db.Integer, primary_key=True)
#     name= db.Column(db.String(64), unique=True)
#     osType = db.Column(db.String(64))
#     resolution = db.Column(db.String(128), nullable=True)
#     dtRegistered = db.Column(db.String(64))
#     dtModified = db.Column(db.String(64))
#
#
# class Device(db.Model):
#     __tablename__ = 'td_device'
#     idx = db.Column(db.Integer, primary_key=True)
#     pushToken = db.Column(db.String(64))
#     model = db.Column(db.String(64))
#     osVersion = db.Column(db.String(64))
#     appVersion = db.Column(db.String(64))
#     appCode = db.Column(db.String(64), db.Foreingnkey('td_app.code'), nullable=True)
#     appTagType = db.Column(db.String(32), default='H')
#     agreeTerm = db.Column(db.Integer, default=0)
#     agreeGPS = db.Column(db.Integer, default=0)
#     useBackground = db.Column(db.Integer, default=1)
#     language = db.Column(db.String(32))
#     languageCode = db.Column(db.String(32), nullable=True)
#     serverName = db.Column(db.String(32), nullable=True)
#     state = db.Column(db.String(32))
#     dtRegistered = db.Column(db.string(64))
#     dtLastConnected = db.Column(db.string(64))
#     dtTermAgreement = db.Column(db.string(64), nullable=True)
#     serviceTermVersion = db.Column(db.String(32), db.Freingkey('td_servive_term.version'), nullable=True)
#     locationTermVersion = db.Column(db.String(32), db.Freingkey('td_location_term.version'), nullable=True)
#     ipAddr = db.Column(db.String(32), nullable=True)
#
#
#
class ICraftaccount(db.Model):
    __tablename__ = 'td_admin'
    idx = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(64))
    email = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.string(64))
    telephone = db.Column(db.string(64))
    role = db.Column(db.Integer, db.ForeignKey('tc_role.code'))
    position = db.Column(db.String(64), nullable=True)
    department = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(64))
    #자기 참조....
    registrant = db.Column(db.string(64), nullable=True)
    dtRegistered = db.Column(db.string(64))
    modifier = db.Column(db.string(64), nullable=True)
    dtModified = db.Column(db.string(64))
    #.........
    dtLastConnected = db.Column(db.String(64), nullable=True)
    note = db.Column(db.String(128), nullable=True)
    failCount = db.Column(db.Integer, default=0)
#
#
#
# class Holotageimage(db.Model):
#     __tablename__ = 'ti_holotag'
#     idx = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     tagIdx = db.Column(db.Integer, db.ForeignKey('td_holotag.idx'))
#     path = db.Column(db.String(128))
#     state = db.Column(db.string(64))
#     registarant = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
#     dtRegistered = db.Column(db.string(64))
#     modigier = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
#     dtModified = db.Column(db.string(64))
#     note = db.Column(db.String(128),nullable=True)
#
#
#
#

#
#
#
#
#
class Customeraccount(db.Model):
    __tablename__ = 'td_account'
    idx = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64))
    name_kr = db.Column(db.String(64))
    name_en = db.Column(db.String(64), nullable=True)
    name_zh = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.string(64))
    telephone = db.Column(db.string(64))
    fax = db.Column(db.string(64), nullable=True)
    companyCode = db.Column(db.String(64), db.ForeignKey('td_company.code'))
    role = db.Column(db.Integer, db.ForeignKey('tc_role.code'))
    position = db.Column(db.String(64), nullable=True)
    department = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(64))
    registrant = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtRegistered = db.Column(db.string(64))
    modifier = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtModified = db.Column(db.string(64))
    dtLastConnected = db.Column(db.String(64), nullable=True)
    note = db.Column(db.String(128), nullable=True)
    failCount = db.Column(db.Integer, default=0)
#
#
#
#
#
# class ProductManagement(db.Model):
#     __tablename__ = 'td_holotage'
#     idx = db.Column(db.Integer, primary_key=True)
#     code = db.Column(db.String(64), nuique=True)
#     name_kr = db.Column(db.String(64))
#     name_en = db.Column(db.String(64), nullable=True)
#     name_zh = db.Column(db.String(64), nullable=True)
#     companyCode = db.Column(db.Integer, db.ForeignKey('td_company.code'), nullable=True)
#     state = db.Column(db.String(64))
#     attachType = db.Column(db.String(32))
#     certOverCnt = db.Column(db.Integer)
#     certOverManyCnt = db.Column(db.Integer)
#     registrant = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
#     dtRegistered = db.Column(db.string(64))
#     modifier = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
#     dtModified = db.Column(db.string(64))
#     sourceImage = db.Column(db.string(128))
#     note = db.Column(db.String(128), nullable=True)
#     mappingCode = db.Column(db.String(64), nullable=True)
#     sqrUrl = db.Column(db.String(128), nullable=True)
#     hVersion = db.Column(db.String(64), db.ForeignKey('td_tag_version.id'))
#     sqrVer = db.Column(db.Integer)
#
#
#
#
# class TagtypeManagement(db.Model):
#     __tablename__ = 'td_tag_version'
#     idx = db.Column(db.Integer, primary_key=True)
#     version = db.Column(db.String(64), unique=True)
#     type = db.Column(db.String(64))
#     name_kr = db.Column(db.String(64))
#     name_en = db.Column(db.String(64))
#     name_zh = db.Column(db.String(64))
#     state = db.Column(db.String(64), default='Disable')
#     width = db.Column(db.Integer)
#     height =db.Column(db.Integer)
#     description = db.Column(db.String(128))
#     registrant = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
#     dtRegistered = db.Column(db.string(64))
#     modifier = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
#     dtModified = db.Column(db.string(64))
#     sourceImage = db.Column(db.string(128))
#     note = db.Column(db.String(128), nullable=True)
#
#
#
#
# class ProductCertification(db.Model):
#     __tablename__ = 'th_certification'
#     idx = db.Column(db.Integer, primary_key=True)
#     deviceID = db.Column(db.String(128))
#     companyCode = db.Column(db.String(64), db.ForeignKey('td_company.code'), nullable=True)
#     tagType = db.Column(db.String(64), nullable=True)
#     tagCode = db.Column(db.String(64), nullable=True)
#     hVersion = db.Column(db.String(64), db.ForeignKey('td_tag_vesion.version'), nullable=True)
#     mappingCode = db.Column(db.String(64), nullable=True)
#     image = db.Colmn(db.String(128), nullable=True)
#     result = db.Colmn(db.String(64))
#     resultDetail = db.Colmn(db.Integer, default=0)
#     osType = db.Colmn(db.String(64))
#     dtCertificate = db.Column(db.string(64))
#     longitude = db.Column(db.string(64), nullable=True)
#     latitude = db.Column(db.string(64), nullable=True)
#     regionIdx = db.Column(db.Integer, default=-1)
#     random = db.Column(db.string(64), nullable=True)
#     randomCnt = db.Column(db.Integer, default=0)
#     retailerID = db.Column(db.string(64), nullable=True)
#     mode = db.Column(db.string(64), nullable=True)
#     data = db.Column(db.string(64), nullable=True)
#
#
#
# class Report(db.Model):
#     __tablename__ = 'th_report'
#     idx = db.Column(db.Integer, primary_key=True)
#     deviceID = db.Column(db.String(128), db.ForeignKey('td_device.pushToken'))
#     companyCode = db.Column(db.String(64), db.ForeignKey('td_company.code'), nullable=True)
#     tagCode = db.Column(db.String(64), nullable=True)
#     hVersion = db.Column(db.String(64), db.ForeignKey('td_tag_vesion.version'), nullable=True)
#     image = db.Colmn(db.String(128))
#     imageProduct = db.Colmn(db.String(128), nullable=True)
#     latitude = db.Colmn(db.String(128), nullable=True)
#     longitude = db.Colmn(db.String(128), nullable=True)
#     address = db.Colmn(db.String(128), nullable=True)
#     dtCreated = db.Colmn(db.String(64))
#     email = db.Colmn(db.String(128), nullable=True)
#     content = db.Colmn(db.String(128), nullable=True)
#     category = db.Colmn(db.Integer, nullable=True)
#     contact = db.Colmn(db.String(128), nullable=True)
#     contactType = db.Colmn(db.String(128), nullable=True)
#     purchasePlace = db.Colmn(db.String(128), nullable=True)
#     onlinePurchasePlace = db.Colmn(db.String(128), nullable=True)
#     purchaseDate = db.Colmn(db.String(64), nullable=True)
#     type = db.Colmn(db.String(128))
#     tagType = db.Column(db.String(64), nullable=True)
#     mappingCode = db.Column(db.String(64), nullable=True)
#     random = db.Colmn(db.String(64), nullable=True)
#     retailerID = db.Colmn(db.String(64), nullable=True)
#     state = db.Colmn(db.String(64), default='Question')
#     answerer = db.Column(db.string(64), db.ForeignKey('td_admin.id'), nullable=True)
#     dtAnswer = db.Column(db.string(64), nullable=True)
#     aContent = db.Column(db.string(128), nullable=True)
#     osType = db.Colmn(db.String(64))
#     memo = db.Colmn(db.String(128), nullable=True)
#     certificationIdx = db.Column(db.Integer, default=-1)
#     importantYN = db.Colmn(db.String(32), default='N')
#     codeState = db.Colmn(db.String(32), nullable=True)
#     codeChannel = db.Colmn(db.String(32), nullable=True)
#     resultDetail = db.Column(db.Integer, default=0)
#     data = db.Colmn(db.String(32), nullable=True)
#
# class Loginlog(db.Model):
#     __tablename__ = 'tl_login'
#     idx = db.Column(db.Integer, primary_key=True)
#     id = db.Column(db.String(64))
#     resultCode = db.Column(db.String(64))
#     dtAttempted = db.Column(db.String(64))
#     remoteAddr = db.Column(db.String(64))
#
# class Blacklist(db.Model):
#     __tablename__ = 'td_black_list'
#     idx= db.Column(db.Integer, primary_key=True)
#     pushToken  = db.Colmn(db.String(128))
#     blType
#     delYN
#     dtRegistered
#     registrant
#     dtModified
#     modifier
