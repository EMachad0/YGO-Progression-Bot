from notebooks import db

class Banlist(db.Model):
    __tablename__ = 'banlist'
    banlist_cod = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    release_date = db.Column(db.Date, nullable=False, unique=True)
    list = db.Column(db.Text)


def get_banlist(banlist_cod):
    return Banlist.query.get(banlist_cod)


def get_banlist_by_date(release_date):
    return Banlist.query.filter_by(release_date=release_date).first()