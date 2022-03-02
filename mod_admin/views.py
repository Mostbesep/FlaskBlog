from flask import session , render_template , request , abort , flash
from mod_users.forms import Loginform
from mod_users.models import User
from . import admin
from .utils import admin_only_view


@admin.route('/')
@admin_only_view #admin login requirement decorator
def index():
    return 'hello from admin index'



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
        return 'Logged in successfully'
    if session.get('role') == 1:
        return 'you are already logged in'        
    return render_template('admin/login.html', form = form, title = 'admin login')