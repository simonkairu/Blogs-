import unittest
from app import db
from app.models import Posts, User, Comments

class TestComment(unittest.TestCase):
    """
    Class that holds all test cases for the Comment model
    """
   
    def setUp(self):
        self.new_comment = Comments(comment='nice')
   
            

    def test_instance(self):
        self.assertEqual(self.new_comment.comment,'nice')
    
        
    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comments.query.all())>0)
    
    def test_get_comment_by_id(self):

        self.new_comment.save_comment()
        got_comment = Comments.get_comment(1)
        self.assertTrue(len(got_comment) > 0)