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
    #Not sure if the above is needed or at the correct place when you use codelist.py
    patients,
    Measure
     #Other programs/options that could be added
     #combine_codelists,
     #filter_codes_by_category,'''
)

#from codelists import *
# We are bypassing the codelist.py file at this stage
# NEED TO MAKE SURE THIS IS EXTRACTING FROM THE CORRECT MOST UP-TO-DATE VERSION - IT IS ALSO CALLED IN CODELIST.PY
PSA_test = codelist_from_csv("codelists/user-poliveira28-psa-test.csv",
    system="snomed",
    column="code") 
#    For the time being the list is under review and not finalised
#    Unsure if the below line of code would work - check other projects
#    Probably the below need to have "-" instead of "/"
#    from codelists import user/poliveira28/psa-test/437eb36a

#CHECKED THAT DETAILS OF SECOND LIST CORRECT
PSA_test_long = codelist_from_csv("codelists/user-poliveira28-psa-test-long.csv",
    system="snomed",
    column="code")



#    Comments on codelists - here is one where SNOMED codes for vaccins are compiled:
#    https://github.com/opensafely/oral-anticoagulant-covid-outcome/blob/main/codelists/opensafely-influenza-vaccination.csv
#    QUESTION: What I am not sure is then how do you set up the study to look up the SNOMED code in which data schemas
#    Although not marked as such codes here look like SNOMED codes:
#    https://github.com/opensafely/SRO-pulse-oximetry/blob/master/codelists/opensafely-pulse-oximetry.csv


#start_date = "2019-04-01"
#end_date = "2021-09-30"


######################
#  Study definition  #
######################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Commented out as when generating study population gave module not recognized  import plotly.graph_objects as go
import json
import datetime

