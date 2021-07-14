from notebooks import db


class Collection(db.Model):
    __tablename__ = 'collection'
    collection_cod = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    player_cod = db.Column(db.Integer, db.ForeignKey('player.player_cod'))
    pull_cod = db.Column(db.Integer, db.ForeignKey('pull.pull_cod'))
    quantity = db.Column(db.Integer)


def insert_collection(values):
    ins = db.insert(Collection).values(values)
    db.session.execute(ins)
    db.session.commit()


def get_player_collection(player_cod, offset=None, limit=None, name_filter=None, sorts=None, filters=None):
    from notebooks.filters import apply_sort, apply_filter
    from notebooks.dao import Pull, Card

    query = db.session.query(Card.card_cod, Card.name, Card.atk, Card.level, Card.cod_img, Card.type, Card.level,
                             Card.scale, Card.link_val, Card.race, Card.attribute, Collection.quantity) \
        .join(Pull, Collection.pull_cod == Pull.pull_cod) \
        .join(Card, Pull.card_cod == Card.card_cod) \
        .filter(Collection.player_cod == player_cod)
    if name_filter is not None:
        query = query.filter(Card.name.ilike(name_filter))
    query = apply_sort(query, sorts)
    query = apply_filter(query, filters)
    query = query.offset(offset).limit(limit)
    # print(query.cte())
    return query.all()
