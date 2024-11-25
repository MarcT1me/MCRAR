import requests

mods = {
    "Create": "https://www.curseforge.com/minecraft/mc-mods/create/files"
}

for name, url in mods.items():
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Request Error {response.status_code}")
