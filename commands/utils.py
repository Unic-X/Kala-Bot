import json
import re

def get_key_from_json(key: str):
    with open('keys.json', 'r+') as file:
        data = json.load(file)
    return data[key]


async def fetch(session, url,params=None):
    if params==None:
            async with session.get(url) as response:
                return await response.json()
    else:
        async with session.get(url,params=params) as response:
            return await response.json()


def temp_ban(userid):
    with open('commands\\banned.json', 'r') as file:
        json_data = json.load(file)
        if userid not in json_data["banned"]:
            json_data["banned"].append(userid)
    with open('commands\\banned.json', 'w') as file:
        json.dump(json_data, file, indent=2)

def to_dict(string):
    argumented_list=re.split('; |, |\*|\s|\n',re.sub(' +', ' ',string))
    a={}
    for e in argumented_list:
        if len(e)>1:
            sub_list=e.split("=")
            a[sub_list[0]]=sub_list[1]  #key

    return a