#!/bin/bash
mkdir bkp
../manage.py dumpdata --indent=2 assistance > bkp/assistance.json
../manage.py dumpdata --indent=2 registration > bkp/registration.json
../manage.py dumpdata --indent=2 repository > bkp/repository.json
../manage.py dumpdata --indent=2 reviewapp > bkp/reviewapp.json
../manage.py dumpdata --indent=2 tickets > bkp/tickets.json
../manage.py dumpdata --indent=2 vocabulary > bkp/vocabulary.json
../manage.py dumpdata --indent=2 -n -e assistance -e registration -e repository -e reviewapp -e tickets -e vocabulary -e contenttypes > bkp/other.json
cd ../static/
tar czvf attachments.tgz attachments/
cd ../tools/
mv ../static/attachments.tgz bkp/
tar czvf bkp.tgz bkp/



