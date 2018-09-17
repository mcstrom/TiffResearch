from datetime import timedelta

class Patient:
    def __init__(self, patient_id, admit_age, gender, race, ethnicity, hospital_stays):
        self.patient_id = patient_id
        self.race = race
        self.ethnicity = ethnicity
        self.admit_age = admit_age[0]
        self.gender = gender[0]
        hospital_stays.sort(key=lambda x: x.admission_date)
        self.hospital_stays = hospital_stays
        self.total_number_of_stays = len(self.hospital_stays)
        self.total_number_of_stays_observed = 0

        # self.total_num_stays_observed = sum(1 for stay in self.hospital_stays if stay.is_observed) (cool way to do this on one line)
        #The stuff below this line calculates the number of observed stays for a patient
        for stay in self.hospital_stays:
            if stay.is_observed:
                self.total_number_of_stays_observed += 1

        self.calculate_readmission_stats()
        self.calculate_bouncebacks()
        self.calculate_total_number_of_bouncebacks()
        self.calculate_unobserved_bouncebacks()
        self.calculate_total_unobserved_bouncebacks()
        self.calculate_total_readmissions()
        self.calculate_total_observed_stays()

    def calculate_readmission_stats(self):
        self.hospital_stays[0].assign_readmittance(False)
        for i in range(len(self.hospital_stays)-1):
            prior_stay = self.hospital_stays[i]
            current_stay = self.hospital_stays[i+1]

            # If current admission date is within seven days of prior discharge date and same principle DX, return true
            seven_days_after_discharge = prior_stay.discharge_date + timedelta(days=7)
            is_within_seven = current_stay.admission_date <= seven_days_after_discharge
            readmitted_result = is_within_seven and prior_stay.principal_diagnosis == current_stay.principal_diagnosis
            current_stay.assign_readmittance(readmitted_result)

    #Bouncebacks are the case in which the patient was observed and then readmitted
    def calculate_bouncebacks(self):
        self.hospital_stays[0].assign_bounceback(False)
        for i in range(len(self.hospital_stays)-1):
            prior_stay = self.hospital_stays[i]
            current_stay = self.hospital_stays[i+1]

            # Check if the readmission occurs after a prior observed stay or not
            # if prior stay = observed and current stay is a readmission return true
            bounceback_result = prior_stay.is_observed and current_stay.is_readmitted
            current_stay.assign_bounceback(bounceback_result)

    # Unobserved bouncebacks are the case in which the patient was readmitted after not being observed
    def calculate_unobserved_bouncebacks(self):
        self.hospital_stays[0].assign_unobserved_bounceback(False)
        for i in range(len(self.hospital_stays)-1):
            prior_stay = self.hospital_stays[i]
            current_stay = self.hospital_stays[i+1]

            # Check if the readmission occurs after a prior observed stay or not
            # if prior stay = observed and current stay is a readmission return true
            unobserved_bounceback_result = not prior_stay.is_observed and current_stay.is_readmitted
            current_stay.assign_unobserved_bounceback(unobserved_bounceback_result)

    def calculate_total_number_of_bouncebacks(self):
        self.bouncebacks = 0
        for stay in self.hospital_stays:
            if stay.is_bounceback:
                self.bouncebacks += 1

    def calculate_total_unobserved_bouncebacks(self):
        self.unobserved_bouncebacks = 0
        for stay in self.hospital_stays:
            if stay.is_unobserved_bounceback:
                self.unobserved_bouncebacks += 1

    def calculate_total_readmissions(self):
        self.total_readmissions = 0
        for stay in self.hospital_stays:
            if stay.is_readmitted:
                self.total_readmissions += 1

    def calculate_total_observed_stays(self):
        self.total_observed_stays = 0
        for stay in self.hospital_stays:
            if stay.is_observed:
                self.total_observed_stays += 1



    def print_info(self):
        print(self.patient_id, self.admit_age, self.gender, self.ethnicity, self.total_number_of_stays, self.total_number_of_stays_observed, self.bouncebacks, self.unobserved_bouncebacks, self.total_readmissions, (self.hospital_stays))
