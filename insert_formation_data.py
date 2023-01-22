from data import SqliteConnection
from spreadsheet.connect_sheet import OperateSpreadSheet


if __name__ == "__main__":
    SqliteConnection.set_connection()
    formation_data = OperateSpreadSheet.get_formation_data()
    for data in formation_data:
        stage, player, weapon = data
        SqliteConnection.register_formation("ガチエリア", stage, player, weapon)
