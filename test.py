import requests

date = "2024-12-26"
url = "https://www.nrb.org.np/api/forex/v1/rate"
response = requests.get(url, params={"date": date})

print(response.status_code)
print(response.json())