study = StudyDefinition(
    # define default dummy data behaviour - must be done for every variable bar population
    # Define start and end dates/set time period
    index_date = "2019-04-01",
    default_expectations={
        "date": {"earliest": "2019-04-01", "latest": "2021-09-30"},
        "rate": "uniform",
        "incidence": 1
 #Changed from       "incidence": 0.5
        },

    #Even if working with month of birth index date needed to set up some variables (e.g. IMD)
    # We will not be defiing the study index date as
    #index_date="2019-04-01"
    #Since the index rate will be made to vary for the beginning of each of the 27 months we will analyse


    #If extracting age by category referring to an index data
    #https://github.com/opensafely/HbA1c-levels/blob/master/analysis/study_definition.py
    #Contains some very useful code (starting at "#age") to "envelop" this code to create age categories.
    #If not restricted by disclosure of potentially identifiable information disclosure would rather have month of birth


    #    Gender has to be a variable if we want to do checks on the data (how many are missing or are Female)
    #    Keeping a possible specification on gender below initially commented out (not a variable)
    #    By using that one we may be throwing away cases where there has been gender reassignment together with data that may be wrong.
    #    There seems to be a case for analysing the data for gender after extraction rather than limiting it to Men only
 
    #    Getting to the specification of the population from the list of SNOMED codes for PSA is the trickiest
    #    A repository that dealt with diagnostics
    #    https://github.com/opensafely/SRO-pulse-oximetry/blob/master/analysis/study_definition.py
    #    had the following code snippet
    #    had_pulse_ox_event_code=patients.with_these_clinical_events(
    #    pulse_oximetry_codes,
    #    between=["index_date", "index_date + 1 month"],
    #    returning="code",
    #    return_expectations={"category": {
    #        "ratios": {str(1325191000000108): 0.6, str(1325201000000105): 0.4}}}

    #    I think it should be possible to define something like a uniform distribution for the ratios in the codes used
    #    in PSA testing, and this would be OK for test data, and the final distribution of codes in the non-mock data
    #    would be correct
    #    QUESTION: What I have still not understood is if the SNOMED codes are going to be searched in every table where
    #    they may appear
    #    ),

    #Line on PSA test_long_date below added 2021-10-21 - may not be logic    
    #population=patients.all() [A sometimes useful default option that is not used in this study]
    population=patients.satisfying(
        """
        PSA_test_date
        OR PSA_test_long_date
        AND (sex = "M")
        """,
        sex=patients.sex(
        return_expectations={
            #"category": {"ratios": {"M": 0.49, "F": 0.51}},
            #Do also in population sex_at_birth = Male (will also affect full download) - sex is the variable
            "category": {"ratios": {"M": 1, "F": 0}},
            "incidence": 1, #It should be the case bar some minor amount of missing values
        }
    ),


    #     """
    #     PSA_test_long_date
    #     AND (sex_long = "M")
    #     """,
    #     sex_long=patients.sex(
    #     return_expectations={
    #         "category": {"ratios": {"M": 0.49, "F": 0.51}},
    #         Do also in population sex_at_birth = Male (will also affect full download) - sex is the variable
    #         "category": {"ratios": {"M": 1, "F": 0}},
    #         "incidence": 1, #It should be the case bar some minor amount of missing values
    #     }
    # ),

),   
#   Parentheses is OK and closes population. Colon needs to be there. Study definition closing parentheses needs to be before
#   measures, no colon after



    PSA_test_date=patients.with_these_clinical_events(
        PSA_test,
        # The line below will not work as it will include the firts day of the next month
        # between=["index_date", "index_date + 1 month"],
        # So using last_day_of_month function - e.g. as in https://github.com/opensafely/SRO-template/blob/master/analysis/study_definition.py
        between=["index_date", "last_day_of_month(index_date)"],
        #Remember index date will be changed iteratively so that we have data extracted for each month since April 2019
        returning="date",
        find_first_match_in_period=True,
        date_format="YYYY-MM-DD",
        return_expectations={"date": {"earliest": "2019-04-01", "latest": "2021-09-30"}, "rate" : "exponential_increase"},
    ),




    PSA_test_long_date=patients.with_these_clinical_events(
        PSA_test_long,
        # The line below will not work as it will include the firts day of the next month
        # between=["index_date", "index_date + 1 month"],
        # So using last_day_of_month function - e.g. as in https://github.com/opensafely/SRO-template/blob/master/analysis/study_definition.py
        between=["index_date", "last_day_of_month(index_date)"],
        #Remember index date will be changed iteratively so that we have data extracted for each month since April 2019
        returning="date",
        find_first_match_in_period=True,
        date_format="YYYY-MM-DD",
        return_expectations={"date": {"earliest": "2019-04-01", "latest": "2021-09-30"}, "rate" : "exponential_increase"},
    ),






#   Start of the definition of other variables and measure

        #Rather than just 'has_PSA_test',
        #Is it clinical events when we would be looking for codes in diagnostic tests.
        #Which data schema would it look into? All?
        #A full study where a diagnotic procedure or treatment was used would be instrumental in checking the syntax
        #2021/10/11 - moved all of the code allowing defining variables out of the pop definition section    

    #   Question: if (may not be necessary) I wanted to also have the code, guess I need to specify another variable and expectations
    #   But do I need to assign a ratio to each code? There are 18 of them.
    #   return_expectations={"category": {
    #   Check documentation and complete without having all categories"ratios": {str(1325191000000108): 0.6, str(1325201000000105): 0.4}}}


    had_PSA_test=patients.with_these_clinical_events(
        PSA_test,
        returning="binary_flag",
        between=["index_date", "last_day_of_month(index_date)"],
        return_expectations={"incidence": 1}
    #2021/10/19 - changed from    return_expectations={"incidence": 0.5}
    ),



    had_PSA_test_long=patients.with_these_clinical_events(
        PSA_test_long,
        returning="binary_flag",
        between=["index_date", "last_day_of_month(index_date)"],
        return_expectations={"incidence": 1}
    #2021/10/19 - changed from    return_expectations={"incidence": 0.5}
    ),





    # Inspired by https://github.com/opensafely/SRO-pulse-oximetry/blob/master/analysis/study_definition.py
    # Looks logic that the definition of this variable is left out of the definition of the study population
    # population=patients.satisfying(
    #    had_PSA_test_code=patients.with_these_clinical_events(
    #    PSA_test,
    #COULD THERE BE AN ERROR HERE IF CODES WERE NUMERICAL AND NOT CATEGOY (UNLIKELY)? INDENTATION INCORRRECT? EASY TO CHECK CODE
    PSA_test_code=patients.with_these_clinical_events(
        PSA_test,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="code",
        return_expectations={"category":
            #Replace ratios by actual codes - 25 total -, and note this is a highly illogical way of proceeding with many codes
            #Pick just a limited set of codes and make it sum to 1
            #Redefine if there are problmes with extraction
            {"ratios": {str(1030791000000100): 0.5,
            str(1000381000000105): 0.5,
#Commented out and values of expectations above changed as they are in only one of the code lists
#            str(166160000): 0.05,
#            str(166159005): 0.05
                }
            },
        },
    ),



    PSA_test_long_code=patients.with_these_clinical_events(
        PSA_test_long,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="code",
        return_expectations={"category":
            #Replace ratios by actual codes - 25 total -, and note this is a highly illogical way of proceeding with many codes
            #Pick just a limited set of codes and make it sum to 1
            #Redefine if there are problmes with extraction
            {"ratios": {str(1030791000000100): 0.5,
            str(1000381000000105): 0.5,
#Commented out and values of expectations above changed as they are in only one of the code lists
#            str(166160000): 0.05,
#            str(166159005): 0.05
                }
            },
        },
    ),







    #2021/10/20 - commented out to minimise outputs, though working
    # #Keeping age as of index date
    # age=patients.age_as_of(
    #     "index_date",
    #     return_expectations={
    #         "rate" : "universal",
    #         #Do not fully understand the line below or if it will work in all cases
    #         "int" : {"distribution" : "population_ages"}
    #     },
    # ),

    #2021/10/20 - commented out to minimise outputs, though working
    # #I Confirmed that the below are the age categories required by the sponsor. Adapted from
    # #https://github.com/opensafely/HbA1c-levels/blob/master/analysis/study_definition.py

    # age_group = patients.categorised_as(
    #     {
    #         "0-59": "age >= 0 AND age < 60",
    #         "60-64": "age >= 60 AND age < 65",
    #         "65-69": "age >= 65 AND age < 70",
    #         "70-74": "age >= 70 AND age < 75",
    #         "75-79": "age >= 75 AND age < 80",
    #         "80+": "age >= 80",
    #         "missing": "DEFAULT",
    #     },
    #     return_expectations = {
    #         "rate": "universal",
    #         "category": {
    #             "ratios": {
    #                 "0-59": 0.20,
    #                 "60-64": 0.16,
    #                 "65-69": 0.16,
    #                 "70-74": 0.16,
    #                 "75-79": 0.16,
    #                 "80+": 0.16,
    #                 "missing": 0.0,                   
    #             }
    #         },
    #     },
    # ),



    
    #IMD[Note that is rounded to the nearest 100, so quintiles cannot be defined precisely from that data.
    #If the fist quintile maximum upper bound was 842 values of 843 and 844 which appear as 840 in the data
    #which would be in 2nd quintile would be represented as in the first quintile, which is an error.
    #The error would however been worse if we tried to out of values 330 categories create 66 for each quintile and
    #the distribution of values of IMD across quintiles was not uniform]
 
#     Error in this code - see https://github.com/opensafely/SRO-template/blob/master/analysis/study_definition.py
#     May come from categorization, probably not from rounding, 
#     imd = patients.categorised_as(
#         {
#             "0": "DEFAULT",
#             "1": """index_of_multiple_deprivation >=1 AND index_of_multiple_deprivation < 32844*1/5""",
#             "2": """index_of_multiple_deprivation >= 32844*1/5 AND index_of_multiple_deprivation < 32844*2/5""",
#             "3": """index_of_multiple_deprivation >= 32844*2/5 AND index_of_multiple_deprivation < 32844*3/5""",
#             "4": """index_of_multiple_deprivation >= 32844*3/5 AND index_of_multiple_deprivation < 32844*4/5""",
#             "5": """index_of_multiple_deprivation >= 32844*4/5 """,
#         },
#         index_of_multiple_deprivation = patients.address_as_of(
#             "index_date",
#             returning = "index_of_multiple_deprivation",
#             round_to_nearest = 100,
#         return_expectations = {
#             "rate": "universal",
#             "category": {
#                 "ratios": {
#                     "0": 0.01,
#                     "1": 0.20,
#                     "2": 0.20,
#                     "3": 0.20,
#                     "4": 0.20,
#                     "5": 0.19,
#                 }
#             },
#         },
#     ),  
# ),


#    The below code illustrates the convenience of putting IMD values in categories from inception. Even if you did not
#    have to declare return_expectations for each of the 330 categories available if non-declared could be assumed to be zero
#    you would then not have a representative distribution of IMD in the population
#    imd=patients.address_as_of(
#        "2021-04-01",
#        returning="index_of_multiple_deprivation",
#        round_to_nearest=100,
#        return_expectations={
#            "rate": "universal",
#            "category": {"ratios": {"100": 0.3, "15000": 0.3, "30000": 0.4}},
#        },
#    )
    

    #MSOA may not be worth extracting as it does not seem to allow mapping to CCGs or STPs (LSOAs would, but not in the data)


    month_of_birth=patients.date_of_birth(
        "YYYY-MM",
        return_expectations={
            "date": {"earliest": "1900-01-01", "latest": "today"},
            "rate": "uniform",
#Tried to change to the following but not admitted           "rate": "exponential",
        }
    ),


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
                    "South East": 0.2}
        },      
    #COMMENTED OUT this as it looked extraneous        "incidence": 0.8}
    },
    ),


