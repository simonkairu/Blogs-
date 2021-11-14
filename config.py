import os


class Config:
    """
    General configuration class
    """
    SECRET_KEY = 'qGkdxkNgQcOy3pAOrTi0YQ'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:access@localhost/blog'
    QUOTES_API_BASE_URL = 'http://quotes.stormconsultancy.co.uk/random.json'
    # email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'simon.mureithi@student.moringaschool.com'
    MAIL_PASSWORD = 'prince070202'



class ProdConfig(Config):
    """
    Production configuration class
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    
    
class DevConfig(Config):
    """
    Development configuration class
    """
    DEBUG = True
    
    
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:access@localhost/blog_test'


config_option = {
    'production': ProdConfig,
    'development': DevConfig,
    'test': TestConfig
}