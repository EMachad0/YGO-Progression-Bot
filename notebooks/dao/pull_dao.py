from notebooks import db


class Pull(db.Model):
    __tablename__ = 'pull'
    pull_cod = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    card_cod = db.Column(db.Integer, db.ForeignKey('card.card_cod'))
    set_cod = db.Column(db.String(3), db.ForeignKey('set.set_cod'))
    rarity = db.Column(db.String(100))
    rarity_code = db.Column(db.String(100))
    price = db.Column(db.String(30))


PACK_QUERY = "select pull_cod, cod_img, rarity from " \
             "(select card_cod, cod_img from card) c join" \
             "(select card_cod, pull_cod, rarity from pull where set_cod=%s) p on c.card_cod = p.card_cod;"


def get_pull_values(set_cod):
    from notebooks.dao import Card
    
    sub = db.session.query(Pull.pull_cod, Pull.card_cod, Pull.rarity).filter(Pull.set_cod == set_cod).subquery()
    return db.session.query(sub.c.pull_cod, sub.c.rarity, Card.cod_img).join(sub, sub.c.card_cod == Card.card_cod).all()
