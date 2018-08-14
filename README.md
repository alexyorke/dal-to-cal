# dal-to-cal
Generate an iCal-compatible file (events with alarms) for your classes automatically. This script is not affiliated with Dalhousie University in any way, and does not express my views or relations with Dalhousie. No warranty is expressed or implied.

This program converts your Dalhousie class schedule into a calendar format for your phone or computer. It's a bit hacky but it seems to work fine.

## How to use

1. go to https://dalonline.dal.ca/PROD/bwskfshd.P_CrseSchdDetl and sign in with your net id and password

2. go to https://dalonline.dal.ca/PROD/bwskfshd.P_CrseSchdDetl again (as it redirects you to another unrelated page)

3. select the term you would like to generate events for when prompted. If you are not prompted, check in the top right-hand corner to determine which term it is. If it is the wrong term, select the correct term somehow.

4. right-click and select "view source". Copy everything there and paste it into a new text file called `schedule_view_source.txt` in the same folder as this script.

5. run `python3 dal-to-cal.py`. A file called `dal_schedule.ics` will be generated, and can be imported into any calendar program (e.g. Google Calendar, iOS, Android, Samsung, etc.)
