class Config:
    SECRET_KEY='super-secret-key'
    SQLALCHEMY_DATABASE_URI='sqlite:///apartment.db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY='jwtsecret'
    JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour in seconds
    JWT_REFRESH_TOKEN_EXPIRES=86400  # 24 hours in seconds