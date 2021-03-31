import json

def get_key_from_json(key: str):
    with open('keys.json', 'r+') as file:
        data = json.load(file)
    return data[key]

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()
def temp_ban():
    pass