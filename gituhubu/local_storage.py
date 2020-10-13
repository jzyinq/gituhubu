import json
import os

from appdirs import user_cache_dir, user_config_dir

from gituhubu.config import APP_AUTHOR, APP_NAME


class LocalFile:
    def __init__(self, directory, filename):
        self.directory = directory
        self.file_name = filename
        self.file_path = self._prepare_file_path()

    def _prepare_file_path(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        return f"{self.directory}/{self.file_name}"

    def write(self, data):
        with open(self.file_path, "w+") as f:
            f.write(json.dumps(data))
            f.close()

    def read(self):
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r') as f:
                content = f.read()
            return json.loads(content)

        return {}


class ReposCacheFile(LocalFile):
    def __init__(self):
        super().__init__(user_cache_dir(APP_NAME, APP_AUTHOR), 'repos.json')


class ConfigFile(LocalFile):
    def __init__(self):
        super().__init__(user_config_dir(APP_NAME, APP_AUTHOR), 'config.json')