#    ethnicity has problems, as OS mentor detailed, but for the time being keep this, which still needs default expectations
#    Comment out initially
#    ethnicity_by_16_grouping=patients.with_ethnicity_from_sus(
#    returning="group_16",
#    use_most_frequent_code=True,
#    )

)

# #   This is the parentheses that should be closing the study definition. But it is still giving problems with following code. 

#############
#  Measure  #
############# 

#    Section to include if needed for further development
#    This section
#    https://github.com/opensafely/SRO-pulse-oximetry/blob/master/analysis/study_definition.pyof a repository has
#    some very good examples of application of measures at the data extraction stage, as per below.
#    Note that extracting measures like simplifies work upstream, but does not allow to develop/apply Python capabilities to
#    the extent that "rawer" data would
#


measures = [
   

       Measure(
           id="PSA_test_total",
           numerator="had_PSA_test",
           denominator="population",
           group_by=["population"]
       ),


    #2021/10/20 - commented out to minimise outputs, though working
    #    Measure(
    #         id="PSA_test_by_nuts1_region",
    #         numerator="had_PSA_test",
    #         denominator="population",
    #         group_by=["region"]
    #     ),


    #   Measure(
    #        id="PSA_test_by_IMD",
    #        numerator="had_PSA_test",
    #        denominator="population",
    #        group_by=["imd"],
    #    ),

    #2021/10/20 - commented out to minimise outputs, though working
    #   Measure(
    #        id="PSA_test_by_age_group",
    #        numerator="had_PSA_test",
    #        denominator="population",
    #        group_by=["age_group"],
    #    ),






       Measure(
           id="PSA_test_long_total",
           numerator="had_PSA_test_long",
           denominator="population",
           group_by=["population"]
       ),


    #    When tried to run the two measures below got two errors:
    #    1. For all measures the month 2021-02 was absent (even if it was in the source data)
    #    2. A message "Usecols do not match columns, columns expected but not found: ['had_PSA_test_long']"
    #         Measure(
    #         id="PSA_test_long_by_nuts1_region",
    #         numerator="had_PSA_test_long",
    #         denominator="population",
    #         group_by=["region"]
    #     ),



    #   Measure(
    #        id="PSA_test_long_by_age_group",
    #        numerator="had_PSA_test_long",
    #        denominator="population",
    #        group_by=["age_group"]
    #    ),



]


# Latest error while running code
#       File "/app/cohortextractor/study_definition.py", line 63, in to_file
#         df = self.make_df_from_expectations(expectations_population)
#       File "/app/cohortextractor/study_definition.py", line 293, in make_df_from_expectations
#         self.validate_category_expectations(
#       File "/app/cohortextractor/study_definition.py", line 350, in validate_category_expectations
#         defined = set(return_expectations["category"]["ratios"].keys())
#     TypeError: 'NoneType' object is not subscriptable
#
#Suggested solution here: https://blog.finxter.com/python-typeerror-nonetype-object-is-not-subscriptable
#No square brackets practically anywhere