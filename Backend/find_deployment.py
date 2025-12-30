#!/usr/bin/env python3
"""
Script to help find and test your deployed API
"""
import requests
import json

def test_deployment_urls():
    """Test common deployment URLs"""
    
    # Common deployment patterns
    possible_urls = [
        "https://flatera-backend.onrender.com",
        "https://flatera-backend-app.herokuapp.com", 
        "https://flatera.herokuapp.com",
        "https://flatera-api.herokuapp.com",
        "http://localhost:5000",
        "https://your-app-name.appspot.com",  # GCP App Engine
    ]
    
    print("🔍 Searching for your deployed API...")
    print("=" * 60)
    
    for url in possible_urls:
        try:
            print(f"\n🌐 Testing: {url}")
            response = requests.get(f"{url}/health", timeout=5)
            
            if response.status_code == 200:
                print(f"   ✅ FOUND! API is running at {url}")
                print(f"   Response: {response.json()}")
                
                # Test a few more endpoints
                print(f"\n   Testing more endpoints...")
                
                # Test home
                try:
                    home_response = requests.get(url, timeout=5)
                    if home_response.status_code == 200:
                        print(f"   ✅ Home endpoint working")
                except:
                    print(f"   ❌ Home endpoint failed")
                
                # Test towers
                try:
                    towers_response = requests.get(f"{url}/public/towers", timeout=5)
                    if towers_response.status_code == 200:
                        towers = towers_response.json()
                        print(f"   ✅ Towers endpoint working - {len(towers)} towers found")
                    else:
                        print(f"   ❌ Towers endpoint failed - Status: {towers_response.status_code}")
                except Exception as e:
                    print(f"   ❌ Towers endpoint error: {e}")
                
                return url
                
            else:
                print(f"   ❌ Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Connection failed: {type(e).__name__}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n❌ Could not find your deployed API")
    print(f"\nℹ️  If your app is deployed, please provide the URL")
    print(f"   Example: python quick_test.py https://your-app-url.com")
    
    return None

if __name__ == "__main__":
    found_url = test_deployment_urls()
    
    if found_url:
        print(f"\n🎉 SUCCESS! Your API is accessible at: {found_url}")
        print(f"\n📋 Next steps:")
        print(f"   1. Test all endpoints: python test_apis.py {found_url}")
        print(f"   2. Update your frontend to use: {found_url}")
        print(f"   3. Admin login: admin@flatera.com / admin123")
    else:
        print(f"\n🚀 To deploy your app:")
        print(f"   Docker: docker-compose up --build")
        print(f"   Local: python start_server.py")
        print(f"   GCP: gcloud app deploy app.yaml")