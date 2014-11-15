import sys
import unittest

from ducks import MockAuthor, MockComment, MockReply, MockSubmission, \
    MockSubreddit
from ffbot.lib import get_comment_replies, get_current_threads, \
    get_number_helped, get_unanswered_comments, get_wiki_source


class TestLibCommon(unittest.TestCase):
    def setUp(self):
        self.number_of_comments = 25
        self.number_of_sub1_replies = 10
        self.number_of_sub2_replies = 2
        self.number_of_submissions = 20
        self.number_of_mcgee_replies = 23
        self.number_of_mcface_replies = 15
        self.number_of_answered_comments = 13
        self.number_of_unanswered_comments = 112
        self.comment = MockComment(
            number_of_replies=self.number_of_sub1_replies)
        self.submission = MockSubmission(
            number_of_comments=self.number_of_comments,
            mock_comment=self.comment)
        self.submission2 = MockSubmission(
            number_of_comments=0)
        self.submissions = [
            MockSubmission(number_of_comments=10, mock_comment=self.comment)
            for _ in range(self.number_of_answered_comments)] + \
            [MockSubmission()
                for _ in range(self.number_of_unanswered_comments)]
        self.subreddit = MockSubreddit(
            number_of_submissions=self.number_of_submissions,
            mock_submission=self.submission)
        self.author1 = MockAuthor('stinkyfacemcgee')
        self.author2 = MockAuthor('stinkybuttmcface')
        self.comment_reply1 = MockReply(self.author1)
        self.comment_reply2 = MockReply(self.author2)

    def test_get_comment_replies(self):
        comment_replies = get_comment_replies(self.submission)
        self.assertEqual(len([self.comment_reply1 for _ in range(
                             self.number_of_comments *
                             self.number_of_sub1_replies)]),
                         len(comment_replies))

    def test_get_current_threads(self):
        current_threads = get_current_threads(self.subreddit)
        self.assertListEqual([self.submission for _ in range(
                              self.number_of_submissions)], current_threads)

    def test_get_number_mcgg_helped(self):
        helped_candidates = [
            self.comment_reply1 for _ in range(
                self.number_of_mcgee_replies)] + \
            [self.comment_reply2 for _ in range(
                self.number_of_mcface_replies)]
        number_mcgee_helped = get_number_helped(helped_candidates,
                                                'stinkyfacemcgee')
        self.assertEqual(self.number_of_mcgee_replies, number_mcgee_helped)

    def test_get_number_mcface_helped(self):
        helped_candidates = [
            self.comment_reply1 for _ in range(
                self.number_of_mcgee_replies)] + \
            [self.comment_reply2 for _ in range(
                self.number_of_mcface_replies)]
        number_mcface_helped = get_number_helped(helped_candidates,
                                                 'stinkybuttmcface')
        self.assertEqual(self.number_of_mcface_replies, number_mcface_helped)

    def test_get_unanswered_comments_limit1(self):
        unanswered_comments = get_unanswered_comments(self.submissions)
        self.assertEqual(0, len(unanswered_comments))

    def test_get_unanswered_comments_no_limit_sub1(self):
        unanswered_comments = get_unanswered_comments(self.submission,
                                                      number=sys.maxint)
        self.assertEqual(self.number_of_comments,
                         len(unanswered_comments))

    def test_get_unanswered_comments_no_limit_sub2(self):
        unanswered_comments = get_unanswered_comments(self.submission2,
                                                      number=sys.maxint)
        self.assertEqual(0, len(unanswered_comments))

    def test_get_wiki_source_passes(self):
        wiki_source = get_wiki_source(self.subreddit, 'wiki_test_data')
        self.assertEqual('PASS', wiki_source, )

    def test_get_wiki_source_no_data(self):
        wiki_source_non_existent = get_wiki_source(self.subreddit,
                                                   'wiki_test_no_data')
        self.assertEqual('No Wiki Found', wiki_source_non_existent)

    def test_get_wiki_source_html_unescaping(self):
        wiki_unescape_correctly = get_wiki_source(self.subreddit,
                                                   'wiki_test_html_unescape')
        self.assertEqual('<img src="https://38.media.tumblr.com/'
                         '98b9454a8e9b591e91a0f98d3dcc3443/'
                         'tumblr_nf1vf6IgPz1s0hg4lo1_500.gif">',
                         wiki_unescape_correctly)

    def tearDown(self):
        pass