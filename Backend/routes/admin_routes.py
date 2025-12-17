from flask import Blueprint, jsonify, request
from extensions import db
from models.booking import Booking
from models.flat import Flat
from models.tower import Tower
from models.amenity import Amenity
from decoraters import admin_required
from schemas.flat_schema import FlatSchema
from schemas.amenity_schema import AmenitySchema
from marshmallow import ValidationError

admin_bp=Blueprint('/admin',__name__)

@admin_bp.route('/bookings',methods=['GET'])
# @admin_required
def get_all_bookings():
    bookings=Booking.query.all()
    data=[{
        "id":booking.id,
        "user_id":booking.user_id,
        "flat_id":booking.flat_id,
        "status":booking.status,
        "created_at":booking.created_at
    } for booking in bookings]
    return jsonify(data),200

@admin_bp.route('/booking/<int:booking_id>/approve',methods=['POST'])
# @admin_required
def approve_booking(booking_id):
    booking=Booking.query.get(booking_id)
    if not booking:
        return jsonify({'message':'Booking not found'}),404

    booking.status='approved'
    db.session.commit()
    return jsonify({'message':'Booking approved'}),200

@admin_bp.route('/booking/<int:booking_id>/decline',methods=['POST'])
# @admin_required
def decline_booking(booking_id):    
    booking=Booking.query.get(booking_id)
    if not booking:
        return jsonify({'message':'Booking not found'}),404

    booking.status='declined'
    db.session.commit()
    return jsonify({'message':'Booking declined'}),200


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
    # Handle both JSON and multipart form data
    if request.is_json:
        data = request.json
        image_filename = None
    else:
        data = request.form.to_dict()
        image_file = request.files.get('image')
        image_filename = None
        
        if image_file and image_file.filename:
            # Save image file
            import os
            from werkzeug.utils import secure_filename
            
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join(os.getcwd(), 'static', 'images', 'flats')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Secure the filename and save the file
            filename = secure_filename(image_file.filename)
            image_filename = f"{filename}"
            image_path = os.path.join(upload_dir, image_filename)
            image_file.save(image_path)
            
            print(f"Image saved: {image_path}")
    
    print(f"Received data: {data}")
    schema = FlatSchema()
    try:
        # Convert form data to dict for validation
        if request.is_json:
            validated_data = schema.load(request.json)
        else:
            validated_data = schema.load(data)
    except ValidationError as err:
        return {"errors": err.messages}, 400
    
    flat_no = validated_data["flat_no"]
    bedrooms = validated_data["bedrooms"]
    sqft = validated_data["sqft"]
    rent = validated_data["rent"]
    tower_id = validated_data["tower_id"]
    is_available = validated_data.get("is_available", True)
    
    # Add additional fields
    description = validated_data.get("description")
    features = validated_data.get("features")
    floor = validated_data.get("floor")

    if not all([flat_no,bedrooms,sqft,rent,tower_id]):
        return jsonify({'message':'All required fields must be provided'}),400
    
    if Flat.query.filter_by(flat_no=flat_no).first():
        return jsonify({'message':'Flat already exists'}),400
    
    tower=Tower.query.get(tower_id)
    if not tower:
        return jsonify({'message':'Tower not found'}),404
    
    new_flat=Flat(
        flat_no=flat_no,
        bedrooms=bedrooms,
        sqft=sqft,
        rent=rent,
        tower_id=tower_id,
        is_available=is_available,
        image=image_filename,
        description=description,
        features=features,
        floor=floor
    )

    db.session.add(new_flat)
    db.session.commit()

    return jsonify({'message':'Flat created successfully', 'image': image_filename}),201

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
    tenants=Booking.query.filter_by(status="approved").all()

    data=[{
        "booking_id": tenant.id,
        "user_id": tenant.user_id,
        "flat_id": tenant.flat_id
    } for tenant in tenants]

    return jsonify(data),200