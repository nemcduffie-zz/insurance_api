from run import db
from passlib.hash import pbkdf2_sha256

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_user(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def pw_hash(password):
        return pbkdf2_sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return pbkdf2_sha256.verify(password, hash)

class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)