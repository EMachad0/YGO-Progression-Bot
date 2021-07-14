from notebooks import db


class Player(db.Model):
    __tablename__ = 'player'
    player_cod = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_cod = db.Column(db.BigInteger, db.ForeignKey('discord_user.user_cod'))
    server_cod = db.Column(db.BigInteger, db.ForeignKey('discord_server.server_cod'))


def insert_player(user_cod, server_cod):
    ins = db.insert(Player).values(user_cod=user_cod, server_cod=server_cod).\
        on_conflict_do_nothing(index_elements=[Player.user_cod, Player.server_cod])
    db.session.execute(ins)
    db.session.commit()
    
    
def get_player_by_user_server(user_cod, server_cod):
    return db.session.query(Player).filter(Player.user_cod==user_cod, Player.server_cod==server_cod).first()


def get_player_count_by_server(server_cod):
    return db.session.query(Player).filter(Player.server_cod==server_cod).count()


def get_players_by_server(server_cod):
    return db.session.query(Player).filter(Player.server_cod==server_cod).all()


if __name__ == '__main__':
    from notebooks.dao import *
    print(get_player_count_by_server(823962832583655424))