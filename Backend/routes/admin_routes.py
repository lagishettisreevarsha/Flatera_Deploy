from flask import Blueprint, jsonify, request
from extensions import db
from models.booking import Booking
from models.flat import Flat
from models.tower import Tower
from models.amenity import Amenity
from models.user import User
from decoraters import admin_required
from schemas.flat_schema import FlatSchema
from schemas.amenity_schema import AmenitySchema
from marshmallow import ValidationError

admin_bp=Blueprint('/admin',__name__)

@admin_bp.route('/bookings',methods=['GET'])
# @admin_required
def get_all_bookings():
    try:
        # Join bookings with users and flats to get complete booking information
        bookings_data = db.session.query(Booking, User, Flat).join(User, Booking.user_id == User.id).join(Flat, Booking.flat_id == Flat.id).all()
        
        data = []
        for booking, user, flat in bookings_data:
            data.append({
                "id": booking.id,
                "user_id": booking.user_id,
                "user_name": user.name if user.name and user.name != 'public' else user.email.split('@')[0] if user.email else f"User {user.id}",
                "user_email": user.email,
                "flat_id": booking.flat_id,
                "flat_no": flat.flat_no,
                "tower_name": flat.tower.name if flat.tower else "Unknown Tower",
                "status": booking.status,
                "booking_date": booking.booking_date.isoformat() if booking.booking_date else None
            })
        
        return jsonify(data),200
    except Exception as e:
        print(f"Error loading bookings: {str(e)}")
        return jsonify({"error": "Failed to load bookings", "details": str(e)}),500

@admin_bp.route('/booking/<int:booking_id>/approve',methods=['POST'])
# @admin_required
def approve_booking(booking_id):
    booking=Booking.query.get(booking_id)
    if not booking:
        return jsonify({'message':'Booking not found'}),404

    # Update booking status
    booking.status='approved'
    
    # Make the flat unavailable since booking is confirmed
    flat = Flat.query.get(booking.flat_id)
    if flat:
        flat.is_available = False
    
    db.session.commit()
    return jsonify({'message':'Booking approved and flat marked as unavailable'}),200

@admin_bp.route('/booking/<int:booking_id>/decline',methods=['POST'])
# @admin_required
def decline_booking(booking_id):    
    booking=Booking.query.get(booking_id)
    if not booking:
        return jsonify({'message':'Booking not found'}),404

    # Update booking status
    booking.status='declined'
    
    # Keep the flat available since booking was declined
    flat = Flat.query.get(booking.flat_id)
    if flat:
        flat.is_available = True
    
    db.session.commit()
    return jsonify({'message':'Booking declined and flat remains available'}),200


@admin_bp.route('/towers',methods=['GET'])
# @admin_required
def get_towers():
    towers=Tower.query.all()

    data=[{"id":tower.id,
           "name":tower.name
           } for tower in towers]
    return jsonify(data),200


@admin_bp.route('/towers',methods=['POST'])
# @admin_required
def create_tower():
    data=request.json

    name=data.get('name')

    if not name:
        return jsonify({'message':'Name is required'}),400
    
    if Tower.query.filter_by(name=name).first():
        return jsonify({'message':'Tower already exists'}),400
    

    new_tower=Tower(
        name=name
    )

    db.session.add(new_tower)
    db.session.commit()

    return jsonify({'message':'Tower created successfully'}),201

@admin_bp.route('/towers',methods=['DELETE'])
# @admin_required
def delete_tower():
    data=request.json

    tower_id=data.get('tower_id')

    tower=Tower.query.get(tower_id)

    if not tower:
        return jsonify({'message':'Tower not found'}),404

    db.session.delete(tower)
    db.session.commit()

    return jsonify({'message':'Tower deleted successfully'}),200


@admin_bp.route("/towers/<int:tower_id>", methods=["PUT"])
# @admin_required
def update_tower(tower_id):
    tower = Tower.query.get(tower_id)

    if not tower:
        return {"msg": "Tower not found"}, 404

    data = request.json

    name = data.get("name")
    if not name:
        return {"msg": "Tower name is required"}, 400

    if Tower.query.filter(
        Tower.name == name,
        Tower.id != tower_id
    ).first():
        return {"msg": "Tower name already exists"}, 400

    tower.name = name
    db.session.commit()

    return {"msg": "Tower updated successfully"}, 200

@admin_bp.route('/flats',methods=['GET'])
# @admin_required
def get_flats():
    try:
        flats=Flat.query.all()

        data=[{
            "id":flat.id,
            "flat_no":flat.flat_no,
            "bedrooms":flat.bedrooms,
            "sqft":flat.sqft,
            "rent":flat.rent,
            "is_available":flat.is_available,
            "tower_id":flat.tower_id
        } for flat in flats]

        return jsonify(data),200
    except Exception as e:
        print(f"Error in admin get_flats: {str(e)}")
        return jsonify({"error": "Failed to load flats", "details": str(e)}),500

