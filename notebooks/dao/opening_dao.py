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
    print(ins)
    db.session.execute(ins)
    db.session.commit()


def update_opening(open_cod, values):
    db.session.query(Opening).filter(Opening.open_cod == open_cod).update(values)
    db.session.commit()


def get_player_available_openings(player_cod):
    return db.session.query(Opening.open_cod, Opening.set_cod, Opening.quantity). \
        filter(Opening.player_cod == player_cod, Opening.quantity > 0).all()


def get_openings_by_player(player_cod):
    return db.session.query(Opening).filter(Opening.player_cod == player_cod).all()
