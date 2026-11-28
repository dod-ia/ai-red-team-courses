import os
import urllib.request

url = "https://httpbin.org/headers"

req = urllib.request.Request(
    url,
    headers={"Authorization": f"Bearer {os.environ['MY_VALUE']}"}
)

print("Request:", req.full_url)
print("Method:", req.get_method())
print("Headers:", {k: v for k, v in req.header_items()})

with urllib.request.urlopen(req) as response:
    print("Status:", response.status)
    print("Body:", response.read().decode())
