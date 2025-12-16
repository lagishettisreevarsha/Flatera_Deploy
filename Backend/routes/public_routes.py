from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.booking import Booking
from models.tower import Tower
from models.flat import Flat
from models.amenity import Amenity
from decoraters import admin_required

public_bp=Blueprint('public',__name__)

@public_bp.route('/towers',methods=['GET'])
def get_towers():
    towers=Tower.query.all()
    data=[{"id":tower.id,
           "name":tower.name
           } for tower in towers]
    return jsonify(data),200

@public_bp.route('/flats',methods=['GET'])
def get_flats():
    flats=Flat.query.filter_by(is_available=True).all()
    data=[{
        "id":flat.id,
        "flat_no":flat.flat_no,
        "bedrooms":flat.bedrooms,
        "sqft":flat.sqft,
        "rent":flat.rent,
        "tower":flat.tower.name
    } for flat in flats]
    return jsonify(data),200

@public_bp.route('/amenities',methods=['GET'])
def get_amenities():
    amenities=Amenity.query.all()
    data=[{
        "id":amenity.id,
        "name":amenity.name,
        "description":amenity.description
    } for amenity in amenities]
    return jsonify(data),200

@public_bp.route('/tower/<int:tower_id>/flats',methods=['GET'])
def get_flats_by_tower(tower_id):
    tower=Tower.query.get(tower_id)
    if not tower:
        return jsonify({'message':'Tower not found'}),404

    flats=Flat.query.filter_by(tower_id=tower_id,is_available=True).all()
    data=[{
        "id":flat.id,
        "flat_no":flat.flat_no,
        "bedrooms":flat.bedrooms,
        "sqft":flat.sqft,
        "rent":flat.rent
    } for flat in flats]
    return jsonify(data),200

@public_bp.route('/book/<int:flat_id>',methods=['POST'])
@jwt_required()
def req_booking(flat_id):
    flat=Flat.query.get(flat_id)
    if not flat or not flat.is_available:
        return jsonify({'message':'Flat not available'}),404

    user=get_jwt_identity()
    user_id=user['id']

    new_booking=Booking (
        user_id=user_id,
        flat_id=flat_id,
        status='pending'
    )

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({'message':'Booking request submitted'}),201