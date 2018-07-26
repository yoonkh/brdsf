from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from .exceptions import ValidationError
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'tc_role'
    idx = db.Column(db.String(32), primary_key=True)
    code = db.Column(db.Integer)
    name_kr = db.Column(db.String(64), unique=True)
    name_en = db.Column(db.String(64))
    name_zh = db.Column(db.String(64))
    name_kr_forAccount = db.Column(db.String(64))
    name_en_forAccount = db.Column(db.String(64))
    name_zh_forAccount = db.Column(db.String(64))
    state = db.Column(db.string(64))
    description = db.Column(db.String(128))
    dtRegistered = db.Column(db.String(64))
    dtModified = db.Column(db.String(64))
    isIcraft = db.Column(db.Integer)

class Result(db.Model):
    __tablename__ = 'tc_result'
    idx = db.Column(db.String(32), primary_key=True)
    code = db.Column(db.String(32))
    msg_kr = db.Column(db.String(64), unique=True)
    msg_en = db.Column(db.String(64))
    msg_zh= db.Column(db.String(64))
    msg = db.Column(db.String(128))


class ICraftaccount(db.Model):
    __tablename__ = 'td_admin'
    idx = db.Column(db.String(64), primary_key=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False, unique=True)
    name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.string(64))
    telephone = db.Column(db.string(64))
    role = db.Column(db.Integer, db.ForeignKey('tc_role.code'))
    position = db.Column(db.String(64))
    department = db.Column(db.String(64))
    state = db.Column(db.String(64))
    #자기 참조....
    registrant = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtRegistered = db.Column(db.string(64))
    modifier = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtModified = db.Column(db.string(64))
    #.........
    note = db.Column(db.String(128))
    failCount = db.Column(db.Integer)

class Holotageimage(db.Model):
    __tablename__ = 'ti_holotag'
    idx = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    tagIdx = db.Column(db.Integer)
    path = db.Column(db.String(128))
    state = db.Column(db.string(64))
    registarant = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtRegistered = db.Column(db.string(64))
    modigier = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtModified = db.Column(db.string(64))
    note = db.Column(db.String(128))


class Customercompany(db.Model):
    __tablename__ = 'td_company'
    idx = db.Column(db.String(32), primary_key=True)
    code = db.Column(db.String(64), unique=True)
    name_kr = db.Column(db.String(64), unique=True)
    name_en = db.Column(db.String(64))
    name_zh = db.Column(db.String(64))
    registrationNumber = db.Column(db.String(64))
    businessRegistrationUrl = db.Column(db.String(64))
    addr_kr = db.Column(db.String(64))
    addr_en = db.Column(db.String(64))
    addr_zh = db.Column(db.String(64))
    telephone = db.Column(db.string(64))
    fax=db.Column(db.string(64))
    delegator_kr = db.Column(db.string(64))
    delegator_en = db.Column(db.string(64))
    delegator_zh = db.Column(db.string(64))
    permissions = db.Column(db.Integer)
    state = db.Column(db.string(64))
    registrant = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtRegistered = db.Column(db.string(64))
    modigier = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtModified = db.Column(db.string(64))
    note = db.Column(db.Integer, default=None)
    ci = db.Column(db.String(128))
    url = db.Column(db.String(128))
    description_kr = db.Column(db.String(128))
    description_en = db.Column(db.String(128))
    description_zh = db.Column(db.String(128))
    tntLogoImgUrl = db.Column(db.String(128))



class Customeraccount(db.Model):
    __tablename__ = 'td_account'
    idx = db.Column(db.String(64), primary_key=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), nullable=False, unique=True)
    name_kr = db.Column(db.String(64), nullable=False)
    name_en = db.Column(db.String(64))
    name_zh = db.Column(db.String(64))
    phone = db.Column(db.string(64))
    telephone = db.Column(db.string(64))
    fax = db.Column(db.string(64))
    companyCode = db.Column(db.String(64), db.ForeignKey('td_company.code'))
    role = db.Column(db.Integer, db.ForeignKey('tc_role.code'))
    position = db.Column(db.String(64))
    department = db.Column(db.String(64))
    state = db.Column(db.String(64))
    registrant = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtRegistered = db.Column(db.string(64))
    modifier = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtModified = db.Column(db.string(64))
    note = db.Column(db.String(128))
    failCount = db.Column(db.Integer)



