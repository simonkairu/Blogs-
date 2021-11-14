import unittest
from app.models import Posts
from app import db

class PitchModelTest(unittest.TestCase):
    def setUp(self):
        self.new_post = Posts(title="title", post="content")
        db.session.add(self.new_blog)
        db.session.commit()

    def tearDown(self):
        Posts.query.delete()
        db.session.commit()

    def test_save_blogs(self):
        self.new_post.save_post()
        self.assertTrue(len(Blog.query.all()) > 0)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog.title, 'title')
        self.assertEquals(self.new_blog.post, 'content')