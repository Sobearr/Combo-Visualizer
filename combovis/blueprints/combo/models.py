from combovis.app import db


class Combo(db.Model):
    # table for the combos saved by the user
    __tablename__ = 'Combo'

    cid = db.Column(db.Integer, primary_key=True)
    notation = db.Column(db.String(), unique=True, nullable=False)
    drive = db.Column(db.String(), nullable=False)
    bars = db.Column(db.String(), nullable=False)


class Favourite(db.Model):
    # table with all combos and the users that saved them as favourites
    __tablename__ = 'Favourite'

    fid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey('Combo.cid'))
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'))
