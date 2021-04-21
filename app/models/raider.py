from app import db, login

class Raider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    game_class = db.Column(db.String(64))
    role = db.Column(db.String(64))
    realm = db.Column(db.String(64))
    guild = db.Column(db.String(64))

    def __repr__(self):
        return '<Raider {} {} {} {}-{}>'.format(self.name, self.game_class, self.role, self.realm, self.guild)
