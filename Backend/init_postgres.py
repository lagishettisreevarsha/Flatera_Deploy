
import os

from app import app, db
from models.user import User
from models.tower import Tower
from models.flat import Flat
from models.amenity import Amenity
from sqlalchemy import text


def init_postgres_database():
    """Initialize PostgreSQL database safely."""

    try:
        with app.app_context():

            print("Testing database connection...")

            db.session.execute(text("SELECT 1"))
            print("Database connection successful!")

            print("Creating database tables...")

            db.create_all()

            print("Tables created/verified successfully!")

            # --------------------------------
            # 1. Create admin if not exists
            # --------------------------------

            admin_email = "admin@flatera.com"

            existing_admin = User.query.filter_by(
                email=admin_email
            ).first()

            if not existing_admin:

                admin_password = os.environ.get("ADMIN_PASSWORD")

                if not admin_password:
                    raise ValueError(
                        "ADMIN_PASSWORD environment variable is missing"
                    )

                print("Creating admin user...")

                admin_user = User(
                    name="Flatera Admin",
                    email=admin_email,
                    role="admin"
                )

                admin_user.set_password(admin_password)

                db.session.add(admin_user)
                db.session.commit()

                print("Admin user created successfully!")

            else:
                print("Admin user already exists. Skipping.")

            # --------------------------------
            # 2. Create amenities if missing
            # --------------------------------

            amenities_data = [
                ("Parking", "Secure covered parking for residents and visitors"),
                ("Gym", "24/7 fitness center with modern equipment"),
                ("Swimming Pool", "Olympic size swimming pool with lifeguard"),
                ("Club House", "Community gathering space for events and parties"),
                ("Power Backup", "24/7 generator backup for all apartments"),
                ("Security", "24/7 CCTV surveillance and security personnel"),
                ("Elevator", "High-speed elevators with backup power"),
                ("Water Supply", "24/7 water supply with purification system"),
                ("Gas Connection", "Piped gas connection for cooking"),
                ("Intercom", "Video intercom system for security"),
                ("Garden", "Landscaped garden with walking paths"),
                ("Play Area", "Children's play area with safety equipment")
            ]

            existing_amenities = {
                amenity.name for amenity in Amenity.query.all()
            }

            for name, description in amenities_data:

                if name not in existing_amenities:

                    db.session.add(
                        Amenity(
                            name=name,
                            description=description
                        )
                    )

            db.session.commit()

            print("Amenities initialized successfully!")

            # --------------------------------
            # 3. Create towers if missing
            # --------------------------------

            tower_names = [
                "Tower A",
                "Tower B",
                "Tower C",
                "Tower D",
                "Tower E",
                "Tower F"
            ]

            existing_towers = {
                tower.name for tower in Tower.query.all()
            }

            for name in tower_names:

                if name not in existing_towers:

                    db.session.add(
                        Tower(name=name)
                    )

            db.session.commit()

            print("Towers initialized successfully!")

            # --------------------------------
            # 4. Create flats if missing
            # --------------------------------

            towers = Tower.query.filter(
                Tower.name.in_(["Tower A", "Tower B", "Tower C"])
            ).all()

            existing_flats = {
                flat.flat_no for flat in Flat.query.all()
            }

            for tower in towers:

                for floor in range(1, 6):

                    for unit in range(1, 4):

                        flat_no = f"{tower.name}-{floor:02d}{unit:02d}"

                        if flat_no in existing_flats:
                            continue

                        bedrooms = (
                            2 if unit == 1 else
                            3 if unit == 2 else 4
                        )

                        sqft = (
                            1200 if unit == 1 else
                            1800 if unit == 2 else 2400
                        )

                        rent = 25000 + (floor * 1000) + (unit * 5000)

                        flat = Flat(
                            flat_no=flat_no,
                            bedrooms=bedrooms,
                            sqft=sqft,
                            rent=rent,
                            tower_id=tower.id,
                            is_available=True,
                            floor=floor,
                            description=(
                                f"Spacious {bedrooms}BHK flat in "
                                f"{tower.name} on floor {floor} "
                                "with modern amenities and excellent ventilation."
                            ),
                            features=(
                                "Parking,24/7 Security,Power Backup,"
                                "Gym,Swimming Pool,"
                                f"{'Garden' if floor == 1 else 'Balcony'}"
                            )
                        )

                        db.session.add(flat)

                        existing_flats.add(flat_no)

            db.session.commit()

            print("Flats initialized successfully!")

            # --------------------------------
            # 5. Final summary
            # --------------------------------

            print("\nDatabase initialization completed!")

            print(f"Admins: {User.query.filter_by(role='admin').count()}")
            print(f"Towers: {Tower.query.count()}")
            print(f"Amenities: {Amenity.query.count()}")
            print(f"Flats: {Flat.query.count()}")

    except Exception as e:

        db.session.rollback()

        print(f"Database initialization failed: {str(e)}")

        raise


if __name__ == "__main__":
    init_postgres_database()
