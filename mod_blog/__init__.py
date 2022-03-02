from flask import Blueprint



blog = Blueprint('blog', __name__ , '/blog/')

from . import models