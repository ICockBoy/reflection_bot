import json


class DataBase:
    dbFile: str = "Database\\data.json"

    def __init__(self):
        with open(self.dbFile, "r") as file:
            self.data = json.load(file)

    def getUsrInfo(self, id_) -> int:
        return self.data[str(id_)]

    def setUsrInfo(self, id_, info: int) -> None:
        self.data[str(id_)] = info
        with open(self.dbFile, "w") as file:
            json.dump(self.data, file)