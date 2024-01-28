import time
import requests

i=0

while i in range(50):
    lat = -86.784
    long = 36.165
    date = "2024-01-17 11:06:18"

    data = {
        'latitude' : lat+i/100,
        'longitude' : long,
        'date':date,
        'ip':"127.0.0.127"
    }

    data2 = {
        'latitude' : lat+i/100,
        'longitude' : long+i/100,
        'date':date,
        'ip':"18.0.0.18"
    }

    response = requests.post('http://localhost:8000/coordonnees', json=data)
    print(response.status_code)
    time.sleep(2)

    response = requests.post('http://localhost:8000/coordonnees', json=data2)
    print(response.status_code)
    time.sleep(2)

    i+=1
print('fini')