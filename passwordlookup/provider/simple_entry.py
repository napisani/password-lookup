class SimpleEntry:
    def __init__(self, name, address, password, username=''):
        self.name = name
        self.addresses = address
        self.password = password
        self.username = username

    def __str__(self):
        return 'name: {} urls: {}'.format(self.name, ', '.join(self.addresses))
