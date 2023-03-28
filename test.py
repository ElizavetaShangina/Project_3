import requests

print(requests.post("http://127.0.0.1:5000/users", json={
    "name": "first",
    "password": "1"
}).json())
print(requests.post("http://127.0.0.1:5000/users", json={
    "name": "firstt",
    "password": "1"
}).json())
print(requests.post("http://127.0.0.1:5000/users", json={
    "name": "first",
    "password": "hello"
}).json())
print(requests.post("http://127.0.0.1:5000/users", json={
    "name": "first"
}).json())