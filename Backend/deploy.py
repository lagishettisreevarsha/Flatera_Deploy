#!/usr/bin/env python3
"""
Deployment script for Flatera Backend
This script helps deploy the application to various platforms
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr}")
        return False

def deploy_docker():
    """Deploy using Docker Compose"""
    print("🐳 Deploying with Docker Compose...")
    
    # Build and start containers
    if run_command("docker-compose down", "Stopping existing containers"):
        if run_command("docker-compose up --build -d", "Building and starting containers"):
            print("✅ Docker deployment successful!")
            print("🌐 API should be available at: http://localhost:5000")
            return True
    return False

def deploy_local():
    """Deploy locally for development"""
    print("💻 Starting local development server...")
    
    # Install requirements
    if run_command("pip install -r requirements.txt", "Installing requirements"):
        print("🚀 Starting server...")
        print("   Run: python start_server.py")
        print("🌐 API will be available at: http://localhost:5000")
        return True
    return False

def deploy_render():
    """Instructions for Render deployment"""
    print("☁️ Render Deployment Instructions:")
    print("=" * 50)
    print("1. Push your code to GitHub")
    print("2. Go to render.com and create a new Web Service")
    print("3. Connect your GitHub repository")
    print("4. Use these settings:")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: python production_start.py")
    print("   - Environment Variables:")
    print("     DATABASE_URL=postgresql://neondb_owner:npg_P2UoA0aeiwbk@ep-rough-glade-adze8iu4-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
    print("     SECRET_KEY=your-secret-key-here")
    print("     JWT_SECRET_KEY=your-jwt-secret-here")
    print("     PORT=5000")
    print("5. Deploy!")

def main():
    """Main deployment function"""
    print("🚀 Flatera Backend Deployment Tool")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage: python deploy.py [docker|local|render|help]")
        print("\nOptions:")
        print("  docker  - Deploy using Docker Compose")
        print("  local   - Set up local development environment")
        print("  render  - Show Render deployment instructions")
        print("  help    - Show this help message")
        return
    
    option = sys.argv[1].lower()
    
    if option == "docker":
        deploy_docker()
    elif option == "local":
        deploy_local()
    elif option == "render":
        deploy_render()
    elif option == "help":
        print("Flatera Backend Deployment Options:")
        print("=" * 40)
        print("🐳 Docker: Full containerized deployment")
        print("💻 Local: Development server setup")
        print("☁️ Render: Cloud deployment instructions")
    else:
        print(f"❌ Unknown option: {option}")
        print("Use 'python deploy.py help' for available options")

if __name__ == "__main__":
    main()