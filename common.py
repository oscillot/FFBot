def get_current_threads(subreddit,limit=200):
    """
    Gets the hot threads in a subreddit
    :param subreddit: suv
    :param limit:
    :return: threads from praw
    """
    current_threads = []
    for submission in subreddit.get_hot(limit=limit):
        current_threads.append(submission)
    return current_threads

def get_wiki_source(subreddit,wiki_name):
    """
    Returns content of a wiki page to be used for a post
    :param subreddit: subreddit the wiki is on
    :param wiki_name: name of the wiki example: /r/<subreddit>/wiki/ffbot/<wiki_name>
    :return: content of the wiki page
    """
    try:
        content = subreddit.get_wiki_page('ffbot/%s' % wiki_name).content_md
        content = content.replace('&lt;','<').replace('&gt;','>')
    except:
        content = "No Wiki Found"
    return content

def get_unanswered_comments(thread,number=1):
    """
    Get comments that have no responses
    :param thread: thread from PRAW
    :param number: Number of replies required to count it as answered
    :return: comments that havent been replied to
    """
    unanswered_comments = []
    if hasattr(thread,'comments'):
        for comment in thread.comments:
            count = 0
            for reply in comment.replies:

                count += 1
            if count <= number and str(comment.banned_by) == 'None':
                unanswered_comments.append(comment)
    return unanswered_comments

def get_comment_replies(thread):
    """
    Get comments that have replied to other users in thread
    :param thread:  thread
    :return: comments that are replies
    """
    answered_comments = []
    if hasattr(thread,'comments'):
        for comment in thread.comments:
            if len(comment.replies) > 0:
                for reply in comment._replies:
                    answered_comments.append(reply)
    return answered_comments

def get_numbered_helped(comment_replies,author):
    """
    Get the number of replies a user has helped others
    :param comment_replies: replies from get_comment_replies
    :param author: author name
    :return: int of how many times they've helped others
    """
    number_helped = 0
    for reply in comment_replies:
        if str(reply.author) == str(author):
            number_helped += 1
    return number_helped

