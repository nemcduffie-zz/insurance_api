from passlib.hash import pbkdf2_sha256
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_user(dbsession, username) -> str:
        return dbsession.query.filter_by(username=username).first()

    @staticmethod
    def pw_hash(password) -> str:
        return pbkdf2_sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash) -> str:
        return pbkdf2_sha256.verify(password, hash)


class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))
    
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(dbsession, jti) -> bool:
        query = dbsession.query.filter_by(jti=jti).first()
        return bool(query)
