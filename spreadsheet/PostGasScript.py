import requests
import json

# TODO # doPostを追加する
# urlはデプロイの度に変更すること
class PostGasScript:
    url = "https://script.google.com/macros/s/AKfycbz0CfY5cbw4aydZ_dHzqJgEVOaiZ2RW-evNzRN3IoVArxq-3dKhFEXVFWA9aCX8Sk0n5w/exec"
    headers = {"Content-Type": "application/json"}

    @classmethod
    def post(cls, type, data=""):
        payload = {"type": type, "data": data}
        response = requests.post(cls.url, data=json.dumps(payload), headers=cls.headers)
        if response.status_code == "200" and response.text == "success":
            return True
        else:
            return False
