#I quite like the stucture and format of the study definition file here:
#https://github.com/opensafely/HbA1c-levels/blob/master/analysis/study_definition.py
#So getting inspiration from there

#####################
# Import statements #
#####################

from cohortextractor import (
    StudyDefinition,
    codelist,
    codelist_from_csv,
    patients,
     '''Other programs/options that could be added
     combine_codelists,
    filter_codes_by_category,'''
)

'''Complete when codelist is published
from codelists import
'''

'''
Comments on codelists - here is one where SNOMED codes for vaccins are compiled:
https://github.com/opensafely/oral-anticoagulant-covid-outcome/blob/main/codelists/opensafely-influenza-vaccination.csv
QUESTION: What I am not sure is then how do you set up the study to look up the SNOMED code in which data schemas
Although not marked as such codes here look like SNOMED codes:
https://github.com/opensafely/SRO-pulse-oximetry/blob/master/codelists/opensafely-pulse-oximetry.csv

'''

######################
#  Study definition  #
######################

study = StudyDefinition(
    # define default dummy data behaviour - must be done for every variable bar population
    # Define start and end dates/set time period
    default_expectations={
        "date": {"earliest": "2019-04-01", "latest": "2021-06-30"},
        "rate": "uniform",
        "incidence": 0.5,
    },

     #Even if working with month of birth index date needed to set up some variables(e.g. IMD)
    # define the study index date
    index_date="2019-04-01",

    #Keeping age as of index date
    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate" : "universal",
            #Do not fully understand the line below or if it will work in all cases
            "int" : {"distribution" : "population_ages"}
    }

    )    
    #If extracting age by category referring to an index data
    #https://github.com/opensafely/HbA1c-levels/blob/master/analysis/study_definition.py
    #Contains some very useful code (starting at "#age") to "envelop" this code to create age categories.
    #If not restricted by disclosure of potentially identifiable information disclosure would rather have month of birth


    '''Gender has to be a variable if we want to do checks on the data (how many are missing or are Female)
    Keeping a possible specification on gender below initially commented out (not a variable)
    By using that one we may be throwing away cases where there has been gender reassignment together with data that may be wrong.
    There seems to be a case for analysing the data for gender after extraction rather than limiting it to Men only'''
    '''Getting to the specification of the population from the list of SNOMED codes for PSA is the trickiest
        A repository that dealt with diagnostics
        https://github.com/opensafely/SRO-pulse-oximetry/blob/master/analysis/study_definition.py
        had the following code snippet

        had_pulse_ox_event_code=patients.with_these_clinical_events(
        pulse_oximetry_codes,
        between=["index_date", "index_date + 1 month"],
        returning="code",
        return_expectations={"category": {
            "ratios": {str(1325191000000108): 0.6, str(1325201000000105): 0.4}}}

        I think it should be possible to define something like a uniform distribution for the ratios in the codes used
        in PSA testing, and this would be OK for test data, and the final distribution of codes in the non-mock data
        would be correct
        QUESTION: What I have still not understood is if the SNOMED codes are going to be searched in every table where
        they may appear
    ),
    '''
    #population=patients.all() [A sometimes useful default option that is not used in this study]
        population=patients.satisfying(
        #'has_PSA_test AND (sex = "M")'
        'has PSA_test',
        #Is it clinical events when we would be looking for codes in diagnostic tests.
        #Which data schema would it look into? All?
        #A full study where a diagnotic procedure or treatment was used would be instrumental in checking the syntax
        has_PSA_test=patients.with_these_clinical_events(
        PSA_codes,
        between=["index_date", "index_date + 27 month"],
        returning="code"
        return_expectations={"category": {
        #Check documentation and complete without having all categories"ratios": {str(1325191000000108): 0.6, str(1325201000000105): 0.4}}}
        ),
    ),
    
        sex=patients.sex(
            returning_expectations={
                "category": {"ratios": {"M": 0.49, "F": 0.51}},
                #"category": {"ratios": {"M": 1, "F": 0}},
                "incidence": 1, #It should be the case bar some minor amount of missing values
            }
    ),
    
    #IMD[Note that is rounded to the nearest 100, so quintiles cannot be defined precisely from that data.
    #If the fist quintile maximum upper bound was 842 values of 843 and 844 which appear as 840 in the data
    #which would be in 2nd quintile would be represented as in the first quintile, which is an error.
    #The error would however been worse if we tried to out of values 330 categories create 66 for each quintile and
    #the distribution of values of IMD across quintiles was not uniform]
 
    imd = patients.categorised_as(
        {
            "0": "DEFAULT",
            "1": """index_of_multiple_deprivation >=1 AND index_of_multiple_deprivation < 32844*1/5""",
            "2": """index_of_multiple_deprivation >= 32844*1/5 AND index_of_multiple_deprivation < 32844*2/5""",
            "3": """index_of_multiple_deprivation >= 32844*2/5 AND index_of_multiple_deprivation < 32844*3/5""",
            "4": """index_of_multiple_deprivation >= 32844*3/5 AND index_of_multiple_deprivation < 32844*4/5""",
            "5": """index_of_multiple_deprivation >= 32844*4/5 """,
        },
        index_of_multiple_deprivation = patients.address_as_of(
            "index_date",
            returning = "index_of_multiple_deprivation",
            round_to_nearest = 100,
        ),
        return_expectations = {
            "rate": "universal",
            "category": {
                "ratios": {
                    "0": 0.01,
                    "1": 0.20,
                    "2": 0.20,
                    "3": 0.20,
                    "4": 0.20,
                    "5": 0.19,
                }
            },
        },
    ),  

    '''The below code illustrateds the convenience of putting IMD values in categories from inceptions. Even if you did not
    have to declare return_expectations for each of the 330 categories available if non-declared could be assumed to be zero
    you would then not have a representative distribution of IMD in the population
    imd=patients.address_as_of(
        "2021-04-01",
        returning="index_of_multiple_deprivation",
        round_to_nearest=100,
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"100": 0.3, "15000": 0.3, "30000": 0.4}},
        },
    )
    '''

    #MSOA may not be worth extracting as it does not seem to allow mapping to CCGs or STPs (LSOAs would, but not in the data)


    month_of_birth=patients.date_of_birth(
        "YYYY-MM",
        return_expectations={
            "date": {"earliest": "1900-01-01", "latest": "today"},
            "rate": "uniform",
        }
    )


    # Region - keeping this if nothing else can be done in terms of extracting a variable that can be mapped to (e.g.) STPs
    region = patients.registered_practice_as_of(
        "index_date",
        returning = "nuts1_region_name",
        return_expectations = {
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and the Humber": 0.1,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East of England": 0.1,
                    "London": 0.2,
                    "South East": 0.2, 
                }
            },       
            "incidence": 0.8}
    ),



    '''ethnicity has problems, as OS mentor detailed, but for the time being keep this'''
    ethnicity_by_16_grouping=patients.with_ethnicity_from_sus(
    returning="group_16",
    use_most_frequent_code=True,
)


#############
#  Measure  #
############# 

'''Section to include if needed for further development
This section
https://github.com/opensafely/SRO-pulse-oximetry/blob/master/analysis/study_definition.pyof a repository has
some very good examples of application of measures at the data extraction stage, as per below.
Note that extracting measures like simplifies work upstream, but does not allow to develop/apply Python capabilities to
the extent that "rawer" data would

measures = [
   

    Measure(
        id="had_pulse_ox_total",
        numerator="had_pulse_ox",
        denominator="population",
        group_by=None
    ),



    Measure(
        id="had_pulse_ox_by_age_band",
        numerator="had_pulse_ox",
        denominator="population",
        group_by=["age_band"],
    ),

]
'''