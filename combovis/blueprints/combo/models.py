from combovis.app import db


class Combo(db.Model):
    # Table for the combos saved by the user
    __tablename__ = 'Combo'

    cid = db.Column(db.Integer, primary_key=True)
    notation = db.Column(db.String(), unique=True, nullable=False)
    drive = db.Column(db.String(), nullable=False)
    bars = db.Column(db.String(), nullable=False)


class Favourite(db.Model):
    # Intersection table between User and Combo (many-to-many)
    __tablename__ = 'Favourite'

    fid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey('Combo.cid'))
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'))
