import pandas
from config import config


class LocalLoader:
    def load_data(self):
        all_data = None
        for data_path in config["local_data_paths"]:
            if data_path["method"] == "load_from_csv":
                data = self.load_from_csv(data_path["path"])
            if all_data is None:
                all_data = data
            all_data = all_data.append(data)

        return all_data

    def load_from_csv(self, path):
        return pandas.read_csv(path)
