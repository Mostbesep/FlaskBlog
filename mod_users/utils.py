import random

from flask import url_for
from app import redis, mail

def add_to_redis(user,mode):
    token = random.randint(10000,99999)
    name = f'{user.id}_{mode.lower()}'
    redis.set(name=name, value=token, ex=14400)
    return token


def get_from_redis(user, mode):
    name = f'{user.id}_{mode.lower()}'
    return redis.get(name=name)

def delete_from_redis(user,mode):
    name = f'{user.id}_{mode.lower()}'
    redis.delete(name)

def send_signup_message(user,token):
    url = {url_for('users.confirm_registeration', email=user.email, token=token, _external=True)}
    sender = '?????????@gmail.com'
    recipients = [user.email]
    subject = 'flask blog | Registeration Confirm'
    body = f'Hello,<br>for active your account click: {url} <a href="{url}">here</a>'
    mail.send_message(sender=sender, recipients=recipients, subject=subject, html=body)
    