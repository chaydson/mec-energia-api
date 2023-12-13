#!/bin/bash

cat scripts/seed_UFMG.py | ./manage.py shell
cat scripts/seed_UNB.py | ./manage.py shell