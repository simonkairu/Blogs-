from flask import render_template, redirect, url_for,abort,request,flash
from . import main
from flask_login import login_required, current_user
from .forms import UpdateProfile, BlogForm
from .. import db, photos
from ..models import User, Posts, Comments
from ..requests import get_quotes


@main.route('/')
@main.route('/Home')
def index():
    quote = get_quotes()
    title = "Home - Welcome to Blogs."
    return render_template('index.html', title=title, quote=quote)


@main.route('/blogs')
def blogs():
    posts = Posts.query.all()
    title = "Blogs - Welcome to Blogs."
    return render_template('blogs.html', posts = posts, title=title)

@main.route('/add_blog', methods=["GET","POST"])
@login_required
def add_blog():
    form = BlogForm()
    
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        user = current_user._get_current_object().id
        new_blog_object = Posts(user_id=user, title=title, post=post)
        new_blog_object.save_post()
        return redirect(url_for('main.blogs'))
    
    title = "Add Blog - Welcome to Blogs."
    return render_template('add_blog.html', title=title, blog_form=form)

    
@main.route('/user/<uname>')
def profile(uname):
    title = "Profile - Welcome to Blogs."
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, title=title)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    title = "Update Profile - Welcome to Blogs."
    
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form, title=title)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route('/comments/<int:posts_id>', methods=['GET','POST'])
@login_required
def new_comment(posts_id):
    title = "Comment - Welcome to Blogs."
    form = CommentsForm()
    posts = Posts.query.get(posts_id)
    comment = Comments.query.filter_by(post_id=posts_id).all()
    if form.validate_on_submit():
        comments = form.comment.data
        
        post_id = posts_id
        user_id = current_user._get_current_object().id
        new_comment= Comments(comments=comments,posts_id=post_id, user_id=user_id)
        new_comment.save_comment()      
       
        return redirect(url_for('main.new_comment', posts_id=post_id))
    
    return render_template('comments.html', form=form, comment=comment, posts_id=post_id,posts=posts, title=title)

