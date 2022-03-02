from flask import flash, request , render_template
#from sqlalchemy.exc import IntegrityError                                 plan b for prevent register old: user sqlachemy IntegrityError

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
        old_user = User.query.filter(User.email.ilike(form.email.data)).first() #plan a for prevent register old user check in database
        if old_user:                                                            #plan a for prevent register old user check in database
            flash('email is in use.', category='error')                         #plan a for prevent register old user check in database
            return render_template('/users/register.html', form = form)         #plan a for prevent register old user check in database
        new_user = User()
        new_user.full_name = form.full_name.data
        new_user.email = form.email.data
        new_user.set_password(form.password.data)
        # try:                                                                plan b for prevent register old: user sqlachemy IntegrityError     
        db.session.add(new_user) #                                                 
        db.session.commit()
        flash('you created your account successfully.', category='success')
        # except IntegrityError: # if user is aleardy registered              plan b for prevent register old: user sqlachemy IntegrityError
        #     db.session.rollback()                                           plan b for prevent register old: user sqlachemy IntegrityError
        #     flash('email is in use.', category='error')                     plan b for prevent register old: user sqlachemy IntegrityError
    return render_template('/users/register.html', form = form)
