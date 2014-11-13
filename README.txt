REQUIRES:
Python
Praw - a python library for reddit

to run from command line: python create_single_indexed_thread.py

Please fill out all the variables in create_single_indexed_thread.py to what you want to post. Run this script as a chron job to post at times you want.
I usually have it start at 8am and go until Midnight and run every 15 minutes between then.

This will submit it at 8am and then do an edit every 15 minutes.

I usually run this from jenkins but can be ran from pretty much anything.

Any questions feel free to PM me at /u/tonyg623
