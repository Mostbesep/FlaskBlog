from app import db
from flask import (abort, flash, redirect, render_template, request, session,
                   url_for)
from mod_blog.forms import Createpostform , Modifypostform
from mod_blog.models import Post
from mod_users.forms import Loginform , Registerform
from mod_users.models import User
from sqlalchemy.exc import IntegrityError

from . import admin
from .utils import admin_only_view


@admin.route('/')
@admin_only_view #admin login requirement decorator
def index():
    return render_template('admin/index.html')


@admin.route('/login/' , methods=["GET", 'POST'])
def login():
    form = Loginform(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            abort(400)
        user = User.query.filter(User.email.ilike(f'{form.email.data}')).first() #  this object find user email from datebase and get it| ilike is a method for compatibility  in databases
        if not user:
            flash('incorrect password or username', category='error')
            return render_template('admin/login.html', form = form, title = 'admin login')
        if not user.check_password(form.password.data):
            flash('incorrect password or username', category='error')
            return render_template('admin/login.html', form = form, title = 'admin login')
        if not user.is_admin():
            flash('incorrect password or username', category='error')
            return render_template('admin/login.html', form = form, title = 'admin login')
        
        # in this level: so this user logged in whit correct password and username and role is admin

        session['email'] = user.email #hashed along SECRET_KEY so it safe?1-i dont know
        session['user_id'] = user.id #hashed along SECRET_KEY so it safe?
        session['role'] = user.role
        return redirect(url_for('admin.index'))
    if session.get('role') == 1:
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html', form = form, title = 'admin login')


@admin.route('/logout', methods=["GET"])
@admin_only_view
def logout():
    session.clear()
    flash('You logged out successfully.', category='warning')
    return redirect(url_for('admin.login'))


@admin.route('/users/', methods=['GET'])
@admin_only_view
def list_users():
    users = User.query.order_by(User.id.desc()).all() #.order_by(User.id.desc()) : ordering by big to small id,option:asc():iverse
    return render_template('admin/list_users.html', users=users)


@admin.route('/users/new/', methods=['GET'])
@admin_only_view
def get_create_user():
    form = Registerform()
    return render_template('admin/create_user.html', form=form)


@admin.route('users/new/', methods=['POST'])
@admin_only_view
def post_create_user():
    form = Registerform(request.form)
    if not form.validate_on_submit():
        return render_template('admin/create_user.html', form = form)
    if not form.password.data == form.confirm_password.data:
        error_message = 'password and confirm password does not match'
        form.password.errors.append(error_message)
        form.confirm_password.errors.append(error_message)
    old_user = User.query.filter(User.email.ilike(form.email.data)).first()
    if old_user:
        flash('email is in use.', category='error')
        return render_template('admin/create_user.html', form = form)
    new_user = User()
    new_user.full_name = form.full_name.data
    new_user.email = form.email.data
    new_user.set_password(form.password.data)
    db.session.add(new_user) 
    db.session.commit()
    flash('you created user successfully.', category='success')
    return redirect(url_for('admin.list_users'))


@admin.route('/posts/new/', methods=['GET','POST'])
@admin_only_view
def create_post():
    form = Createpostform(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return '1'
        new_post = Post()
        new_post.title = form.title.data
        new_post.content = form.content.data
        new_post.slug = form.slug.data
        new_post.summary = form.summary.data
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Post Created!')
            return redirect(url_for('admin.index'))
        except IntegrityError:
            db.session.rollback()
            flash('Unsuccessful Post', category='error')
            return render_template('admin/create_post.html', form=form)
    return render_template('admin/create_post.html', form=form)


@admin.route('/posts/', methods=['GET'])
@admin_only_view
def list_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('admin/list_posts.html', posts=posts)


@admin.route('posts/delete/<int:post_id>/', methods=['GET'])
@admin_only_view
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted')
    return redirect(url_for('admin.list_posts'))


@admin.route('posts/modify/<int:post_id>/', methods=['GET','POST'])
@admin_only_view
def modify_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = Modifypostform(obj=post)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('admin/modify_post.html', form=form, post=post)
        post.title = form.title.data
        post.content = form.content.data
        post.slug = form.slug.data
        post.summary = form.summary.data
        try:
            db.session.commit()
            flash('Post Modified!')
            return redirect(url_for('admin.list_posts'))
        except IntegrityError:
            db.session.rollback()
            flash('Unsuccessful Modify Post', category='error')
    return render_template('admin/modify_post.html', form=form, post=post)