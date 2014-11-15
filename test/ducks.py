from ffbot.config import config


class MockAuthor(object):
    """
    A mock Author object
    """
    def __init__(self, author_name):
        self.name = author_name


class MockComment(object):
    """
    A mock Comment object

    :param int number_of_replies: the number of reply objects to create
    :param str or None banned_by: the username that banned this comment author
    """
    def __init__(self, number_of_replies=0, banned_by=None, author=
                 MockAuthor('default_mock_author'), permalink='', created=''):
        self.banned_by = banned_by
        self.author = author
        self.permalink = permalink
        self.created = created
        self.replies = []
        for _ in range(number_of_replies):
            self.replies.append(MockReply(mock_author=self.author))
        self._replies = self.replies


class MockMoreComments(object):
    """
    A mock MoreComments object
    """
    def __init__(self):
        pass


class MockReply(object):
    """
    A mock Reply object
    """
    def __init__(self, mock_author=None):
        self.author = mock_author


class MockSubmission(object):
    """
    A mock Submission object

    :param int number_of_comments: the number of comment objects to create
    :param MockComment mock_comment: the comment object to create with
    """
    def __init__(self, number_of_comments=0, mock_comment=None):
        self.comments = []
        for _ in range(number_of_comments):
            self.comments.append(mock_comment)


class MockSubreddit(object):
    """
    A mock Subreddit object

    :param int number_of_submissions: the number of submission objects to create
    :param MockSubmission mock_submission: the submission object to create with
    """
    def __init__(self, number_of_submissions=0, mock_submission=None):
        self.submissions = []
        for _ in range(number_of_submissions):
            self.submissions.append(mock_submission)

    def get_hot(self, limit=0):
        if len(self.submissions) > limit:
            upper_bound = len(self.submissions)
        else:
            upper_bound = limit
        return self.submissions[:upper_bound]

    def get_wiki_page(self, wiki_name):
        if '%s/wiki_test_data' % config.bot_name == wiki_name:
            return MockWikiPage(content_md="PASS")
        elif '%s/wiki_test_html_unescape' % config.bot_name == wiki_name:
            return MockWikiPage(content_md=
                                '&lt;img src=&quot;https://38.media.tumblr.com/'
                                '98b9454a8e9b591e91a0f98d3dcc3443/'
                                'tumblr_nf1vf6IgPz1s0hg4lo1_500.gif&quot;&gt;')
        else:
            return MockWikiPage()


class MockWikiPage(object):
    """
    A mock WikiPage object

    :param str content_md: the markdown wiki content to return
    """
    def __init__(self, content_md=None):
        self.content_md = content_md