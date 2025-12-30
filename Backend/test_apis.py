import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_api_endpoint(method, endpoint, data=None, headers=None, expected_status=200):
    """Test an API endpoint and return the response"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, json=data, headers=headers)
        
        print(f"\n{method.upper()} {endpoint}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == expected_status:
            print("✅ PASSED")
        else:
            print("❌ FAILED")
            
        try:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response: {response.text}")
            
        return response
        
    except requests.exceptions.ConnectionError:
        print(f"❌ CONNECTION ERROR: Could not connect to {url}")
        print("Make sure the Flask server is running on port 5000")
        return None
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None

def run_api_tests():
    """Run comprehensive API tests"""
    print("🚀 Starting API Tests...")
    print("=" * 50)
    
    # Test variables
    admin_token = None
    user_token = None
    tower_id = None
    flat_id = None
    
    # 1. Test user registration
    print("\n📝 TESTING USER REGISTRATION")
    test_user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpass123",
        "role": "user"
    }
    response = test_api_endpoint('POST', '/auth/register', test_user_data, expected_status=201)
    
    # 2. Test admin login
    print("\n🔐 TESTING ADMIN LOGIN")
    admin_login_data = {
        "email": "admin@flatera.com",
        "password": "admin123",
        "role": "admin"
    }
    response = test_api_endpoint('POST', '/auth/login', admin_login_data)
    if response and response.status_code == 200:
        admin_token = response.json().get('access_token')
        print(f"Admin token obtained: {admin_token[:50]}...")
    
    # 3. Test user login
    print("\n🔐 TESTING USER LOGIN")
    user_login_data = {
        "email": "testuser@example.com",
        "password": "testpass123",
        "role": "user"
    }
    response = test_api_endpoint('POST', '/auth/login', user_login_data)
    if response and response.status_code == 200:
        user_token = response.json().get('access_token')
        print(f"User token obtained: {user_token[:50]}...")
    
    # Headers for authenticated requests
    admin_headers = {'Authorization': f'Bearer {admin_token}'} if admin_token else None
    user_headers = {'Authorization': f'Bearer {user_token}'} if user_token else None
    
    # 4. Test public endpoints
    print("\n🌐 TESTING PUBLIC ENDPOINTS")
    test_api_endpoint('GET', '/public/towers')
    test_api_endpoint('GET', '/public/flats')
    test_api_endpoint('GET', '/public/amenities')
    
    # 5. Test admin endpoints (if admin token available)
    if admin_headers:
        print("\n👑 TESTING ADMIN ENDPOINTS")
        
        # Get towers
        response = test_api_endpoint('GET', '/admin/towers', headers=admin_headers)
        if response and response.status_code == 200:
            towers = response.json()
            if towers:
                tower_id = towers[0]['id']
        
        # Create a new tower
        new_tower_data = {"name": "Test Tower"}
        test_api_endpoint('POST', '/admin/towers', new_tower_data, headers=admin_headers, expected_status=201)
        
        # Get flats
        response = test_api_endpoint('GET', '/admin/flats', headers=admin_headers)
        if response and response.status_code == 200:
            flats = response.json()
            if flats:
                flat_id = flats[0]['id']
        
        # Create a new flat (if we have a tower_id)
        if tower_id:
            new_flat_data = {
                "flat_no": "TEST-001",
                "bedrooms": 2,
                "sqft": 1200,
                "rent": 30000,
                "tower_id": tower_id,
                "is_available": True,
                "description": "Test flat",
                "features": "Parking,Security",
                "floor": 1
            }
            test_api_endpoint('POST', '/admin/flats', new_flat_data, headers=admin_headers, expected_status=201)
        
        # Test amenities
        test_api_endpoint('GET', '/admin/amenities', headers=admin_headers)
        
        # Create new amenity
        new_amenity_data = {
            "name": "Test Amenity",
            "description": "This is a test amenity"
        }
        test_api_endpoint('POST', '/admin/amenities', new_amenity_data, headers=admin_headers, expected_status=201)
        
        # Get bookings
        test_api_endpoint('GET', '/admin/bookings', headers=admin_headers)
        
        # Get tenants
        test_api_endpoint('GET', '/admin/tenants', headers=admin_headers)
    
    # 6. Test user booking (if user token and flat available)
    if user_headers and flat_id:
        print("\n📋 TESTING USER BOOKING")
        test_api_endpoint('POST', f'/public/book/{flat_id}', headers=user_headers, expected_status=201)
        test_api_endpoint('GET', '/public/bookings', headers=user_headers)
    
    print("\n" + "=" * 50)
    print("🏁 API Tests Completed!")
    print("\nTo run these tests:")
    print("1. Make sure your Flask server is running: python app.py")
    print("2. Run this test script: python test_apis.py")

if __name__ == "__main__":
    run_api_tests()