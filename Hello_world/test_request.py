import requests

r = requests.get("http://127.0.0.1:8000/about")
print(r.json())
print(r.status_code)
print(r.headers)
print(r.text)