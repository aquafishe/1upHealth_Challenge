# 1upHealth_Challenge
## Setup
This project is supported using Python **3.9.6**

Run following command in the project root directory:
```
pip3 install -r requirements.txt
```
## Instructions
Run the application by using the commands below, also see assumptions:
```
# Search by Patient First/Last Name
python3 search_patient.py --first-name Cleo27 --last-name Bode78

# Search by Patient Id
python3 search_patient.py --patient-id d13874ec-22ea-46ed-a55c-1fd75ef56a58
```    
* Searching by Patient Name, first-name and last-name must be provided together
* Searching by Patient Id, patient-id is valid UUID (version 4)
* If all arguments (first-name, last-name, patient-id) are provided application will default to Patient Id search

## Development Notes
### Assumptions
* CLI arguments used match on **Patient** resource, since goal to find references to "patient"

### Development Process
* Started by reviewing the FHIR resource .ndjson files and researching applicable python packages (fhirclient, fhir.resources, smart-on-fhir)
* Decided to use fhir.resources package for Patient resource retrieval however not for all resources to overcomplicate solution
    * serializing the data to fhir.resources model would give extra validation to ensure the provided JSON match the resource model structure
* Implemented logic based on core tasks below:
    1. Retrieve Patient resource entry based on, First/Last name OR Patient Id
    2. Search ALL resources which reference retrieved Patient
    3. Print results which include Patient details and matching resources

### Takeaways
* Reviewing challenge instructions, I noticed my results did not match 1:1 with the included screenshot. Resources like Practitioner and PractitionerRole had matches however, reviewing the resource entries I did not see specific references to the patient "Cleo27 Bode78". I decided to leave my code as is, since I did not see any references. However I do understand there could be other indirect relationships I am not currently seeing.

