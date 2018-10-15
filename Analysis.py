import csv
from PatientClass import Patient
from HospitalStayClass import HospitalStay
from ServiceDatesClass import ServiceDates
from datetime import datetime, timedelta


''' This is a git practice comment'''

'''
This function will return a list of the headers from the excel file. Takes them out from the dictionary.
'''
def get_race_headers(data_input):
    headers = list(data_input[0].keys())
    return [header for header in headers if 'Race' in header]

'''
This function takes in MRN, ethnicity headers, and data and returns the ethnicity and race of the patient combined
combined into one value.
'''
def get_race(medical_record_id, headers, data_input):
    for row in data_input:
      if row['Medical Record Number'] == medical_record_id:
        for header in headers:
          if row[header] == 'Y':
              return header
        return 'Race - None Specified' #only gets to this case if "N" for all races

'''
This function takes in MRN, discharge id, and data and returns the ethnicity listed for the patient.
'''
def get_ethnicity(medical_record_id, data_input):
    return list(set([row['Ethnicity Title'] for row in data_input if row['Medical Record Number'] == medical_record_id]))[0]

'''
Gets the hospital location for a given stay. takes in the MRN, discharge id, and data.
Returns "Hospital City".
'''
def get_hospital_location(id_string, discharge_id_string, data_input):
    return list(set([row['Hospital City'] for row in data_input if row['Medical Record Number'] == id_string
                     and row['Discharge ID'] == discharge_id_string]))

'''
Gets the hospital location for a given stay. takes in the MRN, discharge id, and data.
Returns "Hospital City".
'''
def get_payment_info(id_string, discharge_id_string, data_input):
    return list(set([row['Primary Source Of Payment Title'] for row in data_input if row['Medical Record Number'] == id_string
                     and row['Discharge ID'] == discharge_id_string]))

'''
Get administration route of abx for a given MRN, discharge id, date of service (date of interest), and the data set
'''
def get_drug_title(discharge_id_string, medical_record_id, date_of_service, data_input):
  return list(set([row['Generic Drug Title'] for row in data_input if row['Medical Record Number'] == medical_record_id
          and row['Discharge ID'] == discharge_id_string and row['Date Of Service'] == date_of_service]))

'''
Get administration route of abx for a given MRN, discharge id, date of service (date of interest), and the data set
'''
def get_administration_route(discharge_id_string, medical_record_id, date_of_service, data_input):
  return list(set([row['Route Of Administration Title'] for row in data_input if row['Medical Record Number'] == medical_record_id
          and row['Discharge ID'] == discharge_id_string and row['Date Of Service'] == date_of_service]))

'''
Get admission date associated with discharge id and user id from the data in the table
'''
def get_admission_date_from_data(discharge_id_string, medical_record_id, data_input):
  return  [row['Admit Date'] for row in data_input if row['Medical Record Number'] == medical_record_id
           and row ['Discharge ID'] == discharge_id_string][0]

'''
Get discharge date associated with discharge id and user id from the data in the table
'''
def get_discharge_date_from_data(discharge_id_string, medical_record_id, data_input):
  return [row['Discharge Date'] for row in data_input if row['Medical Record Number'] == medical_record_id
          and row['Discharge ID'] == discharge_id_string][0]

'''
Takes in patient MRN and discharge id and returns the dates of service associated with that stay. Dates are returned
as a list of strings
'''
def get_service_dates(id_string, discharge_id_string, data_input):
    return list(set([row['Date Of Service'] for row in data_input if row['Medical Record Number'] == id_string
                     and row['Discharge ID'] == discharge_id_string]))

'''
Takes in patient MRN discharge id and returns the principal diagnosis
'''
def get_principal_diagnosis(id_string, discharge_id_string, data_input):
    return list(set([row['Principal Dx Title (ICD)'] for row in data_input if row['Medical Record Number'] == id_string
                     and row['Discharge ID'] == discharge_id_string]))

'''
Takes in patient MRN and returns the gender
'''
def get_gender(id_string, data_input):
    return list(set([row['Gender Title'] for row in data_input if row['Medical Record Number'] == id_string]))

'''
Takes in patient MRN and returns the admit age
'''
def get_admit_age(id_string, data_input):
    return list(set([row['Admit Age In Years'] for row in data_input if row['Medical Record Number'] == id_string]))

'''
Gets the discharge ids for the given medical record number in the data. Returns only one copy of each discharge 
id even if multiple are present.
'''
def get_discharge_ids(id_string, data_input):
    return list(set([row['Discharge ID'] for row in data_input if row['Medical Record Number'] == id_string]))

'''
NOT USED IN THE PATIENT CLASS. Determines all unique discharge IDs in the data. Returns a list of all the ID's.
'''
def get_all_unique_discharge_ids(data_input):
    return list(set([row['Discharge ID'] for row in data_input]))

'''
Determines all medical record numbers in the data. Returns a list of all the MRNs.
'''
def get_all_unique_ids(data_input):
    return list(set([row['Medical Record Number'] for row in data_input]))

def write_to_csv(patients):
    with open('One_line_results.csv', 'w', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['Patient ID', 'Discharge ID', 'Admit Date Calculated', 'Admit Date From Data',
                            'Discharge Date Calculated', 'Discharge Date From Data', 'Principal Diagnosis',
                            'Hospital Location', 'Age', 'Gender', 'Race', 'Ethnicity', 'Payment Info',
                            'Vanco First Day', 'Readmission, Observed Previous Stay',
                            'Readmission, Unobserved Previous Stay', 'Observed Stay', 'All Oral', 'All Parenteral'])
        for patient in patients:
            for stay in patient.hospital_stays:
               value = [patient.patient_id, stay.discharge_id, str(stay.admission_date)[0:-8],
                        stay.admission_date_from_data, str(stay.discharge_date)[0:-8], stay.discharge_date_from_data,
                        stay.principal_diagnosis, stay.hospital_location, patient.admit_age, patient.gender,
                        patient.race, patient.ethnicity, stay.payment_info, stay.is_vanco_first_day, stay.is_bounceback,
                        stay.is_unobserved_bounceback, stay.is_observed, stay.is_all_oral, stay.is_all_parenteral]
               thewriter.writerow(value)


