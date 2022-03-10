import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS',False)
    SECRET_KEY = os.getenv('SECRET_KEY')
    REDIS_SERVER_URL= os.getenv('REDIS_SERVER_URL')



class Development(Config):
    DEBUG=True


class Production(Config):
    DEBUG=False


