import requests

url = "http://localhost:8080/uploadfile"

files = {'file': ('test.txt', open('D:\\nauka\\studia\\SEM5\\PZSP2\\kod\\genetics-app\\docs\\container.png', 'rb'))}

response = requests.post(url, files=files)

print(response.status_code)
print(response.json())