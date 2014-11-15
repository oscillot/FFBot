from collections import defaultdict
import traceback

from ffbot.lib import get_unanswered_comments, get_comment_replies, \
    get_number_helped

from ffbot.templates import helped_table_header, helped_table_footer, \
    updates_table_insert, unanswered_table_header


def create_leader_index(thread, length=5):
    """
    This function creates a leaderboard
    :param praw.objects.Submission or str thread: Thread passed in from PRAW
    :param int length: number of rows to show in the leaderboard
    :returns str: Reddit formatted table
    """
    help_count_thread = defaultdict(int)
    for comment in thread.comments:
        if len(comment.replies) > 0:
            for reply in comment.replies:
                try:
                    help_count_thread[reply.author.name] += 1
                except UnicodeError:
                    # For some reason getting unicode errors.
                    # Im lazy here, I just skip it.
                    ##Printing so I can see it - Paul
                    traceback.print_exc()

    user_scores_sortable = []
    for key, value in help_count_thread.iteritems():
        user_scores_sortable.append((value, key))
    user_scores_sortable = \
        sorted(reversed([(v, k) for k, v in help_count_thread.items()]))

    table = helped_table_header

    for user in user_scores_sortable[:length]:
        table += '\n%s|%s' % (user[1], user[0])
    return table


def create_unanswered_index(thread, length=20):
    """
    :param praw.objects.Submission or str thread: Thread passed in from PRAW
    :param int length: number of rows to show in the index
    :returns str: Reddit formatted table of index
    """
    rows = []
    table = unanswered_table_header

    # Get the unanswered comments
    unanswered_comments = get_unanswered_comments(thread, number=0)

    # Calculate the Percentage of Users Answered
    if len(thread.comments) > 0:
        percent_answered = int((1 - (float(len(unanswered_comments)) /
                                     len(thread.comments))) * 100)
    else:
        percent_answered = 100

    comment_replies = get_comment_replies(thread)

    # Go through each unanswered comment and get the author, link, time, and
    # how many others they've helped
    for comment in unanswered_comments:
        try:
            author = comment.author.name

            # Comments in Current Thread
            author_replies = get_number_helped(comment_replies, author)

            # Link to Users Comment
            link = comment.permalink

            # Time Stamp
            created = -int(comment.created)

            # Append to tuple for free sort
            rows.append((author_replies, created, author, link))
        except UnicodeError:
            # I did this because im lazy and was getting unicode errors.
            ##Printing so I can see it - Paul
            traceback.print_exc()

    # Free Sort
    rows.sort()

    # Reverse sort so most replies go to top of list
    rows.reverse()

    # Create table and return table in Reddit Formatting
    num_of_unanswered = length
    if len(rows) > 0:
        for row in rows[0:num_of_unanswered]:
            table += '\n%s | %s | [Comment](%s)' % (row[2], row[0], row[3])
        if len(rows) > num_of_unanswered:
            table += '\n**and %d others.**| |' % \
                     (len(rows) - num_of_unanswered)
        table += updates_table_insert + helped_table_footer % percent_answered
        return table
    return helped_table_footer % percent_answered