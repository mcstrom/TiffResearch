from datetime import datetime


class ServiceDates:

    def __init__(self, date_of_service, drug_title, route_of_administration):

        self.date_of_service = datetime.strptime(date_of_service, "%m/%d/%Y")
        self.drug_title = drug_title
        self.route_of_administration = route_of_administration

    def __str__(self):
        return 'service_date<' + ' day:' + str(self.date_of_service)[:-9] + ' drug_title:' + str(self.drug_title) + \
               ' route_of_administration' + str(self.route_of_administration) + '>'

    __repr__ = __str__