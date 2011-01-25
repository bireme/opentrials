<!-- ===========================================================================
File: opentrials-vocabularies.mod

OpenTrials: Latin-American and Caribbean Clinical Trial Record XML DTD
DTD Version 1.0: 2011-01-18

Entity definitions used by the opentrials.dtd file.
This file should be generated automatically from controlled vocabulary data
such as those from Vocabulary application.
=========================================================================== -->

<!-- TRDS 12: health condition attributes -->
<!ENTITY % vocabulary.options
    "decs|icd10|other">

<!-- TRDS 13: intervention descriptor attributes -->
<!-- attribute options cannot contain slashes "/" -->
<!ENTITY % interventioncode.options
    "drug|device|biologicalvaccine|proceduresurgery|radiation|behavioural|genetics|dietary_supplement|other">

<!ENTITY % requirementstatus.options
    "not_yet_recruiting|recruiting|suspended|recruitment_completed|other|terminated|withdrawn|data_analysis_completed">

<!ENTITY % ageunit.options
    "null|years|months|weeks|days|hours">

<!ENTITY % gender.options
    "female|male|both">

<!-- TRDS 15b: study_design attributes -->
<!ENTITY % purpose.options
    "diagnostic|etiological|prognostic|prevention|treatment|other">

<!ENTITY % assignment.options
    "single-group|parallel|cross-over|factorial|other">

<!ENTITY % masking.options
    "open|single-blind|double-blind|triple-blind">

<!ENTITY % allocation.options
    "non-randomized-controlled|randomized-controlled|single-arm-study">

<!-- TRDS 15c -->
<!ENTITY % phase.options
    "null|1|1-2|2|2-3|3|4|0">

<!ENTITY % contacttype.options
    "public|scientific|site">

<!ENTITY % country.options
    "AF|AX|AL|DZ|AS|AD|AO|AI|AQ|AG|AR|AM|AW|AU|AT|AZ|BS|BH|BD|BB|BY|BE|BZ|BJ|BM|BT|BO|BA|BW|BV|BR|IO|BN|BG|BF|BI|KH|CM|CA|CV|KY|CF|TD|CL|CN|CX|CC|CO|KM|CG|CD|CK|CR|CI|HR|CU|CY|CZ|DK|DJ|DM|DO|EC|EG|SV|GQ|ER|EE|ET|FK|FO|FJ|FI|FR|GF|PF|TF|GA|GM|GE|DE|GH|GI|GR|GL|GD|GP|GU|GT|GG|GN|GW|GY|HT|HM|VA|HN|HK|HU|IS|IN|ID|IR|IQ|IE|IM|IL|IT|JM|JP|JE|JO|KZ|KE|KI|KP|KR|KW|KG|LA|LV|LB|LS|LR|LY|LI|LT|LU|MO|MK|MG|MW|MY|MV|ML|MT|MH|MQ|MR|MU|YT|MX|FM|MD|MC|MN|ME|MS|MA|MZ|MM|NA|NR|NP|NL|AN|NC|NZ|NI|NE|NG|NU|NF|MP|NO|OM|PK|PW|PS|PA|PG|PY|PE|PH|PN|PL|pt-br|PR|QA|RE|RO|RU|RW|BL|SH|KN|LC|MF|PM|VC|WS|SM|ST|SA|SN|RS|SC|SL|SG|SK|SI|SB|SO|ZA|GS|es|LK|SD|SR|SJ|SZ|SE|CH|SY|TW|TJ|TZ|TH|TL|TG|TK|TO|TT|TN|TR|TM|TC|TV|UG|UA|AE|GB|US|UM|UY|UZ|VU|VE|VN|VG|VI|WF|EH|YE|ZM|ZW">

<!ENTITY % trialstatus.options
    "processing|published|archived">

<!ENTITY % study_type.options
    "interventional|observational">

<!ENTITY % institution_type.options
    "clinical_research_network|federal_agency|industry|ministery_of_health|non-governamental_agency|state_research_support_foundation|other">
