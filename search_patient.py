import os
import json
import sys
import argparse

from fhir.resources.patient import Patient

from search_util import get_patient_resource, find_all_matches, print_results, is_valid_uuid

#handle CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('--first-name', help='First name of patient')
parser.add_argument('--last-name', help='Last name of patient')
parser.add_argument('--patient-id', help='Patient resource UUID')
args = parser.parse_args()
print(args)

#initialize variables
patient_id = f_name = l_name = None
#if patient_id received, validate and set
if args.patient_id:
    if is_valid_uuid(args.patient_id):
        patient_id = args.patient_id
    else:
        print("ERROR: patient-id is not UUID, please pass in proper patient-id")
        sys.exit()

#if names recieved, retrieve patient_id from patient resource
patient_resource = get_patient_resource(patient_id, f_name, l_name)
if patient_resource:
    patient_id = patient_resource.id
else:
    print("Error: First/Last name did not match any patient resources")
    sys.exit()

#search resources for matching entries
resource_matches = find_all_matches(patient_id)

# convert and sort dictionary to list of tuples
resource_matches = list(resource_matches.items()) 
resource_matches.sort(key = lambda x: x[1], reverse = True)

#print final results
print_results(patient_resource, resource_matches)