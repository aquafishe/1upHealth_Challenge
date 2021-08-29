import os
import json
from uuid import UUID
from fhir.resources.patient import Patient

base_resource_dir = 'CodingChallengeData'

#get Patient resource matching CLI patient args
def get_patient_resource(patient_id, f_name, l_name):
    patient_resource_path = f"{base_resource_dir}/Patient.ndjson"
    for line in open(patient_resource_path):
        patient = Patient.parse_obj(json.loads(line))
        if patient_id:
            if match_by_id(patient, patient_id):
                return patient
        else: 
            if match_by_name(patient, f_name, l_name):
                return patient
    return None

#check if patient resource match CLI name arguments
def match_by_name(patient, f_name, l_name):
    for name in patient.name:
        if name.use == "official":
            for g in name.given:
                if g == f_name and name.family == l_name:
                    return True
    return False

#check if patient resource match CLI patient_id arguments
def match_by_id(patient, patient_id):
    if patient.id == patient_id:
        return True
    return False

#get patient name from patient_resource
def get_official_patient_name(patient_resource):
    for name in patient_resource.name:
        if name.use == "official":
            return (name.given[0], name.family)
    return None

#Get Patient resource matching CLI patient args
def get_patient_resource_n(f_name, l_name):
    patient = None
    patient_resource = f"{base_resource_dir}/Patient.ndjson"
    for line in open(patient_resource):
        cur_p = json.loads(line)
        for name in cur_p.get('name'):
            if name.get('family') == l_name:
                for g in name.get('given'):
                    if g == f_name:
                        patient = cur_p
    return 
    
#search through resources for patient specific matching values
def find_resource_matches(patient_id, resource_name):
    count = 0
    resource_path = f"{base_resource_dir}/{resource_name}"
    for line in open(resource_path):
        entry = json.loads(line)
        patient_val = f"Patient/{patient_id}"
        
        #check for patient attribute
        patient = entry.get('patient')
        if patient != None:
            reference = patient.get('reference')
            if reference == patient_val:
                count += 1
                continue
        #check for subject attribute
        subject = entry.get('subject')
        if subject != None:
            reference = subject.get('reference')
            if reference == patient_val:
                count += 1
                continue
        #check for target attribute
        target = entry.get('target')
        if target != None:
            for ref in target:
                reference = ref.get('reference')
                if reference == patient_val:
                    count += 1
    return count

#find all patient matches to resources
#returns dictionary with (resource_name: #_of_matches)
def find_all_matches(patient_id):
    fhir_resources = os.listdir(base_resource_dir)
    resource_matches = {}
    for resource_name in fhir_resources:
        matches = find_resource_matches(patient_id, resource_name)
        if matches > 0:
            #remove file extension
            resource_name = resource_name[:-7]
            resource_matches[resource_name] = matches
    return resource_matches

#print final matching results
def print_results(patient, resource_matches):
    names = get_official_patient_name(patient)
    print(f"Patient Name: {names[0]} {names[1]}")
    print(f"Patient Id: {patient.id}\n")
    print(f"RESOURCE_TYPE {'COUNT'.rjust(15, ' ')}")
    print(f"-----------------------------")
    for resource_name, count in resource_matches:
        print('{:<20} {:>8}'.format(resource_name, count))
    print("resource matches: " + str(len(resource_matches)))

#validate UUID based on version 4, citing http://www.hl7.org/FHIR/uuid.profile.json.html
def is_valid_uuid(patient_id):
    try:
        uuid_obj = UUID(patient_id, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == patient_id