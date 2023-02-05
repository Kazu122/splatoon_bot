import datetime as dt
import os
from dotenv import load_dotenv
import gspread
from gspread import utils
from data import SqliteConnection
from data.ResultData import ResultData
from oauth2client.service_account import ServiceAccountCredentials
from spreadsheet.client_secret import secret_json

# スプレッドシート操作用クラス
class OperateSpreadSheet:
    # use creds to create a client to interact with the Google Drive API
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        secret_json,
        scope,
    )
    client = gspread.authorize(creds)

    SHEET_KEY = "11lWvKtezKWysVDQqUETCATKt7guVgAZ7jDV7rD-AomU"

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open_by_key(SHEET_KEY).worksheet("入力")
    formation_sheet = client.open_by_key(SHEET_KEY).worksheet("武器編成")
    totalizeSheet = client.open_by_key(SHEET_KEY).worksheet("集計")
    termTotalizeSheet = client.open_by_key(SHEET_KEY).worksheet("期間集計")

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

    # 編成データを取得する
    @classmethod
    def get_formation_data(cls):
        stage_data = SqliteConnection.get_stage_data()
        stage_num = len(stage_data)
        sheet_data: list[list[any]] = cls.formation_sheet.get_values(
            f"B5:D{stage_num * 4 + 4}"
        )
        stage = None
        for data in sheet_data:
            if data[0] != "":
                stage = data[0]
            else:
                data[0] = stage
        return sheet_data

    # 集計データを取得する
    @classmethod
    def get_all_term_data(cls):
        stage_data = SqliteConnection.get_stage_data()
        stage_num = len(stage_data)
        sheet_data: list[list[any]] = cls.totalizeSheet.get_values(
            f"B5:E{stage_num + 4}"
        )
        return sheet_data

    # 今月の勝率を取得
    @classmethod
    def get_recently_data(cls):
        try:
            stage_data = SqliteConnection.get_stage_data()
            stage_num = len(stage_data)
            most_old_month = dt.datetime.strptime(
                cls.termTotalizeSheet.cell(4, 3).value, "%Y/%m"
            )
            now = dt.datetime.now()
            diff = (
                (now.year - most_old_month.year) * 12 + now.month - most_old_month.month
            )
            head = cls.termTotalizeSheet.cell(4, 3 + diff)
            if head == "":
                return None
            start = cls.termTotalizeSheet.cell(5, 3 + diff).address
            end = cls.termTotalizeSheet.cell(stage_num + 4, 3 + diff).address
            range = f"{start}:{end}"
            sheet_data: list[list[any]] = cls.totalizeSheet.get_values(f"{range}")
            if len(sheet_data) == 0:
                return None
            return sheet_data
        except:
            return None
