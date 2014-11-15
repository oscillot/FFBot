import praw

from ffbot.config import config

from ffbot.lib.common import get_current_threads, get_wiki_source
from lib import create_leader_index, create_unanswered_index


def main():
    """
    Main workflow
    """
    r = praw.Reddit('Indexer by /u/tonyg623')

    # Login to Reddit with Praw
    r.login(username=config.bot_name, password=config.bot_pw)

    # Get Subreddit
    subreddit = r.get_subreddit(config.sub_name)

    # Get wiki source
    # This is used as top of the post.
    # Indexes and Leaderboards are appended to Wiki source
    body_content = get_wiki_source(subreddit, config.wiki_name)

    # Get current threads.
    # This returns the limit # of threads based on hot.
    # Edit based on performance and how popular your sub is.
    # If a thread isn't returned with same title of your title and author,
    # it will create a new one.
    current_threads = get_current_threads(subreddit, limit=200)

    # Find the thread
    found_thread = False
    for thread in current_threads:
        if thread.title == config.thread_title and \
                thread.author.name == config.bot_name:
            found_thread = thread
            break

    # Submit if no thread found. Or edit it.
    if not found_thread:
        print 'Submitting %s to %s by %s' % (config.thread_title,
                                             config.sub_name,
                                             config.bot_name)
        # Submit the thread
        found_thread = subreddit.submit(config.thread_title, text=body_content)
        # Set flair
        if config.use_flair:
            found_thread.set_flair(flair_text=config.flair_text,
                                   flair_css_class=config.flair_css)
        if config.stick_thread:
            found_thread.sticky()
    else:
        print 'Editing %s' % config.thread_title
        if config.use_index:
            body_content += create_leader_index(found_thread, length=5)
        if config.use_leaderboard:
            body_content += create_unanswered_index(found_thread, length=20)
        found_thread.edit(body_content)

if "__main__" == __name__:
    main()