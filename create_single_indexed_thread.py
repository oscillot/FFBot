import praw,time
from collections import defaultdict
from common import *

"""
Requires Python and PRAW.

to run from command line: python create_single_indexed_thread.py

Please fill out all the below variables to what you want to post. Run this script as a chron job to post at times you want.
I usually have it start at 8am and go until Midnight and run every 15 minutes between then.

This will submit it at 8am and then do an edit every 15 minutes.

Any questions feel free to PM me at /u/tonyg623
"""

# YOUR BOT NAME HERE. CASE PERFECT
bot_name = ""

# YOUR BOT PASSWORD HERE
bot_pw = ""

# SUBREDDIT TO POST TO
sub_name = ""

# WIKI TO USE sub/wiki/ffbot/<wiki_name>. THIS IS WHAT THE BOT WILL PULL INTO THE BODY OF THE POST.
wiki_name = ""

# DATE USED IN THREAD TITLES
current_date = time.strftime("%m/%d/%Y")

# USE LEADERBOARD. SET THIS TO False IF YOU DONT WANT A LEADER BOARD
use_leaderboard = True

# USE INDEX. SET THIS TO False IF YOU DONT WANT A INDEX
use_index = True

# THREAD TITLE
thread_title = "Test %s" % current_date

# THREAD FLAIR. CSS name and flair text required.
# SET use_flair TO False IF YOU DONT WANT A FLAIR
# BOT NEEDS FLAIR MOD PERMISSION
use_flair = True
flair_css = ""
flair_text = ""

# STICK. SET TO False IF YOU DONT WANT IT STICKIED
# BOT NEEDS POST MOD PERMISSION
stick_thread = True

def create_leader_index(thread,length=5):
    """
    This function creates a leaderboard
    :param thread: Thread passed in from PRAW
    :param number: number of rows to show in the leaderboard
    :return: Reddit formatted table
    """
    help_count_thread = defaultdict(int)
    for comment in thread.comments:
        if len(comment.replies) > 0:
            for reply in comment.replies:
                try:
                    help_count_thread[reply.author.name] += 1
                except:
                    # For some reason getting unicode errors. Im lazy here, I just skip it.
                    pass

    user_scores_sortable = []
    for key,value in help_count_thread.iteritems():
        user_scores_sortable.append((value,key))

    user_scores_sortable.sort()
    user_scores_sortable.reverse()
    table = "\n----\n**The following users have helped the most people in this thread:**"
    table += "\n\nUser | # Helped in thread\n-------|:-----:"
    for user in user_scores_sortable[:length]:
        table += '\n%s|%s' % (user[1],user[0])
    return table

def create_unanswered_index(thread,length=20):
    """
    :param thread: Thread passed in from PRAW
    :param length: number of rows to show in the index
    :return: Reddit formatted table of index
    """
    rows = []
    table = "\n\n-------------\n\n **The following posts have gone unanswered in this thread.**\n\n **Would you like your post to be at the top of the list? Remember that the table is sorted by those that have helped the most other users.** \n\n"
    table += '\n\nUser | # Helped in thread | Direct Link'
    table += '\n----|:-----:|----'

    # Get the unanswered comments
    unanswered_comments = get_unanswered_comments(thread,number=0)

    # Calculate the Percentage of Users Answered
    if len(thread.comments) > 0 :
        percent_answered = int((1 - (float(len(unanswered_comments)) / len(thread.comments))) * 100)
    else:
        percent_answered = 100


    comment_replies = get_comment_replies(thread)

    # Go through each unanswered comment and get the author, link, time, and how many others they've helped
    for comment in unanswered_comments:
        try:
            author = comment.author.name

            # Comments in Current Thread
            author_replies = get_numbered_helped(comment_replies,author)

            # Link to Users Comment
            link = comment.permalink

            # Time Stamp
            created = int(comment.created) * -1

            # Append to tuple for free sort
            rows.append((author_replies,created,author,link))
        except:
            # I did this because im lazy and was getting unicode errors.
            pass

    # Free Sort
    rows.sort()

    # Reverse sort so most replies go to top of list
    rows.reverse()

    # Create table and return table in Reddit Formatting
    num_of_unanswered = length
    if len(rows) > 0:
        for row in rows[0:num_of_unanswered]:
            table += "\n%s | %s | [Comment](%s)" % (row[2],row[0],row[3])
        if len(rows) > num_of_unanswered:
            table += '\n**and %d others.**| | ' % (len(rows) - num_of_unanswered)
        table += "\n\n^(This table will be updated every ~15 minutes.)"
        return table + '\n\n**%s%% of users have been helped in this thread**' % percent_answered
    return "\n\n**%s%% of users have been helped in this thread**" % percent_answered


r = praw.Reddit('Indexer by /u/tonyg623')

# Login to Reddit with Praw
r.login(username=bot_name,password=bot_pw)

# Get Subreddit
subreddit = r.get_subreddit(sub_name)

# Get wiki source
# This is used as top of the post. Indexes and Leaderboards are appended to Wiki source
body_content = get_wiki_source(subreddit,wiki_name)

# Get current threads. This returns the limit # of threads based on hot. Edit based on performance and how popular your sub is.
# If a thread isn't return with same title of your title and author , it will create a new one.
current_threads = get_current_threads(subreddit,limit=200)

# Find the thread
found_thread = False
for thread in current_threads:
    if thread.title == thread_title and thread.author.name == bot_name:
        found_thread = thread
        break

# Submit if no thread found. Or edit it.
if not found_thread:
    print 'Submitting %s to %s by %s' % (thread_title,sub_name,bot_name)
    # Submit the thread
    found_thread = subreddit.submit(thread_title,text=body_content)
    # Set flair
    if use_flair:
        found_thread.set_flair(flair_text=flair_text, flair_css_class=flair_css)
    if stick_thread:
        found_thread.sticky()
else:
    print 'Editing %s' % thread_title
    if use_index:
        body_content += create_leader_index(found_thread,length=5)
    if use_leaderboard:
        body_content += create_unanswered_index(found_thread,length=20)
    found_thread.edit(body_content)




