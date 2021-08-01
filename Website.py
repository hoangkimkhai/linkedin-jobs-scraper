class Website:
    """Contains information about website structure"""
    def __init__(self, name, url, search_url, login_url):
        self.name = name
        self.url = url
        self.search_url = search_url
        self.login_url = login_url