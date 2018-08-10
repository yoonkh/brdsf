# coding: utf-8
from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import BigInteger, Column, DateTime, Enum, ForeignKey, Index, Integer, SmallInteger, String, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class Permission:
    VIEW = 1
    QUESTION = 2
    WRITE = 4
    ALL_MENU = 8
    ICRAFT_SUPER_ADMIN = 16


class TcResult(db.Model):
    __tablename__ = 'tc_result'

    idx = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4), nullable=False, unique=True)
    msg_kr = db.Column(db.String(200), nullable=False)
    msg_en = db.Column(db.String(200))
    msg_zh = db.Column(db.String(200))
    msg = db.Column(db.Text, nullable=False)


class TcRole(db.Model):
    __tablename__ = 'tc_role'

    idx = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, unique=True)
    permissions = db.Column(db.Integer)
    name_kr = db.Column(db.String(45), nullable=False)
    name_en = db.Column(db.String(45))
    name_zh = db.Column(db.String(45))
    name_kr_forAccount = db.Column(db.String(45))
    name_en_forAccount = db.Column(db.String(45))
    name_zh_forAccount = db.Column(db.String(45))
    state = db.Column(Enum('Registered', 'Deleted', 'Paused'), nullable=False)
    description = db.Column(db.Text)
    dtRegistered = db.Column(db.DateTime, nullable=False)
    dtModified = db.Column(db.DateTime, nullable=False)
    isIcraft = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    def __init__(self, **kwargs):
        super(TcRole, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        i = 100
        roles = {
            'CustomerUser': [Permission.VIEW],
            'CustomerAdmin': [Permission.VIEW, Permission.QUESTION],
            'iCraftUser': [Permission.VIEW, Permission.QUESTION,
                           Permission.WRITE],
            'iCraftAdministrator': [Permission.VIEW, Permission.QUESTION,
                                    Permission.WRITE,
                                    Permission.ALL_MENU],
            'iCraftSuperAdmin': [Permission.VIEW, Permission.QUESTION,
                                 Permission.WRITE,
                                 Permission.ALL_MENU, Permission.ICRAFT_SUPER_ADMIN]
        }
        default = 'CustomerUser'
        for r in roles:
            role = TcRole.query.filter_by(name_kr=r).first()
            if role is None:
                role = TcRole(name_kr=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name_kr == default)
            role.state = 'Registered'
            role.dtRegistered = datetime.now()
            role.code = i
            i += 1
            db.session.add(role)
            role.dtModified = datetime.now()
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name_kr


class TdAccount(db.Model, UserMixin):
    __tablename__ = 'td_account'

    idx = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(20), nullable=False, unique=True)
    pwd = db.Column(db.String(128))
    email = db.Column(db.String(100), nullable=False)
    name_kr = db.Column(db.String(40), nullable=False, index=True)
    name_en = db.Column(db.String(40))
    name_zh = db.Column(db.String(40))
    phone = db.Column(db.String(20), nullable=False, index=True)
    telephone = db.Column(db.String(20), nullable=False)
    fax = db.Column(db.String(20))
    companyCode = db.Column(db.ForeignKey('td_company.code'), nullable=False, index=True)
    role = db.Column(db.ForeignKey('tc_role.code'), nullable=False, index=True)
    position = db.Column(db.String(20))
    department = db.Column(db.String(45))
    state = db.Column(Enum('Registered', 'Deleted', 'Paused'))
    registrant = db.Column(db.String(20))
    dtRegistered = db.Column(db.DateTime)
    modifier = db.Column(db.String(20))
    dtModified = db.Column(db.DateTime)
    dtLastConnected = db.Column(db.DateTime)
    note = db.Column(db.Text)
    failCount = db.Column(db.SmallInteger, server_default=db.FetchedValue())

    td_company = db.relationship('TdCompany', primaryjoin='TdAccount.companyCode == TdCompany.code', backref='td_accounts')
    tc_role = db.relationship('TcRole', primaryjoin='TdAccount.role == TcRole.code', backref='td_accounts')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.pwd = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pwd, password)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ICRAFT_SUPER_ADMIN)

    def change_role(self, role_str):
        role = TcRole.query.filter_by(code=role_str).first()
        self.role = role
        db.session.add(self)

    def to_json(self):
        json_user = {
            'idx': self.idx,
            'id': self.id,
            'pwd': self.pwd,
            'email': self.email,
            'name_kr': self.name_kr,
            'name_en': self.name_en,
            'name_zh': self.name_zh,
            'phone': self.phone,
            'telephone': self.telephone,
            'fax': self.fax,
            'companyCode': self.companyCode,
            'role': self.role,
            'role_name': TcRole.query.filter_by(code=self.role).first().name_kr,
            'position': self.position,
            'department': self.department,
            'state': self.state,
            'registrant': self.registrant,
            'dtRegistered': self.dtRegistered,
            'modifier': self.modifier,
            'dtModified': self.dtModified,
            'dtLastConnected': self.dtLastConnected,
            'note': self.note,
            'failCount': self.failCount
        }
        return json_user

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'idx': self.idx}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return TdAccount.query.get(data['idx'])

    def __repr__(self):
        return '<User %r>' % self.email


