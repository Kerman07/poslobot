import requests
import json

baseUrl = "https://chatapi.viber.com/pa/send_message"

content = {
    "receiver": "SVDRnk/HlrP/FI/66iUW1w==",
    "min_api_version": 1,
    "sender": {"name": "poslovni_bot", "avatar": "http://avatar.example.com"},
    "tracking_data": "tracking data",
    "type": "url",
    "media": "https://www.mojposao.ba/#!job;t=database-administrator-raiffeisen-bank-dd-bosna-i-hercegovina-sarajevo;id=474431",
}

headers = {
    "X-Viber-Auth-Token": "4ec6da36b227dc6f-cfe43ef1fe4c9487-2930ff0d897e15ca",
}

if __name__ == "__main__":
    r = requests.post(baseUrl, json.dumps(content), headers=headers)
    print(r.json())
