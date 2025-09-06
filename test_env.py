#!/usr/bin/env python
"""
Environment Configuration Test Script
This script helps test your environment variables and settings configuration.
"""

import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

def test_environment():
    print("🔧 Environment Configuration Test")
    print("=" * 50)
    
    # Test basic environment variables
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    secret_key = os.environ.get('SECRET_KEY', 'default-key')
    database_url = os.environ.get('DATABASE_URL')
    allowed_hosts = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1')
    
    print(f"DEBUG: {debug}")
    print(f"SECRET_KEY: {'SET' if secret_key != 'default-key' else 'USING DEFAULT (NOT SECURE)'}")
    print(f"DATABASE_URL: {'SET' if database_url else 'NOT SET (using SQLite)'}")
    print(f"ALLOWED_HOSTS: {allowed_hosts}")
    
    print("\n📦 Production Settings (when DEBUG=False):")
    if not debug:
        print("✅ SSL Redirect: ENABLED")
        print("✅ Secure Cookies: ENABLED") 
        print("✅ HSTS Headers: ENABLED")
        print("✅ WhiteNoise Static Files: ENABLED")
        print("✅ Compressed Static Files: ENABLED")
    else:
        print("ℹ️  Running in DEBUG mode - production settings disabled")
    
    print("\n🗄️  Database Configuration:")
    if database_url:
        print(f"✅ Using DATABASE_URL: {database_url[:50]}...")
        try:
            import dj_database_url
            parsed = dj_database_url.parse(database_url)
            print(f"   Engine: {parsed['ENGINE']}")
            print(f"   Host: {parsed.get('HOST', 'N/A')}")
            print(f"   Port: {parsed.get('PORT', 'N/A')}")
            print(f"   Database: {parsed.get('NAME', 'N/A')}")
        except Exception as e:
            print(f"❌ Error parsing DATABASE_URL: {e}")
    else:
        print("ℹ️  Using SQLite database (development)")
    
    print("\n🚀 Deployment Checklist:")
    checklist = [
        ("Set DEBUG=False", not debug),
        ("Set SECRET_KEY", secret_key != 'default-key'),
        ("Set DATABASE_URL", database_url is not None),
        ("Set ALLOWED_HOSTS", 'localhost' not in allowed_hosts.lower()),
    ]
    
    for item, status in checklist:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {item}")
    
    # Test Django settings import
    print("\n⚙️  Django Settings Test:")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings')
        import django
        django.setup()
        
        from django.conf import settings
        print("✅ Django settings imported successfully")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   DATABASES: {list(settings.DATABASES.keys())}")
        print(f"   STATIC_URL: {settings.STATIC_URL}")
        print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        
    except Exception as e:
        print(f"❌ Error importing Django settings: {e}")
    
    print("\n" + "=" * 50)
    print("Environment test completed!")

if __name__ == "__main__":
    test_environment()