# class AnonymousUser(AnonymousUserMixin):
#     def can(self, permissions):
#         return False
#
#     def is_administrator(self):
#         return False
#
# login_manager.anonymous_user = AnonymousUser


class TdAdmin(db.Model):
    __tablename__ = 'td_admin'

    idx = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(20), nullable=False, unique=True)
    pwd = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.Integer, nullable=False, index=True)
    position = db.Column(db.String(20))
    department = db.Column(db.String(45))
    state = db.Column(Enum('Registered', 'Deleted', 'Paused'), nullable=False)
    registrant = db.Column(db.String(20))
    dtRegistered = db.Column(db.DateTime, nullable=False)
    modifier = db.Column(db.String(20))
    dtModified = db.Column(db.DateTime, nullable=False)
    dtLastConnected = db.Column(db.DateTime)
    note = db.Column(db.Text)
    failCount = db.Column(db.SmallInteger, server_default=db.FetchedValue())

    def to_json(self):
        json_user = {
            'idx': self.idx,
            'id': self.id,
            'pwd': self.pwd,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'telephone': self.telephone,
            'role': self.role,
            'role_name': TcRole.query.filter_by(code=self.role).first().name_kr,
            'position': self.position,
            'department': self.department,
            'state': self.state,
            'registrant': self.registrant,
            'dtRegistered': self.dtRegistered,
            'modifier': self.modifier,
            'dtModified': self.dtModified,
            'dtLastConnected': self.dtLastConnected,
            'note': self.note,
            'failCount': self.failCount
        }
        return json_user


