from data import SqliteConnection
from spreadsheet.connect_sheet import OperateSpreadSheet


if __name__ == "__main__":
    SqliteConnection.set_connection()
    data = OperateSpreadSheet.get_recently_data()
    print(data)
