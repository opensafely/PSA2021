from cohortextractor import codelist, codelist_from_csv
#only use ", combine_codelists" if using more than one codelist

# NEED TO MAKE SURE THIS IS EXTRACTING FROM THE CORRECT MOST UP-TO-DATE VERSION - IT IS IN STUDY_DEFINITION.PY, NOT CALLED FROM HERE
PSA_test = codelist_from_csv("codelist/user-poliveira28-psa-test.csv",
    system="snomed",
    column="code")
#pulse_oximetry_codes = codelist_from_csv("codelists/opensafely-pulse-oximetry.csv",
#    system="ctv3",
#    column="CTV3ID",)

   #This is the csv list in the codelist folder
    #Name of the file has already got the "-" instead of the "/"
    #"codelists/user-poliveira28-psa-test.csv",
    #system="snomed",
    #Other options fpr system/column: ctv3/CTV3ID], icd10/icd10_code
    #column="code",

#    any_from_previous lists = combine_codelists(
#        list name as previously assigned 1,
#        ...,
#        list name as previously assigned n,
#    )
#    
# For future search and use outside this project: Example of a set of cancer codes that is pre-defined and not based on ICD-10 codes
#    lung_cancer_codes = codelist_from_csv(
#        "codelists/opensafely-lung-cancer.csv", system="ctv3", column="CTV3ID"
#    )
