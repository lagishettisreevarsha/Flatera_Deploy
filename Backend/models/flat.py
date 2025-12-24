from extensions import db

class Flat(db.Model):
    __tablename__='flats'

    id = db.Column(db.Integer, primary_key=True)
    flat_no = db.Column(db.String(10), unique=True, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    sqft=db.Column(db.Integer, nullable=False)
    rent=db.Column(db.Float, nullable=False)
    is_available=db.Column(db.Boolean, default=True)
    description=db.Column(db.Text, nullable=True)  
    features=db.Column(db.Text, nullable=True) 
    floor=db.Column(db.Integer, nullable=True) 

    tower_id=db.Column(db.Integer, db.ForeignKey('towers.id'), nullable=False)

    tower=db.relationship('Tower', backref="flats")