class TdApp(db.Model):
    __tablename__ = 'td_app'

    idx = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True)
    name_kr = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    name_zh = db.Column(db.String(64))
    version = db.Column(db.String(11), nullable=False)
    type = db.Column(Enum('LIB', 'APP'), nullable=False)
    tagType = db.Column(Enum('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG', 'RANDOMTAG', 'SQRTAG'))
    companyCode = db.Column(db.ForeignKey('td_company.code'), nullable=False, index=True)
    registrant = db.Column(db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtRegistered = db.Column(db.DateTime, nullable=False)
    modifier = db.Column(db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtModified = db.Column(db.DateTime, nullable=False)
    note = db.Column(db.Text)
    dtPublished = db.Column(db.DateTime)
    attachedPath = db.Column(db.Text)
    osType = db.Column(Enum('iOS', 'Android', 'All'), nullable=False)
    state = db.Column(Enum('Enable', 'Disable', 'Deleted'), nullable=False, server_default=db.FetchedValue())
    description = db.Column(db.Text)
    limitCertHour = db.Column(db.String(50), server_default=db.FetchedValue())
    limitCertCnt = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    updateUrl = db.Column(db.String(128))

    td_company = db.relationship('TdCompany', primaryjoin='TdApp.companyCode == TdCompany.code', backref='td_apps')
    td_admin = db.relationship('TdAdmin', primaryjoin='TdApp.modifier == TdAdmin.id', backref='tdadmin_td_apps')
    td_admin1 = db.relationship('TdAdmin', primaryjoin='TdApp.registrant == TdAdmin.id', backref='tdadmin_td_apps_0')


    @staticmethod
    def insert_company():
        sectors = ['아이크래프트', 'CJ', '블랙야크', '시엔스']

        for s in sectors:
            sector = TdApp.query.filter_by(companyCode=s).first()
            if sector is None:
                sector = TdApp(companyCode=s)
                db.session.add(sector)
        db.session.commit()

    @staticmethod
    def insert_tagtype():
        sectors = ['홀로태그', '하이브리드태그', '난수태그', 'SQR태그']

        for s in sectors:
            sector = TdApp.query.filter_by(tagType=s).first()
            if sector is None:
                sector = TdApp(tagType=s)
                db.session.add(sector)
        db.session.commit()

    @staticmethod
    def insert_os():
        sectors = ['iOS', '안드로이드']

        for s in sectors:
            sector = TdApp.query.filter_by(osType=s).first()
            if sector is None:
                sector = TdApp(osType=s)
                db.session.add(sector)
        db.session.commit()

    @staticmethod
    def insert_apptype():
        sectors = ['APP', 'LIB']

        for s in sectors:
            sector = TdApp.query.filter_by(type=s).first()
            if sector is None:
                sector = TdApp(type=s)
                db.session.add(sector)
        db.session.commit()

    def app_code_generator(self):
        pass

    def to_json(self):
        json_app = {
            'idx': self.idx,
            'code': self.code,
            'name_kr': self.name_kr,
            'name_en': self.name_en,
            'name_zh': self.name_zh,
            'version': self.version,
            'type': self.type,
            'tagType': self.tagType,
            'companyCode': self.companyCode,
            'registrant': self.registrant,
            'dtRegistered': self.dtRegistered,
            'modifier': self.modifier,
            'dtModified': self.dtModified,
            'note': self.note,
            'dtPublished': self.dtPublished,
            'attachedPath': self.attachedPath,
            'osType': self.osType,
            'state': self.state,
            'description': self.description,
            'limitCertHour': self.limitCertHour,
            'limitCertCnt': self.limitCertCnt,
            'updateUrl': self.updateUrl
        }
        return json_app


class TdBanner(db.Model):
    __tablename__ = 'td_banner'

    idx = db.Column(db.Integer, primary_key=True)
    bannerID = db.Column(db.String(10), nullable=False, index=True)
    bannerName = db.Column(db.String(128), nullable=False)
    sizeType = db.Column(Enum('DEFAULT', 'WXGA'), nullable=False)
    imageUrl = db.Column(db.String(256), nullable=False)
    linkUrl = db.Column(db.String(512), nullable=False)
    interval = db.Column(db.Integer, nullable=False)
    dtStart = db.Column(db.DateTime, nullable=False)
    dtEnd = db.Column(db.DateTime, nullable=False)
    registrant = db.Column(db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtRegistered = db.Column(db.DateTime, nullable=False)
    modifier = db.Column(db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtModified = db.Column(db.DateTime, nullable=False)

    td_admin = db.relationship('TdAdmin', primaryjoin='TdBanner.modifier == TdAdmin.id', backref='tdadmin_td_banners')
    td_admin1 = db.relationship('TdAdmin', primaryjoin='TdBanner.registrant == TdAdmin.id', backref='tdadmin_td_banners_0')


class TdBlackList(db.Model):
    __tablename__ = 'td_black_list'

    idx = db.Column(db.Integer, nullable=False, index=True)
    pushToken = db.Column(db.String(50), primary_key=True)
    blType = db.Column(Enum('C', 'O'), nullable=False, server_default=db.FetchedValue())
    delYN = db.Column(db.String(1), nullable=False, server_default=db.FetchedValue())
    dtRegistered = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    registrant = db.Column(db.String(50), nullable=False)
    dtModified = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    modifier = db.Column(db.String(50), nullable=False)

    def to_json(self):
        json_black_list = {
            'idx': self.idx,
            'pushToken': self.pushToken,
            'blType': self.blType,
            'delYN': self.delYN,
            'dtRegistered': self.dtRegistered,
            'registrant': self.registrant,
            'dtModified': self.dtModified,
            'modifier': self.modifier
        }
        return json_black_list


class TdCompany(db.Model):
    __tablename__ = 'td_company'

    idx = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False, unique=True)
    name_kr = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100))
    name_zh = db.Column(db.String(100))
    registrationNumber = db.Column(db.String(45), nullable=False)
    businessRegistrationUrl = db.Column(db.String(64))
    addr_kr = db.Column(db.Text, nullable=False)
    addr_en = db.Column(db.Text)
    addr_zh = db.Column(db.Text)
    telephone = db.Column(db.String(20))
    fax = db.Column(db.String(20))
    delegator_kr = db.Column(db.String(40), nullable=False)
    delegator_en = db.Column(db.String(45))
    delegator_zh = db.Column(db.String(45))
    state = db.Column(Enum('Registered', 'Deleted', 'Paused'), nullable=False, server_default=db.FetchedValue())
    registrant = db.Column(db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtRegistered = db.Column(db.DateTime, nullable=False)
    modifier = db.Column(db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtModified = db.Column(db.DateTime, nullable=False)
    note = db.Column(db.Text)
    ci = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    description_kr = db.Column(db.Text, nullable=False)
    description_en = db.Column(db.Text)
    description_zh = db.Column(db.Text)
    tntLogoImgUrl = db.Column(db.String(64))

    td_admin = db.relationship('TdAdmin', primaryjoin='TdCompany.modifier == TdAdmin.id', backref='tdadmin_td_companies')
    td_admin1 = db.relationship('TdAdmin', primaryjoin='TdCompany.registrant == TdAdmin.id', backref='tdadmin_td_companies_0')


    def to_json(self):
        json_company = {
            'idx': self.idx,
            'code': self.code,
            'name_kr': self.name_kr,
            'name_en': self.name_en,
            'name_zh': self.name_zh,
            'registrationNumber': self.registrationNumber,
            'businessRegistrationUrl': self.businessRegistrationUrl,
            'addr_kr': self.addr_kr,
            'addr_en': self.addr_en,
            'addr_zh': self.addr_zh,
            'telephone': self.telephone,
            'fax': self.fax,
            'delegator_kr': self.delegator_kr,
            'delegator_en': self.delegator_en,
            'delegator_zh': self.delegator_zh,
            'state': self.state,
            'registrant': self.registrant,
            'dtRegistered': self.dtRegistered,
            'modifier': self.modifier,
            'dtModified': self.dtModified,
            'note': self.note,
            'ci': self.ci,
            'url': self.url,
            'description_kr': self.description_kr,
            'description_en': self.description_en,
            'description_zh': self.description_zh,
            'tntLogoImgUrl': self.tntLogoImgUrl
        }
        return json_company


class TdDevice(db.Model):
    __tablename__ = 'td_device'

    idx = db.Column(db.BigInteger, primary_key=True)
    pushToken = db.Column(db.String(50), nullable=False, unique=True)
    model = db.Column(db.String(50), nullable=False, index=True)
    osVersion = db.Column(db.String(20), nullable=False)
    appVersion = db.Column(db.String(11), nullable=False)
    appCode = db.Column(db.ForeignKey('td_app.code'), index=True)
    appTagType = db.Column(db.String(1), nullable=False, server_default=db.FetchedValue())
    agreeTerm = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    agreeGPS = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    useBackground = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    language = db.Column(db.String(4), nullable=False)
    languageCode = db.Column(Enum('Korean', 'English', 'Chinese'))
    serverName = db.Column(db.String(32))
    state = db.Column(Enum('Registered', 'Deleted', 'Paused'), nullable=False)
    dtRegistered = db.Column(db.DateTime, nullable=False)
    dtLastConnected = db.Column(db.DateTime, nullable=False)
    dtTermAgreement = db.Column(db.DateTime)
    serviceTermVersion = db.Column(db.ForeignKey('td_service_term.version'), index=True)
    locationTermVersion = db.Column(db.ForeignKey('td_location_term.version'), index=True)
    ipAddr = db.Column(db.String(24))

    td_app = db.relationship('TdApp', primaryjoin='TdDevice.appCode == TdApp.code', backref='td_devices')
    td_location_term = db.relationship('TdLocationTerm', primaryjoin='TdDevice.locationTermVersion == TdLocationTerm.version', backref='td_devices')
    td_service_term = db.relationship('TdServiceTerm', primaryjoin='TdDevice.serviceTermVersion == TdServiceTerm.version', backref='td_devices')


    def to_json(self):
        json_device = {
            'idx': self.idx,
            'pushToken': self.pushToken,
            'model': self.model,
            'osVersion': self.osVersion,
            'appVersion': self.appVersion,
            'appCode': self.appCode,
            'appTagType': self.appTagType,
            'agreeTerm': self.agreeTerm,
            'agreeGPS': self.agreeGPS,
            'useBackground': self.useBackground,
            'language': self.language,
            'languageCode': self.languageCode,
            'serverName': self.serverName,
            'state': self.state,
            'dtRegistered': self.dtRegistered,
            'dtLastConnected': self.dtLastConnected,
            'dtTermAgreement': self.dtTermAgreement,
            'serviceTermVersion': self.serviceTermVersion,
            'locationTermVersion': self.locationTermVersion,
            'ipAddr': self.ipAddr
        }
        return json_device


class TdHolotag(db.Model):
    __tablename__ = 'td_holotag'
    __table_args__ = (
        db.Index('idx_td_holotag_02', 'code', 'companyCode'),
    )

    idx = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), nullable=False)
    name_kr = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(45))
    name_zh = db.Column(db.String(45))
    companyCode = db.Column(db.ForeignKey('td_company.code'), index=True)
    state = db.Column(Enum('Registered', 'Deleted', 'Paused'), nullable=False)
    attachType = db.Column(Enum('LABELBOX', 'POUCH', 'POUCH_PRINT'))
    certOverCnt = db.Column(db.Integer)
    certOverManyCnt = db.Column(db.Integer)
    registrant = db.Column(db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtRegistered = db.Column(db.DateTime, nullable=False)
    modifier = db.Column(db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtModified = db.Column(db.DateTime, nullable=False)
    sourceImage = db.Column(db.Text, nullable=False)
    note = db.Column(db.Text)
    hVersion = db.Column(db.ForeignKey('td_tag_version.version'), nullable=False, index=True)
    mappingCode = db.Column(db.String(10), index=True)
    sqrUrl = db.Column(db.String(32))
    sqrVer = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    td_company = db.relationship('TdCompany', primaryjoin='TdHolotag.companyCode == TdCompany.code', backref='td_holotags')
    td_tag_version = db.relationship('TdTagVersion', primaryjoin='TdHolotag.hVersion == TdTagVersion.version', backref='td_holotags')
    td_admin = db.relationship('TdAdmin', primaryjoin='TdHolotag.modifier == TdAdmin.id', backref='tdadmin_td_holotags')
    td_admin1 = db.relationship('TdAdmin', primaryjoin='TdHolotag.registrant == TdAdmin.id', backref='tdadmin_td_holotags_0')


class TdLocationTerm(db.Model):
    __tablename__ = 'td_location_term'

    idx = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    termUrl = db.Column(db.String(45), nullable=False)
    state = db.Column(Enum('Registered', 'Deleted', 'Published'), nullable=False)
    dtRegistered = db.Column(db.DateTime, nullable=False)
    dtPublished = db.Column(db.DateTime)
    dtDeleted = db.Column(db.DateTime)


class TdModel(db.Model):
    __tablename__ = 'td_model'
    __table_args__ = (
        db.Index('idx_id_model_02', 'name', 'osType'),
    )

    idx = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    osType = db.Column(Enum('iOS', 'Android', 'Unknown'), nullable=False)
    resolution = db.Column(db.Text)
    dtRegistered = db.Column(db.DateTime, nullable=False)
    dtModified = db.Column(db.DateTime, nullable=False)


class TdRetailer(db.Model):
    __tablename__ = 'td_retailer'

    idx = db.Column(db.Integer, primary_key=True)
    rtid = db.Column(db.String(10), nullable=False, index=True)
    name_kr = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(45))
    name_zh = db.Column(db.String(45))
    companyCode = db.Column(db.ForeignKey('td_company.code'), index=True)
    state = db.Column(Enum('Registered', 'Deleted', 'Paused'), server_default=db.FetchedValue())
    note = db.Column(db.String(512))
    headerquarterYN = db.Column(Enum('Y', 'N'), nullable=False, server_default=db.FetchedValue())
    registrant = db.Column(db.String(20), nullable=False)
    dtRegistered = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    modifier = db.Column(db.String(20))
    dtModified = db.Column(db.DateTime)

    td_company = db.relationship('TdCompany', primaryjoin='TdRetailer.companyCode == TdCompany.code', backref='td_retailers')

    def to_json(self):
        json_retailer = {
            'idx': self.idx,
            'rtid': self.rtid,
            'name_kr': self.name_kr,
            'name_en': self.name_en,
            'name_zh': self.name_zh,
            'companyCode': self.companyCode,
            'company': TdCompany.query.filter_by(code=self.companyCode).first().name_kr,
            'state': self.state,
            'note': self.note,
            'headerquarterYN': self.headerquarterYN,
            'registrant': self.registrant,
            'dtRegistered': self.dtRegistered,
            'modifier': self.modifier,
            'dtModified': self.dtModified
        }
        return json_retailer


class TdServiceTerm(db.Model):
    __tablename__ = 'td_service_term'

    idx = db.Column(db.Integer, primary_key=True)
    appTagType = db.Column(db.String(1), nullable=False, server_default=db.FetchedValue())
    version = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    termUrl = db.Column(db.String(45), nullable=False)
    state = db.Column(Enum('Registered', 'Deleted', 'Published'), nullable=False)
    dtRegistered = db.Column(db.DateTime, nullable=False)
    dtPublished = db.Column(db.DateTime)
    dtDeleted = db.Column(db.DateTime)


class TdTagVersion(db.Model):
    __tablename__ = 'td_tag_version'

    idx = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(11), nullable=False, unique=True)
    type = db.Column(Enum('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG', 'RANDOMTAG', 'SQRTAG'), nullable=False)
    name_kr = db.Column(db.String(60), nullable=False)
    name_en = db.Column(db.String(60), nullable=False)
    name_zh = db.Column(db.String(60), nullable=False)
    state = db.Column(Enum('Enable', 'Disable', 'Deleted'), nullable=False, server_default=db.FetchedValue())
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    registrant = db.Column(db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtRegistered = db.Column(db.DateTime, nullable=False)
    modifier = db.Column(db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtModified = db.Column(db.DateTime, nullable=False)
    note = db.Column(db.Text)

    td_admin = db.relationship('TdAdmin', primaryjoin='TdTagVersion.modifier == TdAdmin.id', backref='tdadmin_td_tag_versions')
    td_admin1 = db.relationship('TdAdmin', primaryjoin='TdTagVersion.registrant == TdAdmin.id', backref='tdadmin_td_tag_versions_0')

    def to_json(self):
        json_tag_version = {
            'idx': self.idx,
            'version': self.version,
            'name_kr': self.name_kr,
            'name_en': self.name_en,
            'name_zh': self.name_zh,
            'type': self.type,
            'width': self.width,
            'state': self.state,
            'height': self.height,
            'description': self.description,
            'registrant': self.registrant,
            'dtRegistered': self.dtRegistered,
            'modifier': self.modifier,
            'dtModified': self.dtModified,
            'note': self.note
        }
        return json_tag_version


class ThCertification(db.Model):
    __tablename__ = 'th_certification'

    idx = db.Column(db.BigInteger, primary_key=True, index=True)
    deviceID = db.Column(db.String(50), nullable=False, index=True)
    companyCode = db.Column(db.ForeignKey('td_company.code'), index=True)
    tagType = db.Column(Enum('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG', 'RANDOMTAG', 'SQRTAG'))
    tagCode = db.Column(db.String(10), index=True)
    hVersion = db.Column(db.ForeignKey('td_tag_version.version'), index=True)
    mappingCode = db.Column(db.String(10))
    image = db.Column(db.String(128), index=True)
    result = db.Column(Enum('Genuine', 'Counterfeit', 'Revalidation', 'Exprired', 'Invalid', 'Retry', 'OverCert', 'DifferentQR', 'CommonQR', 'NotiOverCert'), nullable=False)
    resultDetail = db.Column(db.Integer, server_default=db.FetchedValue())
    osType = db.Column(Enum('iOS', 'Android', 'Unknown', 'Web'), nullable=False)
    dtCertificate = db.Column(db.DateTime, nullable=False, index=True)
    longitude = db.Column(db.String(45))
    latitude = db.Column(db.String(45))
    regionIdx = db.Column(db.BigInteger, nullable=False, index=True, server_default=db.FetchedValue())
    random = db.Column(db.String(16), index=True)
    randomCnt = db.Column(db.Integer, server_default=db.FetchedValue())
    retailerID = db.Column(db.String(10))
    mode = db.Column(Enum('V', 'P'))
    data = db.Column(db.String(64))

    td_company = db.relationship('TdCompany', primaryjoin='ThCertification.companyCode == TdCompany.code', backref='th_certifications')
    td_tag_version = db.relationship('TdTagVersion', primaryjoin='ThCertification.hVersion == TdTagVersion.version', backref='th_certifications')

    def to_json(self):
        json_cert = {
            'idx': self.idx,
            'deviceID': self.deviceID,
            'companyCode': self.companyCode,
            'tagType': self.tagType,
            'tagCode': self.tagCode,
            'hVersion': self.hVersion,
            'mappingCode': self.mappingCode,
            'image': self.image,
            'result': self.result,
            'resultDetail': self.resultDetail,
            'osType': self.osType,
            'dtCertificate': self.dtCertificate,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'regionIdx': self.regionIdx,
            'random': self.random,
            'randomCnt': self.randomCnt,
            'retailerID': self.retailerID,
            'mode': self.mode,
            'data': self.data
        }
        return json_cert


class ThReport(db.Model):
    __tablename__ = 'th_report'

    idx = db.Column(db.Integer, primary_key=True)
    deviceID = db.Column(db.ForeignKey('td_device.pushToken'), nullable=False, index=True)
    companyCode = db.Column(db.ForeignKey('td_company.code'), index=True)
    tagCode = db.Column(db.String(10), index=True)
    hVersion = db.Column(db.ForeignKey('td_tag_version.version'), index=True)
    image = db.Column(db.Text, nullable=False)
    imageProduct = db.Column(db.Text)
    latitude = db.Column(db.String(45))
    longitude = db.Column(db.String(45))
    address = db.Column(db.String(256))
    dtCreated = db.Column(db.DateTime, nullable=False, index=True)
    email = db.Column(db.String(100))
    content = db.Column(db.Text)
    category = db.Column(db.Integer)
    contact = db.Column(db.String(64))
    contactType = db.Column(Enum('CONTACT_NUM', 'WECHAT', 'LINE', 'KAKAOTALK'))
    purchasePlace = db.Column(db.String(120))
    onlinePurchasePlace = db.Column(db.String(120))
    purchaseDate = db.Column(db.String(8))
    type = db.Column(Enum('Report', 'Expire', 'Share', 'Invalid'), nullable=False)
    tagType = db.Column(Enum('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG', 'RANDOMTAG', 'SQRTAG'))
    mappingCode = db.Column(db.String(10))
    random = db.Column(db.String(16))
    retailerID = db.Column(db.String(10))
    state = db.Column(Enum('Question', 'Answer', 'Holding'), nullable=False, server_default=db.FetchedValue())
    answerer = db.Column(db.ForeignKey('td_admin.id', ondelete='CASCADE'), index=True)
    dtAnswer = db.Column(db.DateTime)
    aContent = db.Column(db.Text)
    osType = db.Column(Enum('iOS', 'Android', 'Unknown'), nullable=False)
    memo = db.Column(db.Text)
    certificationIdx = db.Column(db.BigInteger, server_default=db.FetchedValue())
    importantYN = db.Column(Enum('Y', 'N'), nullable=False, server_default=db.FetchedValue())
    codeState = db.Column(db.String(6))
    codeChannel = db.Column(db.String(6))
    resultDetail = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    data = db.Column(db.String(64))

    td_admin = db.relationship('TdAdmin', primaryjoin='ThReport.answerer == TdAdmin.id', backref='th_reports')
    td_company = db.relationship('TdCompany', primaryjoin='ThReport.companyCode == TdCompany.code', backref='th_reports')
    td_device = db.relationship('TdDevice', primaryjoin='ThReport.deviceID == TdDevice.pushToken', backref='th_reports')
    td_tag_version = db.relationship('TdTagVersion', primaryjoin='ThReport.hVersion == TdTagVersion.version', backref='th_reports')


class TiHolotag(db.Model):
    __tablename__ = 'ti_holotag'

    idx = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    tagIdx = db.Column(db.ForeignKey('td_holotag.idx'), nullable=False, index=True)
    path = db.Column(db.Text, nullable=False)
    state = db.Column(Enum('Registered', 'Deleted', 'Paused'), nullable=False)
    registrant = db.Column(db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtRegistered = db.Column(db.DateTime, nullable=False)
    modifier = db.Column(db.ForeignKey('td_admin.id'), nullable=False, index=True)
    dtModified = db.Column(db.DateTime, nullable=False)
    note = db.Column(db.Text)

    td_admin = db.relationship('TdAdmin', primaryjoin='TiHolotag.modifier == TdAdmin.id', backref='tdadmin_ti_holotags')
    td_admin1 = db.relationship('TdAdmin', primaryjoin='TiHolotag.registrant == TdAdmin.id', backref='tdadmin_ti_holotags_0')
    td_holotag = db.relationship('TdHolotag', primaryjoin='TiHolotag.tagIdx == TdHolotag.idx', backref='ti_holotags')


class TlLogin(db.Model):
    __tablename__ = 'tl_login'

    idx = db.Column(db.BigInteger, primary_key=True)
    id = db.Column(db.String(20), nullable=False)
    resultCode = db.Column(db.String(4), nullable=False)
    dtAttempted = db.Column(db.DateTime, nullable=False)
    remoteAddr = db.Column(db.String(23), nullable=False)

    def to_json(self):

        u = TdAdmin.query.filter_by(id=self.id).first()
        print(u)
        json_login = {
            'idx': self.idx,
            'id': self.id,
            'resultCode': self.resultCode,
            'dtAttempted': self.dtAttempted,
            'remoteAddr': self.remoteAddr,
            'role_name': TcRole.query.filter_by(code=u.role).first().name_kr,
            'name': u.name
        }
        return json_login


class TsActiveUniqueCount(db.Model):
    __tablename__ = 'ts_active_unique_count'
    __table_args__ = (
        db.Index('index_active01', 'companyCode', 'osType', 'date'),
    )

    idx = db.Column(db.Integer, primary_key=True)
    companyCode = db.Column(db.String(10))
    appTagType = db.Column(db.String(1), nullable=False, server_default=db.FetchedValue())
    osType = db.Column(Enum('iOS', 'Android', 'Unknown'), nullable=False)
    date = db.Column(db.String(8), nullable=False)
    active_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    unique_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    cert_unique_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    regApp_count = db.Column(db.Integer, server_default=db.FetchedValue())
    registerDt = db.Column(db.DateTime, server_default=db.FetchedValue())


class TsAppdownDaily(db.Model):
    __tablename__ = 'ts_appdown_daily'

    idx = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(8), nullable=False)
    companyCode = db.Column(db.ForeignKey('td_company.code'), index=True)
    osType = db.Column(Enum('iOS', 'Android', 'Unknown'), nullable=False)
    tagType = db.Column(Enum('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG'))
    downloadCount = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    td_company = db.relationship('TdCompany', primaryjoin='TsAppdownDaily.companyCode == TdCompany.code', backref='ts_appdown_dailies')


class TsCertReportCount(db.Model):
    __tablename__ = 'ts_cert_report_count'
    __table_args__ = (
        db.Index('index_cert01', 'companyCode', 'tagCode', 'osType', 'type', 'date'),
    )

    idx = db.Column(db.Integer, primary_key=True)
    companyCode = db.Column(db.String(10))
    tagType = db.Column(Enum('HOLOTAG_ONLY', 'HOLOTAG_BARCODE', 'HYBRIDTAG', 'RANDOMTAG', 'SQRTAG'))
    tagCode = db.Column(db.String(10))
    osType = db.Column(Enum('iOS', 'Android', 'Unknown'), nullable=False)
    type = db.Column(db.String(30), nullable=False)
    date = db.Column(db.String(8), nullable=False)
    count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    registerDt = db.Column(db.DateTime)

    def to_json(self):
        json_cert_report = {
            'idx': self.idx,
            'companyCode': self.companyCode,
            'tagType': self.tagType,
            'tagCode': self.tagCode,
            'osType': self.osType,
            'type': self.type,
            'date': self.date,
            'count': self.count,
            'registerDt': self.registerDt
        }
        return json_cert_report


class TdRandomMnge(db.Model):
    __tablename__ = 'td_random_mnge'
    __table_args__ = (
        db.Index('idx_td_random_mnge_02', 'companyCode', 'tagCode', 'ticketStartIdx'),
    )

    idx = db.Column(db.Integer, primary_key=True)
    companyCode = db.Column(db.ForeignKey('td_company.code'), nullable=False)
    tagCode = db.Column(db.String(10), nullable=False)
    retailerID = db.Column(db.ForeignKey('td_retailer.rtid'), index=True)
    tableNum = db.Column(db.Integer, nullable=False)
    ticketCnt = db.Column(db.Integer, nullable=False)
    ticketStartIdx = db.Column(db.BigInteger)
    ticketEndIdx = db.Column(db.BigInteger)
    dtExpired = db.Column(db.DateTime)
    ticketFileName = db.Column(db.String(128), unique=True)
    ticketListState = db.Column(Enum('ING', 'Complete'))
    delYN = db.Column(Enum('Y', 'N'), nullable=False, server_default=db.FetchedValue())
    memo = db.Column(db.String(64))
    dtRegistered = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    registrant = db.Column(db.String(20), nullable=False)
    dtModified = db.Column(db.DateTime)
    dtPrinted = db.Column(db.DateTime)
    dtShipping = db.Column(db.DateTime)
    modifier = db.Column(db.String(20))

    td_company = db.relationship('TdCompany', primaryjoin='TdRandomMnge.companyCode == TdCompany.code', backref='td_random_mnges')
    td_retailer = db.relationship('TdRetailer', primaryjoin='TdRandomMnge.retailerID == TdRetailer.rtid', backref='td_random_mnges')

    def to_json(self):
        json_random_mnge = {
            'idx': self.idx,
            'companyCode': self.companyCode,
            'tagCode': self.tagCode,
            'retailerID': self.retailerID,
            'tableNum': self.tableNum,
            'ticketCnt': self.ticketCnt,
            'ticketStartIdx': self.ticketStartIdx,
            'ticketEndIdx': self.ticketEndIdx,
            'dtExpired': self.dtExpired,
            'ticketFileName': self.ticketFileName,
            'ticketListState': self.ticketListState,
            'delYN': self.delYN,
            'memo': self.memo,
            'dtRegistered': self.dtRegistered,
            'registrant': self.registrant,
            'dtModified': self.dtModified,
            'dtPrinted': self.dtPrinted,
            'dtShipping': self.dtShipping,
            'modifier': self.modifier,
        }
        return json_random_mnge


class TdAdminApp(db.Model):
    __tablename__ = 'td_admin_app'

    idx = db.Column(db.Integer, primary_key=True)
    pushToken = db.Column(db.String(50), nullable=False, index=True)
    companyName = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    contact = db.Column(db.String(32), nullable=False)
    state = db.Column(Enum('Registered', 'Approved', 'Deleted'), nullable=False, server_default=db.FetchedValue())
    dtRegistered = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    dtModified = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    modifier = db.Column(db.String(20))

    def to_json(self):
        json_admin_app = {
            'idx': self.idx,
            'pushToken': self.pushToken,
            'companyName': self.companyName,
            'name': self.name,
            'contact': self.contact,
            'state': self.state,
            'dtRegistered': self.dtRegistered,
            'dtModified': self.dtModified,
            'modifier': self.modifier
        }
        return json_admin_app