import shutil, sys
import random
import string
import re
from slugify import slugify

# log the user in and get the schedule page
import requests
import getpass
from bs4 import BeautifulSoup

username = input("Enter your Dal NetID (not your CSID!): ")
password = getpass.getpass("Enter your Dal NetID password (won't show up when you're typing): ")

# go to login page to get initial cookies (weird but ok)
s = requests.Session()
res = s.get("https://dalonline.dal.ca/PROD/twbkwbis.P_ValLogin")
cookies = dict(res.cookies)

# try to login
response = s.post('https://dalonline.dal.ca/PROD/twbkwbis.P_ValLogin', cookies=cookies, allow_redirects=True, headers=None, data=("sid=" + username + "&PIN=" + password))

# check credentials
if "Incorrect NetID or password. Please try again." in response.text:
    print("Incorrect password or username! Try again.")
    exit()

# ask user to select term
termHTML = s.post('https://dalonline.dal.ca/PROD/bwskflib.P_SelDefTerm', cookies=cookies, allow_redirects=True, headers=None)

soup = BeautifulSoup(termHTML.text, 'html.parser')
terms = {}
for option in soup.find_all('option'):
    terms[option.text] = option['value']

from pick import pick
title = 'Please choose your term that you would like a schedule for (use arrow keys to select): '
options = list(terms.keys())
option, index = pick(options, title)

term_in_val = terms[option]

schedule = s.post('https://dalonline.dal.ca/PROD/bwskfshd.P_CrseSchdDetl', cookies=cookies, data="term_in=" + term_in_val).text

print("I'm working my magic. Please wait...")

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from ics import Calendar, Event
from dateutil.parser import parse
from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
import datetime as dt
from datetime import timedelta
import pytz

timezone = pytz.timezone('America/Halifax')

scheduleHTML = schedule

# scrape the schedule from the HTML page
soup = BeautifulSoup(scheduleHTML, "html.parser")
scheduleBlocks = soup.find_all('table', {'class': 'datadisplaytable'})
classBlocks = soup.find_all(
    'table',
     {'class': 'datadisplaytable',
      'SUMMARY': 'This table lists the scheduled meeting times and assigned instructors for this class..'})

prevFullClassName = ""
prevInstructor = ""

c = Calendar()

# group together classes and instructors (adjacent blocks in schedule)
for scheduleBlock in scheduleBlocks:
    time = ""
    days = ""
    location = ""
    dates = ""
    fullClassName = scheduleBlock.caption.get_text().strip()
    instructor = scheduleBlock.find_all('td')[3].get_text().strip()

    if (instructor == ""):
        # a lab or a tutorial (a TA probably teaches it)
        instructor = "(A TA on behalf of the course)"

    if (fullClassName == "Scheduled Meeting Times"):
        assignedTimes = scheduleBlock.find_all("tr")
        # remove header
        assignedTimes.pop(0)
        # parse the times that the class runs from and until
        # this can be dates (e.g. Dec 2 to 10th) and days of the week
        # (e.g. Tuesday and Thursday.)
        for assignedTime in assignedTimes:
            assignedSlot = assignedTime.find_all("td")
            time = assignedSlot[1].get_text()
            startTime = time.split(" - ")[0]
            endTime = time.split(" - ")[1]

            days = assignedSlot[2].get_text()
            location = assignedSlot[3].get_text()
            dates = assignedSlot[4].get_text()
            tupleDays = ()
            # convert Dal's day representation to rrules
            # there is no Sunday in Dal's calendar, so S is always Saturday
            dayToTupleLookup = {
                "M": MO,
                "T": TU,
                "W": WE,
                "R": TH,
                "F": FR,
                "S": SA}
            for day in list(days):
                tupleDays = tupleDays + (dayToTupleLookup[day],)
            startingDate = dates.split(" - ")[0]
            endingDate = dates.split(" - ")[1]

            results = rrule(DAILY,
                            dtstart=parse(startingDate),
                            until=parse(endingDate),
                            byweekday=tupleDays,
                            )

            for aResult in results:
                e = Event()
                e.name = prevFullClassName
                # add the time (e.g. 3pm) to the day that the class is on
                finalStartTime = dt.datetime.combine(
                    aResult.date(),
                    dt.datetime.strptime(str(startTime),
                                         "%I:%M %p").time())
                finalEndTime = dt.datetime.combine(
                    aResult.date(),
                    dt.datetime.strptime(str(endTime),
                                         "%I:%M %p").time())

                e.begin = timezone.localize(finalStartTime)
                e.end = timezone.localize(finalEndTime)

                e.description = "Taught by " + prevInstructor
                e.location = location
                c.events.add(e)

    prevInstructor = instructor
    prevFullClassName = fullClassName

with open("dal_schedule.ics", "w") as f:
    f.writelines(c)

timezoneFix = """VERSION:2.0
X-WR-TIMEZONE:America/Halifax
BEGIN:VTIMEZONE
TZID:America/Halifax
X-LIC-LOCATION:America/Halifax
BEGIN:DAYLIGHT
TZOFFSETFROM:-0400
TZOFFSETTO:-0300
TZNAME:ADT
DTSTART:19700308T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:-0300
TZOFFSETTO:-0400
TZNAME:AST
DTSTART:19701101T020000
RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
END:STANDARD
END:VTIMEZONE
"""

# https://stackoverflow.com/questions/10507230/
f = open("dal_schedule.ics", "r")
contents = f.readlines()
f.close()

contents.insert(2, timezoneFix)

f = open("dal_schedule.ics", "w")
contents = "".join(contents)
f.write(contents)
f.close()

print("Finished creating your schedule! You must be excited.")

response = input("Would you like to download your schedule using a web browser? (recommended): type y or n: ")

if (response == "y"):
    chosenTerm = slugify(option)
    random_filename = "dal_sched_" + chosenTerm + ''.join(random.choices(string.ascii_uppercase + string.digits, k=14)) + ".ics"
    calendar_path = "/users/webhome/" + getpass.getuser() + "/" + random_filename
    shutil.move("dal_schedule.ics", calendar_path)
    print("Remember to delete the file from " + calendar_path + " when you are done!")
    print("")
    print("Pssst! It's available at https://web.cs.dal.ca/~" + getpass.getuser() + "/" + random_filename)
else:
    print("No problem. I created the file called dal_schedule.ics which you can download later.")
