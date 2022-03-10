from flask import flash, request , render_template
from sqlalchemy.exc import IntegrityError  #plan b for prevent register old: user sqlachemy IntegrityError

from app import db
from . import users
from .forms import Registerform
from .models import User
from .utils import add_to_redis, send_signup_message, get_from_redis, delete_from_redis

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
        # old_user = User.query.filter(User.email.ilike(form.email.data)).first() #plan a for prevent register old user check in database
        # if old_user:                                                            #plan a for prevent register old user check in database
        #     flash('email is in use.', category='error')                         #plan a for prevent register old user check in database
        #     return render_template('/users/register.html', form = form)         #plan a for prevent register old user check in database
        new_user = User()
        new_user.full_name = form.full_name.data
        new_user.email = form.email.data
        new_user.set_password(form.password.data)
        # db.session.add(new_user)                                                #plan a for prevent register old user check in database
        # db.session.commit()                                                     #plan a for prevent register old user check in database   
        try:                                                      # plan b for prevent register old: user sqlachemy IntegrityError     
            db.session.add(new_user)                                               
            db.session.commit()
            flash('you created your account successfully.', category='success')
            token = add_to_redis(new_user,'register')
            send_signup_message(new_user, token)     
        except IntegrityError: # if user is aleardy registered    # plan b for prevent register old: user sqlachemy IntegrityError
            db.session.rollback()                                 # plan b for prevent register old: user sqlachemy IntegrityError
            flash('email is in use.', category='error')           # plan b for prevent register old: user sqlachemy IntegrityError
    return render_template('/users/register.html', form = form)


@users.route('/confirm/')
def confirm_registeration():
    email = request.args.get('email')
    token = request.args.get('token')
    
    user = User.query.filter(User.email.ilike(email)).first()
    if not user:
        return 'user not found!'
    if user.active:
        return 'user already activated!!'
    
    token_from_redis = get_from_redis(user=user,mode='register') # this is a byte string and should be convert to normal string
    
    if not token_from_redis:
        return 'wrong or expired token!'
    
    if token != token_from_redis.decode('UTF-8'):
        return 'wrong or expired token!'
    
    user.active = True
    db.session.commit()
    
    delete_from_redis(user,'register')
    return '1'
    