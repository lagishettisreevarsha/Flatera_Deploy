class Config:
    SECRET_KEY='super-secret-key'
    SQLALCHEMY_DATABASE_URI='sqlite:///apartment.db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY='jwtsecret'