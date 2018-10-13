from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import ContactUs, LoginForm, RegistrationForm, BlogPostCommentForm
from app.models import ContactMessage, User, BlogPost, BlogPostComment
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash ('Invalid uername of password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/contact', methods=['GET', 'POST'])
def contact_us():
    form = ContactUs()
    if form.validate_on_submit():
        contact_message = ContactMessage()
        contact_message.name = form.name.data
        contact_message.email = form.email.data
        contact_message.message = form.message.data
        db.session.add(contact_message)
        db.session.commit()
        flash ('Message Sent')
        return redirect(url_for('index'))
    return render_template('contact_us.html', title = 'Contact is', form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/admin')
@login_required
def adminPanel():
    messages = ContactMessage.query.all()
    return render_template('admin.html', title ='Admin Panel', messages=messages)

@app.route('/blog')
def blog():
    posts = BlogPost.query.all()
    return render_template('blog.html', title = 'Blog', posts=posts)

@app.route('/blog/post/<int:post_id>', methods=['GET', 'POST'])
def blogPost(post_id):
    post = BlogPost.query.filter(BlogPost.id == post_id).first()
    comments = BlogPostComment.query.filter(BlogPostComment.post == post)
    form = BlogPostCommentForm()
    if form.validate_on_submit():
        comment = BlogPostComment()
        comment.name = form.name.data
        comment.comment = form.comment.data
        comment.post = post
        db.session.add(comment)
        db.session.commit()
        flash ('Comment posted')
        return redirect(url_for('blogPost', post_id = post_id))
    return render_template('blog_post.html', title = 'post', post=post, comments=comments, form=form)
