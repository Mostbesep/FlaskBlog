from app import db
from flask import (abort, flash, redirect, render_template, request, session,
                   url_for)
from mod_blog.forms import Createpostform
from mod_blog.models import Post
from mod_users.forms import Loginform
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
