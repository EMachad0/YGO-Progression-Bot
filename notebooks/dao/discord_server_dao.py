from notebooks import db


class DiscordServer(db.Model):
    __tablename__ = 'discord_server'
    server_cod = db.Column(db.BigInteger, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100))
    img_url = db.Column(db.String(500))
    settings = db.Column(db.Text)


def insert_discord_server(server_cod, name, img_url, settings):
    ins = db.insert(DiscordServer).values(server_cod=server_cod, name=name, img_url=img_url, settings=settings). \
        on_conflict_do_update(index_elements=[DiscordServer.server_cod], set_={'name': name, 'img_url': img_url})
    db.session.execute(ins)
    db.session.commit()


def get_discord_server(server_cod):
    return db.session.query(DiscordServer).get(server_cod)


def drop_discord_server(server_cod):
    db.session.query(DiscordServer).filter(DiscordServer.server_cod == server_cod).delete()
    db.session.commit()


def update_server(server_cod, values):
    db.session.query(DiscordServer).filter(DiscordServer.server_cod == server_cod).update(values)
    db.session.commit()
