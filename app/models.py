from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user 
from . import login_manager
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from flask import session, abort


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255), index=True)
    bio = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    comment = db.relationship('Comments', backref='user', lazy='dynamic')
    post = db.relationship('Posts', backref='user', lazy='dynamic')
 
    
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def save_user(self):
        '''
        Function to save a user
        '''
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"'{self.username}'"

    

class Posts(db.Model):
    '''
    Model class/db table for the post made by the writer
    Args:
        db.Model: Connect our class to the database
    '''
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    post = db.Column(db.Text())
    comments = db.relationship('Comments', backref='comment', lazy='dynamic')
    views = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

    

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"Post '{self.post}', '{self.date_posted}'"

class Comments(db.Model):
    __tablename__ = 'comments' 
    
    id = db.Column(db.Integer, primary_key = True)
    comments = db.Column(db.Text(),nullable=False)
    title = db.Column(db.String(),nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_comments(cls,posts_id):
        comments = Comments.query.filter_by(posts_id=posts_id).all()

        return comments
        
    def __repr__(self):
        return f'Comment{self.comments}'
    
    
class Subscribe(db.Model):
    __tablename__='subscribers'

    id =db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(255),unique=True)

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    def delete_subscriber(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"Subscribe {self.email}"



class Quote:
    """
    class to define Quote Objects
    """
    def __init__(self,quote,author):
        self.quote = quote
        self.author = author

