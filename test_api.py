import requests
import json

# API base URL (change this to your server URL when deployed)
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("Health Check Response:")
        print(json.dumps(response.json(), indent=2))
        print(f"Status Code: {response.status_code}")
        print("-" * 50)
    except Exception as e:
        print(f"Error testing health check: {e}")

def test_contact_form():
    """Test the contact form submission"""
    contact_data = {
        "email": "test@example.com",
        "topic": "Project Inquiry",
        "message": "Hi, I'm interested in working with you on a new project. Can we discuss this further?"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/contact", json=contact_data)
        print("Contact Form Response:")
        print(json.dumps(response.json(), indent=2))
        print(f"Status Code: {response.status_code}")
        print("-" * 50)
    except Exception as e:
        print(f"Error testing contact form: {e}")

def test_get_contacts():
    """Test getting all contact submissions"""
    try:
        response = requests.get(f"{BASE_URL}/contacts")
        print("Get Contacts Response:")
        print(json.dumps(response.json(), indent=2))
        print(f"Status Code: {response.status_code}")
        print("-" * 50)
    except Exception as e:
        print(f"Error testing get contacts: {e}")

if __name__ == "__main__":
    print("Testing Portfolio Contact API")
    print("=" * 50)
    
    test_health_check()
    test_contact_form()
    test_get_contacts() 
