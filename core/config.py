class Config(object):
    DEBUG=False
    TESTING=False
    SECRET_KEY='T\xfe\x1bz\x97\x1a\x84\x1e|\xa4:\x1d\xf8a\x0b\xe9\x06\xd2\xed\xad\xa8v\x99\xa6'
    DB_HOST='localhost'
    DB_USER='postgres'
    DB_PASSWORD='root'
    DB_DATABASE='yapanit'

class DevelopmentConfig(Config):
    DEBUG=True
