from notebooks import db


class Card(db.Model):
    __tablename__ = 'card'
    card_cod = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    flavour_text = db.Column(db.Text)
    atk = db.Column(db.Integer)
    dff = db.Column('def', db.Integer)
    level = db.Column(db.Integer)
    scale = db.Column(db.Integer)
    race = db.Column(db.String(100))
    attribute = db.Column(db.String(100))
    archetype = db.Column(db.String(100))
    cod_img = db.Column(db.Integer)
    link_val = db.Column(db.Integer)
    link_markers = db.Column(db.Integer)
