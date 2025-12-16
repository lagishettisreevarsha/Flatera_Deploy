from extensions import db

class Amenity(db.Model):
    __tablename__='amenities'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),unique=True,nullable=False)
    description=db.Column(db.String(200))