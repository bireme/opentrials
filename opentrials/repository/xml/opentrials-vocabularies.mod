<!-- ===========================================================================
File: opentrials-vocabularies.mod

OpenTrials: Latin-American and Caribbean Clinical Trial Record XML DTD
DTD Version 1.0: 2011-01-07

Entity definitions used by the opentrials.dtd file.
This file should be generated automatically from controlled vocabulary data
such as those from Vocabulary application.
=========================================================================== -->

<!ENTITY % language.options
    "en|es|fr|pt|other">

<!-- TRDS 12: health condition attributes -->
<!ENTITY % vocabulary.options
    "decs|icd10|other">

<!-- TRDS 13: intervention descriptor attributes -->
<!-- attribute options cannot contain slashes "/" -->
<!ENTITY % interventioncode.options
    "other|device|biologicalvaccine|proceduresurgery|radiation|behavioural|genetics|dietary-supplement|drug">

<!ENTITY % studystatus.options
    "not-yet-recruiting|recruiting|suspended|recruitment-completed|terminated|withdrawn|data-analysis-completed|other">

<!ENTITY % ageunit.options
    "null|years|months|weeks|days|hours">

<!ENTITY % gender.options
    "female|male|both">

<!-- TRDS 15b: study_design attributes -->
<!ENTITY % purpose.options
    "etiological|prognostic|prevention|treatment|other|diagnostic">

<!ENTITY % assignment.options
    "parallel|cross-over|factorial|other|single-group">

<!ENTITY % masking.options
    "single-blind|double-blind|triple-blind|open">

<!ENTITY % allocation.options
    "randomized-controlled|single-arm-study|non-randomized-controlled">

<!-- TRDS 15c -->
<!ENTITY % phase.options
    "na|0|1|1-2|2|2-3|3|4">

<!ENTITY % contacttype.options
    "public|scientific|site">

<!ENTITY % country.options
    "AF|AX|AL|DZ|AS|AD|AO|AI|AQ|AG|AR|AM|AW|AU|AT|AZ|BS|BH|BD|BB|BY|BE|BZ|BJ|BM|BT|BO|BA|BW|BV|BR|IO|BN|BG|BF|BI|KH|CM|CA|CV|KY|CF|TD|CL|CN|CX|CC|CO|KM|CG|CD|CK|CR|CI|HR|CU|CY|CZ|DK|DJ|DM|DO|EC|EG|SV|GQ|ER|EE|ET|FK|FO|FJ|FI|FR|GF|PF|TF|GA|GM|GE|DE|GH|GI|GR|GL|GD|GP|GU|GT|GG|GN|GW|GY|HT|HM|VA|HN|HK|HU|IS|IN|ID|IR|IQ|IE|IM|IL|IT|JM|JP|JE|JO|KZ|KE|KI|KP|KR|KW|KG|LA|LV|LB|LS|LR|LY|LI|LT|LU|MO|MK|MG|MW|MY|MV|ML|MT|MH|MQ|MR|MU|YT|MX|FM|MD|MC|MN|ME|MS|MA|MZ|MM|NA|NR|NP|NL|AN|NC|NZ|NI|NE|NG|NU|NF|MP|NO|OM|PK|PW|PS|PA|PG|PY|PE|PH|PN|PL|pt-BR|PR|QA|RE|RO|RU|RW|BL|SH|KN|LC|MF|PM|VC|WS|SM|ST|SA|SN|RS|SC|SL|SG|SK|SI|SB|SO|ZA|GS|es|LK|SD|SR|SJ|SZ|SE|CH|SY|TW|TJ|TZ|TH|TL|TG|TK|TO|TT|TN|TR|TM|TC|TV|UG|UA|AE|GB|US|UM|UY|UZ|VU|VE|VN|VG|VI|WF|EH|YE|ZM|ZW">

<!ENTITY % trialstatus.options
    "processing|published|archived">

<!ENTITY % study_type.options
    "interventional|observational">
