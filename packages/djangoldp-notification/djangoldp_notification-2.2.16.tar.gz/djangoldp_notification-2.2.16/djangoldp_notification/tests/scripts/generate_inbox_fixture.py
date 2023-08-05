import json
import argparse
from pathlib import Path
from copy import deepcopy
from datetime import datetime

'''
A script which generates and outputs placeholder notifications attached to a parametrised user, output 
into a parameterised file (json), which can be used as a Django fixture or imported into a live database
e.g. python manage.py loaddata fixture.json
for help run python generate_inbox_fixture.py -h
'''

# starting from offset ensures that existing users etc are not disturbed
parser = argparse.ArgumentParser(description='generates and outputs random test data, into a file used by the performance unit tests')
parser.add_argument(dest='count', metavar='N', type=int, help='the number of users (and projects) to generate')
parser.add_argument(dest='user', metavar='U', type=str, help='the primary key of the user whose inbox should store the notifications')
parser.add_argument('--offset', dest='offset', type=int, default=100, help='an offset to start primary keys at (should be larger than the largest pre-existing project/user primary key)')
parser.add_argument('-f', dest='file_dest', type=str, default="../fixtures/inbox.json", help='the file destination to write to')

args = parser.parse_args()
count = args.count
user = args.user
OFFSET = args.offset

notification_template = {
    'model': 'djangoldp_notification.notification',
    'pk': 0,
    'fields': {
        'user': user,
        'author': 'Test',
        'object': 'http://localhost:8000/users/admin/',
        'type': 'Update',
        'summary': 'Test',
        'date': str(datetime.date(datetime.now()))
    }
}

fixture = list()
for i in range(count):
    notification = deepcopy(notification_template)
    notification['pk'] = OFFSET + i
    fixture.append(notification)

with open(Path(__file__).parent / args.file_dest, 'w') as output:
    json.dump(fixture, output)

print(str(count))
