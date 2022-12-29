import gspread
from data.ResultData import ResultData
from oauth2client.service_account import ServiceAccountCredentials

# スプレッドシート操作用クラス
class OperateSpreadSheet:
    # use creds to create a client to interact with the Google Drive API
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "client_secret.json", scope
    )
    client = gspread.authorize(creds)

    SHEET_KEY = "11lWvKtezKWysVDQqUETCATKt7guVgAZ7jDV7rD-AomU"

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open_by_key(SHEET_KEY).worksheet("入力")

    # TODO 更新処理未完成
    @classmethod
    def set_result_data(cls):
        result = ResultData.get_result()
        sheet_data: list[list[any]] = cls.sheet.get_values("B9:B22")
        update_data: list[list[any]] = []
        for array in sheet_data:
            values = result[array[0]]
            update_data.append(values)

        # print(update_data)
        cls.sheet.update("C9", update_data)
