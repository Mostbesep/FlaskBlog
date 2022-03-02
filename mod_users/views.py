from flask import flash, request , render_template
from app import db
from . import users
from .forms import Registerform
from .models import User

@users.route('/register/', methods=['GET', 'POST'])
def register():
    form = Registerform(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('/users/register.html', form = form)
        if not form.password.data == form.confirm_password.data:
            error_message = 'password and confirm password does not match'
            form.password.errors.append(error_message)
            form.confirm_password.errors.append(error_message)
        new_user = User()
        new_user.full_name = form.full_name.data
        new_user.email = form.email.data
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('you created your account successfully.', category='success')
    return render_template('/users/register.html', form = form)
