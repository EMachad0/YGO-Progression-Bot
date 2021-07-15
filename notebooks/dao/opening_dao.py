from notebooks import db


class Opening(db.Model):
    __tablename__ = 'opening'
    open_cod = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    set_cod = db.Column(db.String(3), db.ForeignKey('set.set_cod'))
    player_cod = db.Column(db.Integer, db.ForeignKey('player.player_cod'))
    quantity = db.Column(db.Integer)


def insert_opening(values, quantity):
    ins = db.insert(Opening).values(values). \
        on_conflict_do_update(index_elements=[Opening.set_cod, Opening.player_cod],
                              set_={'quantity': Opening.quantity + quantity})
    db.session.execute(ins)
    db.session.commit()


def update_opening(open_cod, values):
    db.session.query(Opening).filter(Opening.open_cod == open_cod).update(values)
    db.session.commit()


def get_player_available_openings(player_cod):
    from notebooks.dao import Set
    return db.session.query(Opening.open_cod, Opening.set_cod, Opening.quantity). \
        filter(Opening.player_cod == player_cod, Opening.quantity > 0) \
        .join(Set, Opening.set_cod == Set.set_cod) \
        .order_by(Set.release_date).all()


def get_openings_by_player(player_cod):
    from notebooks.dao import Set, SetType
    return db.session.query(Opening.set_cod, Opening.open_cod, Opening.quantity, SetType.num_cards, SetType.list) \
        .join(Set, Opening.set_cod == Set.set_cod) \
        .join(SetType, Set.type_cod == SetType.set_type_cod) \
        .filter(Opening.player_cod == player_cod, Opening.quantity > 0) \
        .order_by(Set.release_date).first()


def get_opening_by_set_player(set_cod, player_cod):
    from notebooks.dao import Set, SetType
    return db.session.query(Opening.open_cod, Opening.quantity, SetType.num_cards, SetType.list) \
        .join(Set, Opening.set_cod == Set.set_cod) \
        .join(SetType, Set.type_cod == SetType.set_type_cod) \
        .filter(Opening.player_cod == player_cod, Set.set_cod == set_cod, Opening.quantity > 0).first()
