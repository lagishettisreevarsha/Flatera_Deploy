from app import app, db
from models.user import User
from models.tower import Tower
from models.flat import Flat
from models.amenity import Amenity
from models.booking import Booking

def init_postgres_database():
    """Initialize PostgreSQL database with tables and sample data"""
    with app.app_context():
        print("Creating database tables...")
        
        # Drop all tables and recreate (for fresh start)
        db.drop_all()
        db.create_all()
        
        print("Tables created successfully!")
        
        # Create default admin user
        admin_email = "admin@flatera.com"
        admin_password = "admin123"
        
        admin_user = User(
            name="Flatera Admin",
            email=admin_email,
            role="admin"
        )
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        
        # Create sample amenities
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
        
        # Create sample towers
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
        print("Sample data added successfully!")
        
        # Create sample flats
        towers = Tower.query.all()
        for i, tower in enumerate(towers[:3]):  # First 3 towers
            for floor in range(1, 6):  # 5 floors
                for unit in range(1, 4):  # 3 units per floor
                    flat = Flat(
                        flat_no=f"{tower.name}-{floor:02d}{unit:02d}",
                        bedrooms=2 if unit == 1 else (3 if unit == 2 else 4),
                        sqft=1200 if unit == 1 else (1800 if unit == 2 else 2400),
                        rent=25000 + (floor * 1000) + (unit * 5000),
                        tower_id=tower.id,
                        is_available=True,
                        floor=floor,
                        description=f"Spacious {2 if unit == 1 else (3 if unit == 2 else 4)}BHK flat in {tower.name} on floor {floor} with modern amenities and excellent ventilation.",
                        features=f"Parking,24/7 Security,Power Backup,Gym,Swimming Pool,{'Garden' if floor == 1 else 'Balcony'}"
                    )
                    db.session.add(flat)
        
        db.session.commit()
        
        print(f"Database initialized successfully!")
        print(f"- Admin user: {admin_email} / {admin_password}")
        print(f"- Towers: {Tower.query.count()}")
        print(f"- Amenities: {Amenity.query.count()}")
        print(f"- Flats: {Flat.query.count()}")

if __name__ == '__main__':
    init_postgres_database()