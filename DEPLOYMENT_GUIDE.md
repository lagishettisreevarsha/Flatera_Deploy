# Flatera Backend Deployment Guide

## 🏠 Apartment Rental System - Backend API

### Database Migration: SQLite → PostgreSQL ✅

Your backend has been successfully configured to use PostgreSQL (Neon Database).

---

## 📋 API Endpoints Summary

### Authentication (`/auth`)
- `POST /auth/register` - User registration
- `POST /auth/login` - User login with JWT token

### Public Endpoints (`/public`)
- `GET /public/towers` - List all towers
- `GET /public/flats` - List all flats
- `GET /public/flats/<id>` - Get flat details
- `GET /public/amenities` - List amenities
- `GET /public/tower/<id>/flats` - Get flats by tower
- `POST /public/book/<id>` - Book a flat (requires JWT)
- `GET /public/bookings` - Get user bookings (requires JWT)

### Admin Endpoints (`/admin`)
- `GET /admin/bookings` - Get all bookings
- `POST /admin/booking/<id>/approve` - Approve booking
- `POST /admin/booking/<id>/decline` - Decline booking
- `GET/POST/PUT/DELETE /admin/towers` - Tower management
- `GET/POST/PUT/DELETE /admin/flats` - Flat management
- `GET/POST/PUT/DELETE /admin/amenities` - Amenity management
- `GET /admin/tenants` - Get approved tenants

---

## 🚀 Local Development

### Option 1: Direct Python
```bash
cd Backend
pip install -r requirements.txt
python start_server.py
```

### Option 2: Docker Compose
```bash
docker-compose up --build
```

### Test APIs
```bash
cd Backend
python test_apis.py
```

**Default Admin Credentials:**
- Email: `admin@flatera.com`
- Password: `admin123`

---

## ☁️ Google Cloud Platform Deployment

### Prerequisites
1. Install Google Cloud SDK
2. Create a GCP project
3. Enable App Engine API

### Deploy to App Engine
```bash
cd Backend
gcloud app deploy app.yaml
```

### Environment Variables (Update in app.yaml)
```yaml
env_variables:
  DATABASE_URL: "your-postgresql-connection-string"
  SECRET_KEY: "your-production-secret-key"
  JWT_SECRET_KEY: "your-jwt-secret-key"
```

---

## 🔧 Configuration Files Updated

### ✅ Backend/config.py
- PostgreSQL connection string
- Environment variable support
- Production-ready configuration

### ✅ Backend/requirements.txt
- Added `psycopg2-binary` for PostgreSQL
- All dependencies updated

### ✅ Backend/Dockerfile
- PostgreSQL system dependencies
- Database initialization on startup
- Production-ready container

### ✅ docker-compose.yaml
- PostgreSQL environment variables
- Removed SQLite volume dependency

---

## 🧪 Testing

### API Test Results
Run `python test_apis.py` to verify:
- ✅ User registration/login
- ✅ Admin authentication
- ✅ Public endpoints (towers, flats, amenities)
- ✅ Admin CRUD operations
- ✅ Booking workflow
- ✅ JWT token validation

---

## 🔒 Security Features

- **Password Hashing**: bcrypt with salt
- **JWT Authentication**: Role-based access control
- **CORS**: Configured for frontend integration
- **Input Validation**: Marshmallow schemas
- **SQL Injection Protection**: SQLAlchemy ORM

---

## 📊 Database Schema

### Models
- **User**: Authentication and roles
- **Tower**: Building/complex management
- **Flat**: Individual apartment units
- **Booking**: Rental requests and approvals
- **Amenity**: Building facilities

### Relationships
- Tower → Flats (One-to-Many)
- User → Bookings (One-to-Many)
- Flat → Bookings (One-to-Many)

---

## 🚨 Production Checklist

- [x] PostgreSQL database connection
- [x] Environment variables for secrets
- [x] Docker containerization
- [x] GCP App Engine configuration
- [x] API testing suite
- [x] Database initialization script
- [ ] SSL/HTTPS configuration
- [ ] Rate limiting
- [ ] Logging and monitoring
- [ ] Backup strategy

---

## 📞 Support

For issues or questions:
1. Check API test results: `python test_apis.py`
2. Verify database connection in logs
3. Ensure all environment variables are set
4. Check GCP deployment logs: `gcloud app logs tail -s default`

**Your backend is now ready for production deployment! 🎉**