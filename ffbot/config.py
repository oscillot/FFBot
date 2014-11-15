import time

__configuration = {
    # Please consider all fields case-sensitive
    
    # Credentials:
    ## BE SURE NOT TO COMMIT YOUR CREDENTIALS!
    'bot_name': '',
    'bot_pw': '',

    # Configure Post:
    'subreddit_name': '',
    # Wiki to use: e.g. sub/wiki/ffbot/<wiki_name>
    # This is what the bot will pull into the body of the post
    'wiki_name': '',
    # Set this to False if you don't want a leaderboard
    'use_leaderboard': True,
    # Set this to False if you don't want an index
    'use_index': True,
    'date_format': '%m/%d/%Y',
    # Thread title will have date_format appended
    # e.g. "%s %s" % (thread_title, current_date)
    'thread_title': '',

    ## BELOW SETTING REQUIRE MOD PERMISSION!

    # Thread flair:
    # Set use_flair to True if you want flair
    # flair_css and flair_text are then required
    # BOT NEEDS FLAIR MOD PERMISSION
    'use_flair': False,
    'flair_css': '',
    'flair_text': '',
    
    # Stickied: 
    # Set to True if you want the thread stickied
    # BOT NEEDS POST MOD PERMISSION
    'sticky_thread': False
}


class Configured():
    def __init__(self, config_dict):
        self.bot_name = config_dict['bot_name']
        self.bot_pw = config_dict['bot_pw']
        self.subreddit_name = config_dict['subreddit_name']
        self.wiki_name = config_dict['wiki_name']
        self.use_leaderboard = config_dict['use_leaderboard']
        self.use_index = config_dict['use_index']
        self.date_format = config_dict['date_format']
        self.thread_title = config_dict['thread_title']
        self.use_flair = config_dict['use_flair']
        self.flair_css = config_dict['flair_css']
        self.flair_text = config_dict['flair_text']
        self.sticky_thread = config_dict['sticky_thread']
            
        self.thread_title = '%s %s' % (self.thread_title,
                                       time.strftime(self.date_format))

config = Configured(__configuration)