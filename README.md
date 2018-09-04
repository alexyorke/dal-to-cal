# dal-to-cal
Generate an iCal-compatible file (events with alarms) for your classes automatically. This script is not affiliated with Dalhousie University in any way, and does not express my views or relations with Dalhousie. No warranty is expressed or implied.

![image](https://i.imgur.com/nbg32Qg.jpg)

This program converts your Dalhousie class schedule into a calendar format for your phone or computer.

## How to use

1. Log into Bluenose (via SSH)

2. Run this command in bluenose: `bash <(curl -s https://raw.githubusercontent.com/alhexyorke/dal-to-cal/master/setup.sh)`

3. Follow the on-screen instructions

This script generates events for all courses (even conflicting ones.) However, when importing the events into your calendar, it will be clear that the classes conflict (as shown on the calendar.) This has the positive side effect of showing you exactly which course conflicts with which one, and at what time.
