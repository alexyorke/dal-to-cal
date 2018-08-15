# dal-to-cal
Generate an iCal-compatible file (events with alarms) for your classes automatically. This script is not affiliated with Dalhousie University in any way, and does not express my views or relations with Dalhousie. No warranty is expressed or implied.

![image](https://i.imgur.com/nbg32Qg.jpg)

This program converts your Dalhousie class schedule into a calendar format for your phone or computer. It's a bit hacky but it seems to work fine.

Currently, there are issues with daylight savings time after November 6th. This should be fixed in the next version.

## How to use

1. clone this repo `git clone https://github.com/alhexyorke/dal-to-cal`

2. cd into it `cd dal-to-cal`

3. run `pip install -r requirements.txt`

4. go to https://dalonline.dal.ca/PROD/bwskfshd.P_CrseSchdDetl and sign in with your net id and password

5. go to https://dalonline.dal.ca/PROD/bwskfshd.P_CrseSchdDetl again (as it redirects you to another unrelated page)

6. select the term you would like to generate events for when prompted. If you are not prompted, check in the top right-hand corner to determine which term it is. If it is the wrong term, select the correct term somehow.

7. right-click and select "view source". Copy everything there and paste it into a new text file called `schedule_view_source.txt` in the same folder as this script.

8. run `python3 dal-to-cal.py`. A file called `dal_schedule.ics` will be generated, and can be imported into any calendar program (e.g. Google Calendar, iOS, Android, Samsung, etc.)

This script generates events for all courses (even conflicting ones.) However, when importing the events into your calendar, it will be clear that the classes conflict (as shown on the calendar.) This has the positive side effect of showing you exactly which course conflicts with which one, and at what time.
