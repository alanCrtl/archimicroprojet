import time
import requests

i=0

while i in range(50):
    lat = -86.784
    long = 36.165
    date = "2024-01-17 11:06:18"

    data = {
        'latitude' : lat+i/1000,
        'longitude' : long,
        'date':date,
        'ip':"127.0.0.127"
    }


    response = requests.post('http://localhost:8000/coordonnees', json=data)
    print(response.status_code)
    time.sleep(2)

    i+=1
print('fini')