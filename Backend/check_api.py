import requests
import sys

def check_api(url):
    print(f"Testing API at: {url}")
    
    try:
        # Test health endpoint
        response = requests.get(f"{url}/health", timeout=10)
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print("✅ API is responding")
            return True
        else:
            print("❌ API returned error")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    check_api(url)