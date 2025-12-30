from app import app, db
from models.tower import Tower
from models.flat import Flat
from models.amenity import Amenity

def init_database():
    with app.app_context():
      
        db.create_all()
        
       
        if Amenity.query.count() == 0:
            amenities = [
                Amenity(name='Parking', description='Secure covered parking for residents and visitors'),
                Amenity(name='Gym', description='24/7 fitness center with modern equipment'),
                Amenity(name='Swimming Pool', description='Olympic size swimming pool with lifeguard'),
                Amenity(name='Club House', description='Community gathering space for events and parties'),
                Amenity(name='Power Backup', description='24/7 generator backup for all apartments'),
                Amenity(name='Security', description='24/7 CCTV surveillance and security personnel'),
                Amenity(name='Elevator', description='High-speed elevators with backup power'),
                Amenity(name='Water Supply', description='24/7 water supply with purification system'),
                Amenity(name='Gas Connection', description='Piped gas connection for cooking'),
                Amenity(name='Intercom', description='Video intercom system for security'),
                Amenity(name='Garden', description='Landscaped garden with walking paths'),
                Amenity(name='Play Area', description='Children\'s play area with safety equipment')
            ]
            
            for amenity in amenities:
                db.session.add(amenity)
            
            db.session.commit()
            print("Sample amenities created successfully!")
        
       
        if Tower.query.count() == 0:
            towers = [
                Tower(name='Tower A'),
                Tower(name='Tower B'),
                Tower(name='Tower C'),
                Tower(name='Tower D'),
                Tower(name='Tower E'),
                Tower(name='Tower F')
            ]
            
            for tower in towers:
                db.session.add(tower)
            
            db.session.commit()
            print("Sample towers created successfully!")
        
       
        if Flat.query.count() == 0:
            towers = Tower.query.all()
            for i, tower in enumerate(towers[:3]): 
                for floor in range(1, 4): 
                    for unit in range(1, 3):  
                        flat = Flat(
                            flat_no=f"{tower.name}-{floor:02d}{unit:02d}",
                            bedrooms=2 if unit == 1 else 3,
                            sqft=1200 if unit == 1 else 1800,
                            rent=25000 + (floor * 1000) + (unit * 5000),
                            tower_id=tower.id,
                            is_available=True,
                            floor=floor,
                            description=f"Spacious {2 if unit == 1 else 3}BHK flat in {tower.name} on floor {floor} with modern amenities and excellent ventilation.",
                            features=f"Parking,24/7 Security,Power Backup,Gym,Swimming Pool,{'Garden' if floor == 1 else 'Balcony'}"
                        )
                        db.session.add(flat)
            
            db.session.commit()
            print("Sample flats created successfully!")
        
        print(f"Database initialized! Towers: {Tower.query.count()}, Amenities: {Amenity.query.count()}, Flats: {Flat.query.count()}")
        
        amenities = Amenity.query.all()
        for amenity in amenities:
            print(f"• {amenity.name}: {amenity.description}")
        print("========\n")

if __name__ == '__main__':
    init_database()
