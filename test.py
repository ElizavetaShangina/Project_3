import requests

print(requests.post("http://127.0.0.1:5000/ending", json={
    "user_id": 1,
    "ending_id": 1,
    "rating": 99.9
}).url)