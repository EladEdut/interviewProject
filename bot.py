class Bot:

    def __init__(self, name, provider, display_name, credentials):
        self.name = name
        self.provider = provider
        self.display_name = display_name
        self.credentials = credentials

    def get_name(self):
        return self.name

    def to_json(self):
        return {
                "name": self.name,
                "provider": self.provider,
                "display_name": self.display_name,
                "credentials": self.credentials
                }