def main():

    with open('./Clean_Data.csv', newline='') as csvfile:  # ./ just means to look in current directory
        # Bringing in data
        data_values = [] # data values is a list of dictionaries copied from the dict reader object
        data_object = csv.DictReader(csvfile) # now we can reference specific things
        for row in data_object:
            data_values.append(row)

        #Get patient MRNs
        patient_ids = get_all_unique_ids(data_values)

        #Get particular data for each patient and store it for them
        all_patients = []
        hospital_locations = []
        payment_sources = []
        for patient_id in patient_ids:
            discharge_ids = get_discharge_ids(patient_id, data_values)
            race = get_race(patient_id, get_race_headers(data_values), data_values)
            ethnicity = get_ethnicity(patient_id, data_values)
            admit_age = get_admit_age(patient_id, data_values)
            gender = get_gender(patient_id, data_values)

            hospital_stays = []
            for discharge_id in discharge_ids:

                days_of_service = get_service_dates(patient_id, discharge_id, data_values)
                service_days = []
                for day in days_of_service:
                    route_of_administration = get_administration_route(discharge_id, patient_id, day, data_values)
                    drug_title = get_drug_title(discharge_id, patient_id, day, data_values)
                    service_day = ServiceDates(day, drug_title, route_of_administration)
                    service_days.append(service_day)

                admission_date_from_data = get_admission_date_from_data(discharge_id, patient_id, data_values)
                discharge_date_from_data = get_discharge_date_from_data(discharge_id, patient_id, data_values)
                principal_diagnosis = get_principal_diagnosis(patient_id, discharge_id, data_values)
                payment_info = get_payment_info(patient_id, discharge_id, data_values)
                payment_sources.append(payment_info[0])
                hospital_location = get_hospital_location(patient_id, discharge_id, data_values)
                hospital_locations.append(hospital_location[0])
                hospital_stay = HospitalStay(discharge_id, principal_diagnosis, payment_info, hospital_location,
                                             service_days, admission_date_from_data, discharge_date_from_data)
                hospital_stays.append(hospital_stay)

            temp_patient = Patient(patient_id, admit_age, gender, race, ethnicity, hospital_stays)
            all_patients.append(temp_patient)
        hospital_location_list = list(set(hospital_locations))
        unique_payment_sources = list(set(payment_sources))
        print(hospital_location_list)
        print(unique_payment_sources)

        # print particular data for each of the patients. Mainly for troubleshooting purposes.
        #for patient in all_patients:
        #    patient.print_info()

        # Data Analysis section
        total_number_of_patients = len(patient_ids)
        print('Total Number of Patients: ' + str(total_number_of_patients))
        total_number_of_admissions = len(get_all_unique_discharge_ids(data_values))
        print('Total Number of Admissions: ' + str(total_number_of_admissions))

        total_number_of_stays =  0
        total_number_of_bouncebacks = 0
        total_number_of_unobserved_bouncebacks = 0
        total_number_of_readmissions = 0
        total_number_of_observed_stays = 0

        for patient in all_patients:
            total_number_of_stays += len(patient.hospital_stays)
            total_number_of_bouncebacks += patient.bouncebacks
            total_number_of_unobserved_bouncebacks += patient.unobserved_bouncebacks
            total_number_of_readmissions += patient.total_readmissions
            total_number_of_observed_stays += patient.total_observed_stays


        total_number_of_unobserved_stays = total_number_of_stays - total_number_of_observed_stays

        print('Total Number of stays: ' + str(total_number_of_stays))
        print('Total Number of bouncebacks: ' + str(total_number_of_bouncebacks))
        print('Total Number of unobserved bouncebacks: ' + str(total_number_of_unobserved_bouncebacks))
        print('Total Number of readmissions within 7 days for same principle DX: ' + str(total_number_of_readmissions))
        print('Total Number of observed stays: ' + str(total_number_of_observed_stays))
        print('Total Number of unobserved stays: ' + str(total_number_of_unobserved_stays))

        # next thing we care about is the not-observed bouncebacks

        # Write things to Excel for easy manipulation
        printout_titles = ['Total Number of Patients: ', 'Total Number of Admissions: ',
                           'Total Number of Observed Stays: ', 'Total Number of Unobserved Stays: ',
                           'Total Number of Bouncebacks: ', 'Total Number of Unobserved Bouncebacks: ',
                           'Total Number of Readmissions within 7 days for same principle DX: ']

        printout_values = [total_number_of_patients, total_number_of_admissions, total_number_of_observed_stays,
                           total_number_of_unobserved_stays, total_number_of_bouncebacks,
                           total_number_of_unobserved_bouncebacks, total_number_of_readmissions]

        write_to_csv(all_patients)

'''
        
        with open('AnalysisResults.csv', 'w', newline='') as f:
            thewriter = csv.writer(f)
            thewriter.writerow(printout_titles)
            thewriter.writerow(printout_values)




    print('Yo')

    with open('One_Line_Data.csv', 'w', newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['Row'])
        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            thewriter.writerow(str(i))
'''

if __name__ == "__main__":
    main()
