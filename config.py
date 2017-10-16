# config.py

class Config(object):
    """
    Common configurations
    """

class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

    # email server
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 465
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True
# MAIL_USERNAME = 'katerak2013@gmail.com'
# MAIL_PASSWORD = 'kthadmin2017#'

# administrator list
ADMINS = ['cate.rakama@gmail.com']
# titicancinoarmas@gmail.com,

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