@admin_bp.route('/flats',methods=['POST'])
# @admin_required
def create_flat():
    if not request.is_json:
        return jsonify({'message':'JSON data required'}), 400
        
    data = request.json
    print(f"Received data: {data}")
    
    required_fields = ['flat_no', 'bedrooms', 'sqft', 'rent', 'tower_id']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        return jsonify({'message': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    
    try:
        flat_no = str(data['flat_no']).strip()
        bedrooms = int(data['bedrooms'])
        sqft = int(data['sqft'])
        rent = float(data['rent'])
        tower_id = int(data['tower_id'])
        is_available = data.get('is_available', True)
        description = data.get('description', '')
        features = data.get('features', '')
        floor = data.get('floor')
        
        if floor is not None:
            floor = int(floor)
    except (ValueError, TypeError) as e:
        return jsonify({'message': f'Invalid data format: {str(e)}'}), 400
    
    if not all([flat_no, bedrooms, sqft, rent, tower_id]):
        return jsonify({'message':'All required fields must be provided'}), 400
    
    if Flat.query.filter_by(flat_no=flat_no).first():
        return jsonify({'message':'Flat already exists'}), 400
    
    tower = Tower.query.get(tower_id)
    if not tower:
        return jsonify({'message':'Tower not found'}), 404
    
    try:
        new_flat = Flat(
            flat_no=flat_no,
            bedrooms=bedrooms,
            sqft=sqft,
            rent=rent,
            tower_id=tower_id,
            is_available=is_available,
            description=description,
            features=features,
            floor=floor
        )

        db.session.add(new_flat)
        db.session.commit()

        return jsonify({'message':'Flat created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({'message': f'Database error: {str(e)}'}), 500

@admin_bp.route('/flats/<int:flat_id>',methods=['PUT'])

@admin_required
def update_flat(flat_id):
    flat=Flat.query.get(flat_id)
    print("working")
    if not flat:
        return jsonify({'message':'Flat not found'}),404

    data=request.json
    print(data)
    flat_no=data.get('flat_no')
    bedrooms=data.get('bedrooms')
    sqft=data.get('sqft')
    rent=data.get('rent')
    is_available=data.get('is_available')
    tower_id=data.get('tower_id')

    if flat_no:
        if Flat.query.filter(Flat.flat_no==flat_no,Flat.id!=flat_id).first():
            return jsonify({'message':'Flat number already exists'}),400
        flat.flat_no=flat_no
    if bedrooms:
        flat.bedrooms=bedrooms
    if sqft:
        flat.sqft=sqft
    if rent:
        flat.rent=rent
    if is_available is not None:
        flat.is_available=is_available
    if tower_id:
        tower=Tower.query.get(tower_id)
        if not tower:
            return jsonify({'message':'Tower not found'}),404
        flat.tower_id=tower_id

    db.session.commit()

    return jsonify({'message':'Flat updated successfully'}),200


@admin_bp.route('/flats/<int:flat_id>',methods=['DELETE'])
# @admin_required
def delete_flat(flat_id):
    flat=Flat.query.get(flat_id)

    if not flat:
        return jsonify({'message':'Flat not found'}),404

    booking = Booking.query.filter_by(flat_id=flat.id).first()

    if booking:
        return jsonify({'message': 'Cannot delete flat with existing bookings'}), 400
    
    db.session.delete(flat)
    db.session.commit()

    return jsonify({'message':'Flat deleted successfully'}),200

@admin_bp.route('/amenities',methods=['GET'])
# @admin_required 
def get_amenities():
    amenities=Amenity.query.all()

    data=[{
        "id":amenity.id,
        "name":amenity.name,
        "description":amenity.description
    } for amenity in amenities]

    return jsonify(data),200

@admin_bp.route('/amenities',methods=['POST'])
# @admin_required
def create_amenity():
    data=request.json

    schema = AmenitySchema()
    try:
        validated_data = schema.load(request.json)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    name = validated_data["name"]
    description = validated_data.get("description")

    if not name or not description:
        return jsonify({'message':'Name and description are required'}),400
    
    if Amenity.query.filter_by(name=name).first():
        return jsonify({'message':'Amenity already exists'}),400
    

    new_amenity=Amenity(
        name=name,
        description=description
    )

    db.session.add(new_amenity)
    db.session.commit()

    return jsonify({'message':'Amenity added successfully'}),201

@admin_bp.route('/amenities/<int:amenity_id>',methods=['PUT'])
# @admin_required
def update_amenity(amenity_id):
    amenity=Amenity.query.get(amenity_id)

    if not amenity:
        return jsonify({'message':'Amenity not found'}),404

    data=request.json

    name=data.get('name')
    description=data.get('description')
    
    if name:
        amenity.name=name
    if description:
        amenity.description=description

    db.session.commit()

    return jsonify({'message':'Amenity updated successfully'}),200

@admin_bp.route('/amenities/<int:amenity_id>',methods=['DELETE'])
# @admin_required
def delete_amenity(amenity_id):
    amenity=Amenity.query.get(amenity_id)

    if not amenity:
        return jsonify({'message':'Amenity not found'}),404

    db.session.delete(amenity)
    db.session.commit()

    return jsonify({'message':'Amenity deleted successfully'}),200

@admin_bp.route('/tenants',methods=['GET'])
# @admin_required
def get_tenants():
    try:
        # Join bookings with users and flats to get complete tenant information
        tenants = db.session.query(Booking, User, Flat).join(User, Booking.user_id == User.id).join(Flat, Booking.flat_id == Flat.id).filter(Booking.status == "approved").all()
        
        print(f"Found {len(tenants)} tenants") # Debug log
        
        data = []
        for booking, user, flat in tenants:
            print(f"User: {user.name}, Email: {user.email}, Role: {user.role}") # Debug log
            data.append({
                "booking_id": booking.id,
                "user_id": user.id,
                "user_name": user.name if user.name and user.name != 'public' else user.email.split('@')[0] if user.email else f"User {user.id}",
                "user_email": user.email,
                "flat_id": flat.id,
                "flat_no": flat.flat_no,
                "tower_id": flat.tower_id,
                "booking_date": booking.booking_date.isoformat() if booking.booking_date else None
            })
        
        return jsonify(data), 200
    except Exception as e:
        print(f"Error loading tenants: {str(e)}")
        return jsonify({"error": "Failed to load tenants", "details": str(e)}), 500