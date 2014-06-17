import yaml
import debug


class Config:
    data = None
    config_file = None

    def __init__(self, config_file="../config.yaml"):
        self.config_file = config_file

    def load(self):
        debug.message("Reading config")
        try:
            with open(self.config_file, "r") as file:
                self.data = yaml.load(file.read())

        except Exception, e:
            debug.exception("Exception while reading config", e)


    def get(self, key):
        if self.data is None:
            self.load()

        try:
            return self.data[key]
        except Exception, e:
            debug.exception("Key does not exist in config: %s" % key, e)

    def all(self):
        if self.data is None:
            self.load()

        return self.data