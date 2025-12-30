#!/usr/bin/env python3
"""
Quick test script to check if the API is working
"""
import requests
import json

def test_api(base_url="http://localhost:5000"):
    """Test basic API endpoints"""
    print(f"🧪 Testing API at {base_url}")
    print("=" * 50)
    
    try:
        # Test health endpoint
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print("   ❌ Health check failed")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False
    
    try:
        # Test home endpoint
        print("\n2. Testing home endpoint...")
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Home endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print("   ❌ Home endpoint failed")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
    
    try:
        # Test public towers endpoint
        print("\n3. Testing public towers endpoint...")
        response = requests.get(f"{base_url}/public/towers", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            towers = response.json()
            print(f"   ✅ Found {len(towers)} towers")
            if towers:
                print(f"   First tower: {towers[0]}")
        else:
            print("   ❌ Towers endpoint failed")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
    
    try:
        # Test admin login
        print("\n4. Testing admin login...")
        login_data = {
            "email": "admin@flatera.com",
            "password": "admin123",
            "role": "admin"
        }
        response = requests.post(f"{base_url}/auth/login", json=login_data, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Admin login successful")
            token = response.json().get('access_token')
            print(f"   Token: {token[:50]}..." if token else "   No token received")
        else:
            print("   ❌ Admin login failed")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Quick test completed!")
    
    return True

if __name__ == "__main__":
    import sys
    
    # Allow custom URL as command line argument
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    test_api(base_url)