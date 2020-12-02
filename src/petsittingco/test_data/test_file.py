import requests

r = requests.get("http://petinfo.json")#/petinfo?id=1&pet_id=1&auth=1
r.status_code
r.json