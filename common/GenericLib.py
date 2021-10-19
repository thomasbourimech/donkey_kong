import json


class GenericLib:

    @staticmethod
    def load_json_conf(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        return json.loads(file_content)