# -*- coding: utf-8 -*-

import csv

from faker import Faker
fake = Faker()

with open('filename', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
