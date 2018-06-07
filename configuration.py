import json

DEFAULTS = {

}


class Configuration(object):
    @classmethod
    def from_json(cls, folder):
        with open(folder + '/configuration.json', "a+") as json_file:
            configurations = json.load(json_file)

        return cls(configurations)

    def __init__(self, **configurations):
        self.configurations = {}

        for key, value in configurations.iteritems():
            self.configurations[key] = value

        for key, value in DEFAULTS.iteritems():
            if key not in self.configurations:
                self.configurations[key] = value

    def __getattr__(self, name):
        try:
            return self.configurations[name]
        except KeyError:
            raise AttributeError

    def __setattr__(self, name, value):
        if name == "configurations":
            object.__setattr__(self, name, value)
        else:
            self.configurations[name] = value

    def store(self, folder):
        with open(folder + '/configuration.json', "a+") as json_file:
            json.dump(self.configurations, json_file)
