<!-- file reclac-vocabularies.mod

RECLAC: Latin-American and Caribbean Clinical Trial Record XML DTD
DTD Version 1.0: 2010-03-01

Entity definitions used by the reclac.dtd file.
This file should be generated automatically from controlled vocabulary data
such as those from Vocabulary application.
=========================================================================== -->

<!-- TRDS 12, 13: health condition and intervention descriptor attributes -->
<!ENTITY % vocabulary.options
    "decs|icd10|other">
<!-- attribute options cannot contain slashes "/" -->
<!ENTITY % interventioncode.options
    "drug|device|biological-vaccine|procedure-surgery|radiation|behavioural|
     genetics|dietary-supplement|other">

<!-- TRDS 15b: study_design attributes -->
<!ENTITY % purpose.options
    "diagnostic|etiological|prognostic|prevention|treatment|other">
<!ENTITY % assignment.options
    "single-group|parallel|cross-over|factorial|other">
<!ENTITY % masking.options
    "open|single-blind|double-blind|triple-blind">
<!ENTITY % allocation.options
    "non-randomized-controlled|randomized-controlled|single-arm-study">

<!-- TRDS 15b: study_endpoint attributes -->
<!ENTITY % endpoint.options
    "safety|efficacy|bioequivalence|biodisponibility|
     pharmacokinetics|pharmacodynamics|pharmacogenetics">

<!ENTITY % countrycode.options
    "AF|AX|AL|DZ|AS|AD|AO|AI|AQ|AG|AR|AM|AW|AU|AT|AZ|BS|BH|BD|BB|BY|BE|BZ|BJ|
     BM|BT|BO|BA|BW|BV|BR|IO|BN|BG|BF|BI|KH|CM|CA|CV|KY|CF|TD|CL|CN|CX|CC|CO|
     KM|CG|CD|CK|CR|CI|HR|CU|CY|CZ|DK|DJ|DM|DO|EC|EG|SV|GQ|ER|EE|ET|FK|FO|FJ|
     FI|FR|GF|PF|TF|GA|GM|GE|DE|GH|GI|GR|GL|GD|GP|GU|GT|GG|GN|GW|GY|HT|HM|VA|
     HN|HK|HU|IS|IN|ID|IR|IQ|IE|IM|IL|IT|JM|JP|JE|JO|KZ|KE|KI|KP|KR|KW|KG|LA|
     LV|LB|LS|LR|LY|LI|LT|LU|MO|MK|MG|MW|MY|MV|ML|MT|MH|MQ|MR|MU|YT|MX|FM|MD|
     MC|MN|ME|MS|MA|MZ|MM|NA|NR|NP|NL|AN|NC|NZ|NI|NE|NG|NU|NF|MP|NO|OM|PK|PW|
     PS|PA|PG|PY|PE|PH|PN|PL|PT|PR|QA|RE|RO|RU|RW|BL|SH|KN|LC|MF|PM|VC|WS|SM|
     ST|SA|SN|RS|SC|SL|SG|SK|SI|SB|SO|ZA|GS|ES|LK|SD|SR|SJ|SZ|SE|CH|SY|TW|TJ|
     TZ|TH|TL|TG|TK|TO|TT|TN|TR|TM|TC|TV|UG|UA|AE|GB|US|UM|UY|UZ|VU|VE|VN|VG|
     VI|WF|EH|YE|ZM|ZW">