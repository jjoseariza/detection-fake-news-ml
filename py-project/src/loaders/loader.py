from src.loaders.local_loader import LocalLoader
from src.loaders.blob_loader import BlobLoader


class Loader:
    def __init__(self, loader_name):
        self.loader_name = loader_name
        if self.loader_name == "local_loader":
            self.loader = LocalLoader()
        if self.loader_name == "blob_loader":
            self.loader = BlobLoader()

    def load_data(self):
        assert self.loader is not None, "Loader not supported"
        return self.loader.load_data()
