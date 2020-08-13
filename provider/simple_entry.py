class SimpleEntry:
    def __init__(self, name, address, password):
        self.name = name
        self.addresses = address
        self.password = password

    def __str__(self):
        return 'name: {} urls: {}'.format(self.name, ', '.join(self.addresses))
