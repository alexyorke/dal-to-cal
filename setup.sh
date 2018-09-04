#!/bin/bash
echo "Preparing dal-to-cal, please wait..."
git clone https://github.com/alhexyorke/dal-to-cal
cd dal-to-cal
pip3 install --user -r requirements.txt
python3 dal-to-cal.py
