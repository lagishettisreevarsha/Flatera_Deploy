from flask import Flask
from config import Config
from extensions import db, Marshmallow, bcrypt, jwt
from routes.auth_routes  import auth_bp
from routes.public_routes import public_bp
from routes.admin_routes import admin_bp
from flask_cors import CORS

app=Flask(__name__)
CORS(app,origins=["http://localhost:4200"])
app.config.from_object(Config)
           
db.init_app(app)
Marshmallow.init_app(app)   
bcrypt.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth_bp,url_prefix='/auth')
app.register_blueprint(public_bp,url_prefix='/public')
app.register_blueprint(admin_bp,url_prefix='/admin')

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)