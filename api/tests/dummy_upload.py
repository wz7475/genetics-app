import requests

url = "http://127.0.0.1:8080/uploadfile"

files = {'file': ('test.txt', open('data/brca.csv', 'rb'))}

response = requests.post(url, files=files)

print(response.status_code)
