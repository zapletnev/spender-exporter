#!/usr/bin/python

import sys
import subprocess
import json
import datetime
import calendar
import types
import re

if len(sys.argv) < 4 or len(sys.argv) > 5:
    print('Error: invalid format. Please use: ./spender.py login password 01-2017 12-2017')
    sys.exit()

login = sys.argv[1]
password = sys.argv[2]

# Auth
print('https://spender.me/aut/check')
process = subprocess.Popen("curl --silent --output /dev/null --cookie-jar - 'https://spender.me/aut/check' " + 
                        "-H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' " + 
                        "--data 'login={}&pass={}' | grep PHPSESSID".format(login, password), stdout=subprocess.PIPE, stderr=None, shell=True)

output = re.split(r'\t+', process.communicate()[0])
phpsession_id = output[len(output) - 1].strip()

# Start and end dates
start_date = datetime.datetime.strptime(sys.argv[3], "%m-%Y").date()
if len(sys.argv) == 5:
    end_date = datetime.datetime.strptime(sys.argv[4], "%m-%Y").date()
else:
    end_date = start_date

if end_date < start_date:
    print('Error: start date should be less than end date')
    sys.exit()

# Spender.me service
def get_spener_expenses(date):
    #print('{}-{}'.format(date.month, date.year))
    from_date_str = '01-{:02}-{}'.format(date.month, date.year)
    to_date_str = '{}-{:02}-{}'.format(calendar.monthrange(date.year, date.month)[1], date.month, date.year)
    print('https://spender.me/ajax/stat?date_from={}&date_to={}'.format(from_date_str, to_date_str))
    output = subprocess.check_output([
        'curl', 'https://spender.me/ajax/stat?date_from={}&date_to={}'.format(from_date_str, to_date_str), 
        '-H', 'Cookie: PHPSESSID={};'.format(phpsession_id)
    ])
    data = json.loads(output)
    return data

# Parsing
months = []
current_date = start_date
while current_date <= end_date:
    data = get_spener_expenses(current_date)
    
    expenses_dict = {}
    month_dict = {}
    month_dict['expenses'] = expenses_dict
    month_dict['month'] = '{:02}-{}'.format(current_date.month, current_date.year)
    months.append(month_dict)

    balance = 0
    if type(data['diagram1']) != types.BooleanType:
        for d in data['diagram1']:
            expenses_dict[d['category']] = d['value']
            balance = balance + d['value']
        #month_dict['balance'] = balance

    if current_date.month == 12:
        current_date = current_date.replace(month=1, year=current_date.year+1)
    else:
        current_date = current_date.replace(month=current_date.month+1)

with open('data.json', 'w') as outfile:
    json.dump(months, outfile)