# PSA2021

[View on OpenSAFELY](https://jobs.opensafely.org/prostate-cancer-psa-testing/)

Details of the purpose and any published outputs from this project can be found at the link above.

The contents of this repository MUST NOT be considered an accurate or valid representation of the study or its purpose. 
This repository may reflect an incomplete or incorrect analysis with no further ongoing work.
The content has ONLY been made public to support the OpenSAFELY [open science and transparency principles](https://www.opensafely.org/about/#contributing-to-best-practice-around-open-science) and to support the sharing of re-usable code for other subsequent users.
No clinical, policy or safety conclusions must be drawn from the contents of this repository.


This repository contains configuration and analysis files for the project PSA2021 (formerly opensafely202109). We computed the monthly number of Prostate Specific Antigen (PSA) tests one year before and throughout the COVID-19 pandemic. We used data for the period 1/4/2019 to 30/9/2021, and aggregated it to national (England) and Office of National Statistics (ONS) England Regions' level.

With the main caveats that primary care data was extracted only from SystmOne (EMIS data could not at the time be queried) and tests in other settings (such as Accident and Emergency) were not included, the analysis showed that from July 2020 to September 2021 England and most Regions had monthly PSA tests that did not on average attain the pre-pandemic period (April 2019-March 2020) numbers, and that the number of PSA tests in some Regions where it was close to the pre-pandemic would still not have been sufficient to clear backlogs created by the large reduction in testing in the period April 2020-June 2020.  


You can run this project via [Gitpod](https://gitpod.io) in a web browser by clicking on this badge: [![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-908a85?logo=gitpod)](https://gitpod.io/#https://github.com/PedroOliveira28/opensafely202109)

* There were no publications or public presentations as an outcome of this study. 
* Raw model outputs, including charts, crosstabs, etc, are in `released_outputs/`
* If you are interested in how we defined our variables, take a look at the [study definition](analysis/study_definition.py); this is written in `python`, but non-programmers should be able to understand what is going on there
* If you are interested in how we defined our code lists, look in the [codelists folder](./codelists/).
* Developers and epidemiologists interested in the framework should review [the OpenSAFELY documentation](https://docs.opensafely.org)

# About the OpenSAFELY framework

The OpenSAFELY framework is a Trusted Research Environment (TRE) for electronic
health records research in the NHS, with a focus on public accountability and
research quality.

Read more at [OpenSAFELY.org](https://opensafely.org).

# Licences
As standard, research projects have a MIT license. 
