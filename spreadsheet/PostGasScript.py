import requests
import json

# urlはデプロイの度に変更すること
# アクセスできるユーザーは全員で設定すること
class PostGasScript:
    url = "https://script.google.com/macros/s/AKfycbzKVNp-A6zqAHbOat1eDEcnAhd6bvUWKAyTEn_kB8MgbNzDqKfn5LMvt7YRUhtH4ZIBEg/exec"
    headers = {"Content-Type": "application/json"}

    # TODO: なぜかfalseが返る、要確認
    @classmethod
    def post(cls, type, data=""):
        payload = {"type": type, "data": data}
        response = requests.post(cls.url, data=json.dumps(payload), headers=cls.headers)
        if response.status_code == "200" and response.text == "success":
            return True
        else:
            return False
