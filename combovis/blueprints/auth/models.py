from combovis.app import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.uid

    def check_password(self, password):
        return check_password_hash(self.password, password)
