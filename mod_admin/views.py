from flask import session , render_template , request , abort
from mod_users.forms import Loginform
from mod_users.models import User
from . import admin

@admin.route('/')
def index():
    return 'hello from admin index'



@admin.route('/login/' , methods=["GET", 'POST'])
def login():
    form = Loginform(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            abort(400)
        user = User.query.filter(User.email.ilike(f'{form.email.data}')).first() #ilike is a method for compatibility  in databases
        if not user:
            return 'incorrect credentials' , 400
        if not user.check_password(form.password.data):
            return 'incorrect credentials' , 400
        session['email'] = user.email
        session['user_id'] = user.id
        return 'Logged in successfully'
    if session.get('email') is not None:
        return 'you are already logged in'        
    return render_template('admin/login.html', form = form, title = 'admin login')