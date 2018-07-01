from app import app, db
from models import User, Defect


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Defect': Defect}
