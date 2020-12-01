import requests

r = requests.get("http://petinfo.json")
r.status_code
r.json