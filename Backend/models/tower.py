from extensions import db

class Tower(db.Model):
    __tablename__='towers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True,nullable=False)
    