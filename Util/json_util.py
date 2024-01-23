import json


class OperationJson:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.read_json_data()

    def read_json_data(self):
        with open(self.file_path, encoding='utf-8') as f:
            data = json.load(f)
            return data

