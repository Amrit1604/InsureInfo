import requests
import json

def test_quota_fix():
    url = "http://localhost:8000/hackrx/run"
    data = {
        "documents": "policy documents loaded from system",
        "questions": [
            "My friend needs medical emergency, his foot ligament got tore, he has 3 months old insurance, he is 20 years old from panchkula"
        ]
    }

    try:
        response = requests.post(url, json=data, timeout=30)
        print("Status Code:", response.status_code)
        print("Response:", json.dumps(response.json(), indent=2))
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    test_quota_fix()
