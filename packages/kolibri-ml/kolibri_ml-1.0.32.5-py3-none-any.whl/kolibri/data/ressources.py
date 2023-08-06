import os, logging
from kolibri.settings import DATA_PATH, _repo
from kolibri.data.auto_downloader import DownloaderBase
from kolibri import settings



LOGGER = logging.getLogger(__name__)

class Ressources(DownloaderBase):

    def __init__(self):
        """

        """
        super().__init__(
            download_dir=DATA_PATH)


    def get(self, resource_path, external_url=None):
        self.download(resource_path, external_url=external_url)
        self.path=os.path.join(DATA_PATH, resource_path)

        return self

    def list_directory_content(self, directory):
        return [f.name for f in settings._repo.get_contents(os.path.join("data", directory))]


resources=Ressources()