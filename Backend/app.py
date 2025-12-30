from flask import Flask, jsonify
from config import Config
from extensions import db, Marshmallow, bcrypt, jwt
from routes.auth_routes  import auth_bp
from routes.public_routes import public_bp
from routes.admin_routes import admin_bp
from flask_cors import CORS
from models.user import User

app=Flask(__name__)
CORS(app, origins=["*"], supports_credentials=True)
app.config.from_object(Config)
           
db.init_app(app)
Marshmallow.init_app(app)   
bcrypt.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth_bp,url_prefix='/auth')
app.register_blueprint(public_bp,url_prefix='/public')
app.register_blueprint(admin_bp,url_prefix='/admin')

# Health check endpoint
@app.route('/health')
def health_check():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "message": "Flatera Backend API is running"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 500

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Flatera Backend API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "auth": "/auth/*",
            "public": "/public/*",
            "admin": "/admin/*"
        }
    })

def create_default_admin():
    admin_email = "admin@flatera.com"
    admin_password = "admin123"
    
    existing_admin = User.query.filter_by(email=admin_email).first()
    if not existing_admin:
        admin_user = User(
            name="Flatera Admin",
            email=admin_email,
            role="admin"
        )
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        db.session.commit()
        print("Default admin user created successfully!")
        print(f"Email: {admin_email}")
        print(f"Password: {admin_password}")
    else:
        print("Admin user already exists!")

if __name__=="__main__":
    with app.app_context():
        db.create_all()
        create_default_admin()
    app.run(debug=True)