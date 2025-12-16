from extensions import db
from datetime import datetime

class Booking(db.Model):
    __tablename__='bookings'

    id=db.Column(db.Integer, primary_key=True)

    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flat_id=db.Column(db.Integer, db.ForeignKey('flats.id'), nullable=False)
    booking_date=db.Column(db.DateTime, default=datetime.utcnow)
    status=db.Column(db.String(20), nullable=False, default='pending')

    user=db.relationship('User')
    flat=db.relationship('Flat')