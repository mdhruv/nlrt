from app import db, login, constants
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean

partner_table = Table("partner_table", db.Model.metadata,
    Column("left_partner_id", Integer, ForeignKey("raider.id"), primary_key=True),
    Column("right_partner_id", Integer, ForeignKey("raider.id"), primary_key=True)
)

friend_table = Table("friend_table", db.Model.metadata,
    Column("left_friend_id", Integer, ForeignKey("raider.id"), primary_key=True),
    Column("right_friend_id", Integer, ForeignKey("raider.id"), primary_key=True)
)

class Raider(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    game_class = Column(String(64))
    role = Column(String(64))
    realm = Column(String(64))
    guild = Column(String(64))
    is_raid_leader = Column(Boolean)
    profession1 = Column(String(64))
    profession2 = Column(String(64))
    has_cooking = Column(Boolean)
    has_first_aid = Column(Boolean)
    has_fishing = Column(Boolean)
    
    alt_id = Column(Integer, ForeignKey('raider.id'))
    alt = db.relationship("Raider", foreign_keys=[alt_id], backref=db.backref('main', remote_side=[id]))
    
    friends = db.relationship("Raider", secondary=friend_table,
                        primaryjoin=id==friend_table.c.left_friend_id,
                        secondaryjoin=id==friend_table.c.right_friend_id)
    partner = db.relationship("Raider", secondary=partner_table,
                        uselist=False,
                        primaryjoin=id==partner_table.c.left_partner_id,
                        secondaryjoin=id==partner_table.c.right_partner_id)
                        
    def is_main(self):
        if self.main:
            return False
        return True
        
    def get_main(self):
        if self.main:
            return self.main
        return self
    
    def sort_key(self):
        score = 0
        if self.is_raid_leader:
            score+=2**16        
        bit = 15
        for role in constants.Roles:
            if self.role == role:
                score+=2**bit
            bit-=1
        for game_class in constants.Classes:
            if self.game_class == game_class:
                score+=2**bit
            bit-=1
        return score
        

    def __repr__(self):
        return '<Raider {} {} {} {}-{}>'.format(self.name, self.game_class, self.role, self.realm, self.guild)

    