import requests

url = "http://127.0.0.1:2020/api/setstatus"

res = requests.post(url, data={
    'test': "NofuihsiSkbsvkbjasjkbasjkvjasdvjl"
},)

print(res.status_code)
print(res.json())