import requests

url = "http://101.200.45.55:6800/schedule.json"
parmas = {"project":"onylady","spider":"wylady"}
resp = requests.post(url,parmas)
print(resp.text)
