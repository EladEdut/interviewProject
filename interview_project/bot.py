class Bot:

    def __init__(self, provider, name, display_name, credentials):
        self.provider = provider
        self.name = name
        self.display_name = display_name
        self.credentials = credentials

    def get_name(self):
        return self.name

    def to_json(self):
        return {
                "name": self.name,
                "provider": self.provider,
                "display name": self.display_name,
                "credentials": self.credentials
                }