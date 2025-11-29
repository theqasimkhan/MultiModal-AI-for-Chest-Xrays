import requests
import json
import os

# Configuration
API_URL = "http://127.0.0.1:5000/analyze"
IMAGE_PATH = r"C:\Users\Qasim Khan\.gemini\antigravity\brain\93f81db4-850c-42cc-b555-1d727f9c06e4\chest_xray_sample_1764268566438.png"

def test_analyze():
    print(f"Testing API at {API_URL}")
    print(f"Using image: {IMAGE_PATH}")
    
    if not os.path.exists(IMAGE_PATH):
        print("Error: Image file not found!")
        return

    payload = {
        "image_path": IMAGE_PATH,
        "clinical_indication": "Shortness of breath",
        "date": "2025-11-27"
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("\nAnalysis Results:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("\nError Response:")
            print(response.text)
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_analyze()
