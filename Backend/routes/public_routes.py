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
    try:
        # Get ALL flats (both available and unavailable) for public view
        flats=Flat.query.all()
        data=[]
        
        for flat in flats:
            try:
                tower_name = flat.tower.name if flat.tower else "Unknown Tower"
            except:
                tower_name = "Unknown Tower"
            
            flat_data = {
                "id":flat.id,
                "flat_no":flat.flat_no,
                "bedrooms":flat.bedrooms,
                "sqft":flat.sqft,
                "rent":flat.rent,
                "is_available":flat.is_available,
                "tower_name":tower_name,
                "tower_id":flat.tower_id,
                "description":getattr(flat, 'description', None) or f"Spacious {flat.bedrooms}BHK flat in {tower_name}",
                "location":f"Floor {getattr(flat, 'floor', 'N/A')}, {tower_name}" if hasattr(flat, 'floor') else tower_name,
                "image":getattr(flat, 'image', None),
                "features":getattr(flat, 'features', None) or ["Parking", "24/7 Security"]
            }
            data.append(flat_data)
        
        return jsonify(data),200
    except Exception as e:
        print(f"Error in get_flats: {str(e)}")
        return jsonify({"error": "Failed to load flats", "details": str(e)}),500

@public_bp.route('/flats/<int:flat_id>',methods=['GET'])
def get_flat_details(flat_id):
    flat=Flat.query.get(flat_id)
    if not flat:
        return jsonify({'error':'Flat not found'}),404
    
    data={
        "id":flat.id,
        "flat_no":flat.flat_no,
        "bedrooms":flat.bedrooms,
        "sqft":flat.sqft,
        "rent":flat.rent,
        "is_available":flat.is_available,
        "tower_name":flat.tower.name if flat.tower else "Unknown",
        "tower_id":flat.tower_id,
        "description":flat.description if flat.description else f"Spacious {flat.bedrooms}BHK flat in {flat.tower.name if flat.tower else 'Unknown'}",
        "location":f"Floor {flat.floor}, {flat.tower.name if flat.tower else 'Unknown'}" if hasattr(flat, 'floor') else f"{flat.tower.name if flat.tower else 'Unknown'}",
        "image":flat.image if hasattr(flat, 'image') and flat.image else None,
        "features":flat.features if hasattr(flat, 'features') and flat.features else ["Parking", "24/7 Security"]
    }
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
    try:
        flat=Flat.query.get(flat_id)
        if not flat:
            return jsonify({'message':'Flat not found'}),404
        
        if not flat.is_available:
            return jsonify({'message':'Flat not available'}),400

        user=get_jwt_identity()
        
        # Handle different JWT token formats
        if isinstance(user, str):
            # If user is a string, it might be the user ID directly
            user_id = user
        elif isinstance(user, dict):
            # If user is a dictionary, get the ID
            user_id = user.get('id')
        else:
            return jsonify({'message':'User not authenticated properly'}),401
        
        if not user_id:
            return jsonify({'message':'User ID not found in token'}),401

        # Check if user already has a booking for this flat
        existing_booking = Booking.query.filter_by(user_id=user_id, flat_id=flat_id).first()
        if existing_booking:
            return jsonify({'message':'You already have a booking request for this flat'}),400

        new_booking=Booking (
            user_id=user_id,
            flat_id=flat_id,
            status='pending'
        )

        db.session.add(new_booking)
        db.session.commit()

        return jsonify({'message':'Booking request submitted'}),201
        
    except Exception as e:
        print(f"Booking error: {str(e)}")
        db.session.rollback()
        return jsonify({'error':'Failed to submit booking request', 'details': str(e)}),500