import requests
import json

# urlはデプロイの度に変更すること
# アクセスできるユーザーは全員で設定すること
class PostGasScript:
    url = "https://script.google.com/macros/s/AKfycbyxIo16BRnHjzwChvGuBPL5bzhOqKjNl-ir6OIgxzwygitJD8tZk9OZYhygpwATfKW1/exec"
    headers = {"Content-Type": "application/json"}

    @classmethod
    def post(cls, type, data=""):
        payload = {"type": type, "data": data}
        response = requests.post(cls.url, data=json.dumps(payload), headers=cls.headers)
        if response.status_code == "200" and response.text != "fail":
            return True
        else:
            return False
