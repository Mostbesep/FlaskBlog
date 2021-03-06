from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Development
from flask_mail import Mail
from mail_info import mail_settings
from redis import Redis




app = Flask(__name__)
app.config.from_object(Development)
app.config.update(mail_settings)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
redis = Redis.from_url(app.config['REDIS_SERVER_URL'])

from views import index

from mod_admin import admin
from mod_users import users
from mod_blog import blog
from mod_uploads import uploads

app.register_blueprint(admin)
app.register_blueprint(users)
app.register_blueprint(blog)
app.register_blueprint(uploads)
