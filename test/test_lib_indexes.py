import unittest
import time

from ducks import MockComment, MockSubmission
from mock_templates import sub1_leader_index, sub1_unanswered_index, \
    sub2_leader_index, sub2_unanswered_index

from ffbot.lib import create_leader_index, create_unanswered_index


class TestLibIndexes(unittest.TestCase):
    def setUp(self):
        self.number_of_comments = 25
        self.number_of_sub1_replies = 10
        self.number_of_sub2_replies = 0
        self.comment = MockComment(
            number_of_replies=self.number_of_sub1_replies)
        self.unanswered_comment = MockComment(
            number_of_replies=self.number_of_sub2_replies,
            permalink='UNANSWERED COMMENT PERMALINK',
            created=str(int(time.time())))
        self.submission = MockSubmission(
            number_of_comments=self.number_of_comments,
            mock_comment=self.comment)
        self.submission2 = MockSubmission(
            number_of_comments=self.number_of_comments,
            mock_comment=self.unanswered_comment)

    def test_create_leader_index_sub1(self):
        leader_index = create_leader_index(self.submission)
        self.assertEqual(sub1_leader_index, leader_index)

    def test_create_leader_index_sub2(self):
        leader_index = create_leader_index(self.submission2)
        self.assertEqual(sub2_leader_index, leader_index)

    def test_create_unanswered_index_sub1(self):
        unanswered_index = create_unanswered_index(self.submission)
        self.assertEqual(sub1_unanswered_index, unanswered_index)

    def test_create_unanswered_index_sub2(self):
        unanswered_index = create_unanswered_index(self.submission2)
        self.assertEqual(sub2_unanswered_index, unanswered_index)

    def tearDown(self):
        pass
