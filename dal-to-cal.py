try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from ics import Calendar, Event
from dateutil.parser import parse
from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR, SA, SU
import datetime as dt
from bs4 import BeautifulSoup
from datetime import timedelta

scheduleHTML = ""

with open("schedule_view_source.txt", "rb") as scheduleFile:
	for line in scheduleFile:
		scheduleHTML = scheduleHTML + (line.decode(errors='ignore'))

# scrape the schedule from the HTML page
soup = BeautifulSoup(scheduleHTML, "html.parser")
scheduleBlocks = soup.find_all('table', {'class' : 'datadisplaytable'})
classBlocks = soup.find_all('table', {'class': 'datadisplaytable', 'SUMMARY': 'This table lists the scheduled meeting times and assigned instructors for this class..'})

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
			dayToTupleLookup = {"M":MO, "T":TU, "W":WE, "R": TH, "F":FR, "S":SA}
			for day in list(days):
				tupleDays = tupleDays + (dayToTupleLookup[day],)
			startingDate = dates.split(" - ")[0]
			endingDate = dates.split(" - ")[1]

			results = rrule(DAILY,
				dtstart = parse(startingDate),
				until = parse(endingDate),
				byweekday = tupleDays,
			)

			for aResult in results:
				e = Event()
				e.name = prevFullClassName
				# add the time (e.g. 3pm) to the day that the class is on
				finalStartTime = dt.datetime.combine(aResult.date(), dt.datetime.strptime(str(startTime), "%I:%M %p").time())
				finalEndTime = dt.datetime.combine(aResult.date(), dt.datetime.strptime(str(endTime), "%I:%M %p").time())
				e.begin = finalStartTime + timedelta(hours=3)
				e.end = finalEndTime + timedelta(hours=3) #timezone fix
				e.description = "Taught by " + prevInstructor
				e.location = location
				c.events.add(e)

	prevInstructor = instructor
	prevFullClassName = fullClassName

with open("dal_schedule.ics", "w") as f:
	f.writelines(c)

# terrible hack to fix timezone issues (off by three hours)

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

# https://stackoverflow.com/questions/10507230/insert-line-at-middle-of-file-with-python
f = open("dal_schedule.ics", "r")
contents = f.readlines()
f.close()

contents.insert(2, timezoneFix)

f = open("dal_schedule.ics", "w")
contents = "".join(contents)
f.write(contents)
f.close()
