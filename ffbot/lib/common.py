from HTMLParser import HTMLParser

from ffbot.config import config


def get_comment_replies(thread):
    """
    Get comments that have replied to other users in thread
    :param praw.objects.Submission or str thread: thread
    :returns List of praw.objects.Comment or praw.objects.MoreComment:
        comments that are replies
    """
    answered_comments = []
    if hasattr(thread, 'comments'):
        for comment in thread.comments:
            if len(comment.replies):
                #QUESTION: why do we use _replies here?
                for reply in comment._replies:
                    answered_comments.append(reply)
    return answered_comments


def get_current_threads(subreddit, limit=200):
    """
    Gets the hot threads in a subreddit
    :param praw.objects.Subreddit subreddit: subreddit
    :param int limit:
    :returns List of praw.objects.Submission or str: threads from praw
    """
    current_threads = []
    for submission in subreddit.get_hot(limit=limit):
        current_threads.append(submission)
    return current_threads


def get_number_helped(comment_replies, author):
    """
    Get the number of replies a user has helped others
    :param comment_replies: replies from get_comment_replies
    :param str author: author name
    :returns int: how many times they've helped others
    """
    number_helped = 0
    for reply in comment_replies:
        if reply.author.name == author:
            number_helped += 1
    return number_helped


def get_unanswered_comments(thread, number=1):
    """
    Get comments that have no responses
    :param praw.objects.Submission or str thread: thread from PRAW
    :param int number: Number of replies required to count it as answered
    :returns List of praw.objects.Comment or praw.objects.MoreComment:
        comments that haven't been replied to
    """
    unanswered_comments = []
    if hasattr(thread, 'comments'):
        for comment in thread.comments:
            if len(comment.replies) <= number and comment.banned_by is None:
                unanswered_comments.append(comment)
    return unanswered_comments


def get_wiki_source(subreddit, wiki_name):
    """
    Returns content of a wiki page to be used for a post
    :param praw.objects.Subreddit subreddit: subreddit the wiki is on
    :param str wiki_name: name of the wiki
        e.g. /r/<subreddit>/wiki/ffbot/<wiki_name>
    :returns str: content of the wiki page in markdown format
    """
    content = subreddit.get_wiki_page(
        '%s/%s' % (config.bot_name, wiki_name)).content_md
    if content is None:
        content = "No Wiki Found"
    return HTMLParser().unescape(content)