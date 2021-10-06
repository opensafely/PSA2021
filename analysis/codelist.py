from cohortextractor import codelist, codelist_from_csv
#only use ", combine_codelists" if using more than one codelist

PSA_test = codelist_from_csv(
    #This is the csv list in the codelist folder
    "user/poliveira28/psa-test/437eb36a.csv",
    system="snomed",
    #Other options: ctv3 [column CTV3ID], icd10 [column icd10_code]
    column="code",
)
'''any_from_previous lists = combine_codelists(
    list name as previously assigned 1,
    ...,
    list name as previously assigned n,
)'''
'''For future search and use outside this project: Example of a set of cancer codes that is pre-defined and not based on ICD-10 codes
lung_cancer_codes = codelist_from_csv(
    "codelists/opensafely-lung-cancer.csv", system="ctv3", column="CTV3ID"
)'''
