class Job:
    def __init__(self, title, company, location, posted_date, num_apps):
        self.title = title
        self.company = company
        self.location = location
        self.posted_date = posted_date
        self.num_apps = num_apps

    def myprint(self):
        print(self.title, self.company, self.location)
