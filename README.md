# dal-to-cal
Generate an iCal-compatible file (in .ics format) for your classes automatically. All you need to do is load the file into your Calendar program (e.g. Outlook, Calendar, Android, iPhone, Google Calendar, etc.) and all of your classes will appear with their times and dates! Huzzah! The calendar below was 100% completely automated by `dal-to-cal.`

This script is not affiliated with Dalhousie University in any way, and does not express my views or relations with Dalhousie. No warranty is expressed or implied.

![image](https://i.imgur.com/nbg32Qg.jpg)

## How to use

1. Log into Bluenose (via SSH)

2. Run this command in bluenose: `bash <(curl -s https://raw.githubusercontent.com/alhexyorke/dal-to-cal/master/setup.sh)`

3. Follow the on-screen instructions

This script generates events for all courses (even conflicting ones.) However, when importing the events into your calendar, it will be clear that the classes conflict (as shown on the calendar.) This has the positive side effect of showing you exactly which course conflicts with which one, and at what time.

## FAQ

### I don't have a clue what you're talking about but it looks cool. How do I make my own schedule?

Snag a computer science student and get them to help you with it. Some might be hanging out in the Goldberg building, but they are afraid of loud noises, so don't scare them.

### How do I import this file into Google Calendar?

Go to https://calendar.google.com/calendar/r/settings/export then click on "Select a file from your computer." Select the `dal_schedule.ics` file that you downloaded, then import it. It's recommended that you create a new calendar to import the events into, in case you have to change your classes later (and don't want to manually delete all of the events.)
