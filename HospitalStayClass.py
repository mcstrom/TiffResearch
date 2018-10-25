from datetime import datetime


class HospitalStay:

    # Expecting dates in string format
    def __init__(self, discharge_id, principal_diagnosis, payment_info, hospital_location, service_days, admission_date_from_data, discharge_date_from_data):
        self.discharge_id = discharge_id
        self.payment_info = payment_info[0]
        self.hospital_location = hospital_location[0]
        self.principal_diagnosis = principal_diagnosis[0]
        service_days.sort(key=lambda x: x.date_of_service)
        self.service_days = service_days
        self.admission_date = self.service_days[0].date_of_service
        self.discharge_date = self.service_days[-1].date_of_service
        self.admission_date_from_data = admission_date_from_data
        self.discharge_date_from_data = discharge_date_from_data
        # self.admission_date_unstripped = admission_date
        # self.discharge_date_unstripped = discharge_date
        self.is_all_oral = all("parenteral" not in day.route_of_administration for day in self.service_days)
        self.is_all_parenteral = all("oral" not in day.route_of_administration for day in self.service_days)
        self.is_vanco_first_day = 'Vancomycin (HCl)' in self.service_days[0].drug_title
        self.is_parenteral_first_day = "parenteral" in self.service_days[0].route_of_administration
        self.is_Penicillin_V_in_stay = any("Penicillin V potassium" in day.drug_title for day in self.service_days)
        self.is_Penicillin_G_in_stay = any("Penicillin G (aqueous) (potassium) (sodium)" in day.drug_title for day in self.service_days)
        self.is_Ceftriaxone_sodium_in_stay = any("Ceftriaxone sodium" in day.drug_title for day in self.service_days)
        self.is_Cefazolin_sodium_in_stay = any("Cefazolin sodium" in day.drug_title for day in self.service_days)

        # Now calculate if patient was observed or not. Default behavior is not observed or false
        self.is_observed = False
        if len(self.service_days) > 1:
            self.is_observed = "parenteral" not in self.service_days[-1].route_of_administration and \
                               "oral" in self.service_days[-2].route_of_administration and \
                               "parenteral" in self.service_days[0].route_of_administration





        # Initialize readmittance values only if we call the readmitted function


    def assign_readmittance(self, is_readmitted):
        self.is_readmitted = is_readmitted

    def assign_bounceback(self, is_bounceback):
        self.is_bounceback = is_bounceback

    def assign_unobserved_bounceback(self, is_unobserved_bounceback):
        self.is_unobserved_bounceback = is_unobserved_bounceback

    def __str__(self):
        return 'Hospital_Stay<' + ' d_id:' + str(self.discharge_id) + ' pay_info:' + str(self.payment_info) + \
               ' a_date:' + str(self.admission_date)[:-9] + ' d_date:' + str(self.discharge_date)[:-9] + \
               ' principal_dx: ' + str(self.principal_diagnosis) + ' Stay_info: ' + str(self.service_days) + \
               ' Is observed: ' + str(self.is_observed) + ' Is readmitted: ' + str(self.is_readmitted) + \
               ' Is BOUNCEBACK: ' + str(self.is_bounceback) + '>'

        # return 'Hospital_Stay<' + ' d_id: ' + str(self.discharge_id) + ' a_date: ' + str(self.admission_date)[:-9] + \
        #       ' a_date_unstr: ' + str(self.admission_date_unstripped) + ' d_date: ' + str(self.discharge_date)[:-9] +\
        #        ' d_date_unstr: ' + str(self.discharge_date_unstripped) + '>'

    __repr__ = __str__
