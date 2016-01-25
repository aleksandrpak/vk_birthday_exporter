import vk
import icalendar as ic
import pytz
from datetime import datetime, date

USER_ID = 447465

session = vk.Session()
api = vk.API(session)

cal = ic.Calendar()
cal.add('prodid', '-//VK Birthdays//vk.com//')
cal.add('version', '2.0')

for entry in api.users.get(user_ids=api.friends.get(user_id=USER_ID), fields='bdate'):
    if not 'bdate' in entry:
        continue

    event = ic.Event()
    event['uid'] = str(entry['uid']) + '@vk.com'
    event.add('summary', 'Birthday of ' + entry['first_name'] + ' ' + entry['last_name'])

    bvalues = entry['bdate'].split('.')
    day = int(bvalues[0])
    month = int(bvalues[1])
    year = int(date.today().year)

    bdate = datetime(year, month, day, tzinfo=pytz.utc)
    event.add('dtstart', bdate)
    event.add('dtend', bdate)
    event.add('dtstamp', bdate)

    event['rrule'] = ic.vText('FREQ=YEARLY')
    event['sequence'] = ic.vInt(0)
    event['transp'] = ic.vText('TRANSPARENT')

    cal.add_component(event)

f = open('bdate.ics', 'wb')
f.write(cal.to_ical())
f.close()
