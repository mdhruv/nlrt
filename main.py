from app import app, db
from app.models.user import User
from app.models.raider import Raider

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Raider': Raider}