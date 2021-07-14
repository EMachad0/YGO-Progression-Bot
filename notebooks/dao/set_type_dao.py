from notebooks import db


class SetType(db.Model):
    __tablename__ = 'set_type'
    set_type_cod = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    num_cards = db.Column(db.Integer)
    release_date = db.Column(db.Text)