class ProductManagement(db.Model):
    __tablename__ = 'td_holotage'
    idx = db.Column(db.String(32), primary_key=True)
    code = db.Column(db.String(64), nuique=True)
    name_kr = db.Column(db.String(64), nullable=False)
    name_en = db.Column(db.String(64))
    name_zh = db.Column(db.String(64))
    companyCode = db.Column(db.Integer, db.ForeignKey('td_company.code'))
    state = db.Column(db.String(64))
    registrant = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtRegistered = db.Column(db.string(64))
    modifier = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtModified = db.Column(db.string(64), db.ForeignKey('ti_holotag.path'))
    sourceImage = db.Column(db.string(128))
    note = db.Column(db.String(128))
    hVersion = db.Column(db.Integer, db.ForeignKey('td_tag_version.id'))
    mappingCode = db.Column(db.String(64))
    sqrUrl = db.Column(db.String(128))
    sqrVer = db.Column(db.Integer)


class TagtypeManagement(db.Model):
    __tablename__ = 'td_tag_version'
    idx = db.Column(db.String(32), primary_key=True)
    version = db.Column(db.String(64), nullable=False, unique=True)
    type = db.Column(db.String(64), nullable=False)
    name_kr = db.Column(db.String(64), nullable=False)
    name_en = db.Column(db.String(64))
    name_zh = db.Column(db.String(64))
    state = db.Column(db.String(64))
    width = db.Column(db.Integer, nullable=False)
    height =db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(128))
    registrant = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtRegistered = db.Column(db.string(64))
    modifier = db.Column(db.string(64), db.ForeignKey('td_admin.id'))
    dtModified = db.Column(db.string(64))
    sourceImage = db.Column(db.string(128))
    note = db.Column(db.String(128))


class ProductCertification(db.Model):
    __tablename__ = 'th_certification'
    idx = db.Column(db.String(32), primary_key=True)
    deviceID = db.Column(db.String(64), db.ForeignKey('td_company.code'))
    companyCode = db.Column(db.String(64), db.ForeignKey('td_company.code'))
    tagType = db.Column(db.String(64), db.ForeignKey('td_tag_vesion.type'))
    tagCode = db.Column(db.String(64), db.ForeignKey('td_holotag.code'))
    hVersion = db.Column(db.String(64), db.ForeignKey('td_tag_vesion.version'))
    mappingCode = db.Column(db.String(64), defalut=None)
    image = db.Colmn(db.Sring(128))
    result = db.Colmn(db.Sring(64))
    resultDetail = db.Colmn(db.Sring(128))
    osType = db.Colmn(db.Sring(64))
    dtCertificate = db.Column(db.string(64))
    longitude = db.Column(db.string(64))
    latitude = db.Column(db.string(64))
    regionIdx = db.Column(db.Integer)
    random = db.Column(db.Integer)
    randomCnt = db.Column(db.Integer)
    retailerID = db.Column(db.Integer)
    mode = db.Column(db.Integer)
    data = db.Column(db.Integer)

class Report(db.Model):
    __tablename__ = 'th_cerification'
    idx = db.Column(db.String(32), primary_key=True)
    deviceID =
    companyCode
    tagCode
    hVersion
    image
    imageProduct
    latitude
    longitude
    address
    dtCreated
    email
    content
    category
    contact
    contactType
    purchasePlace
    onlinePurchasePlace
    purchaseDate
    type
    tagType
    mappingCode
    random
    retailerID
    state
    answerer
    dtAnswer
    aContent
    osType
    memo
    certificationIdx
    importantYN
    codeState
    codeChannel
    resultDetail
    data
