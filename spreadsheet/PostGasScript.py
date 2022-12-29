import requests
import json

# TODO gas側でactiveSheetをopenByIdに変更する
# doPostを追加する
class PostGasScript:
    url = "https://script.google.com/macros/s/AKfycbzuvpMQR5CaLl4dZkBaFjXk3CwWY4RcN6nb7ywZGRk6PXfkqU8ynOxOslZ4mk0n8g3o0g/exec"
    headers = {"Content-Type": "application/json"}

    @classmethod
    def post(cls, type, data=""):
        payload = {"type": type, "data": data}
        response = requests.post(cls.url, data=json.dumps(payload), headers=cls.headers)
        if response.status_code == "200" and response.text == "success":
            return True
        else:
            return False
