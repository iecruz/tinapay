class Config(object):
    DEBUG=False
    TESTING=False
    SECRET_KEY='T\xfe\x1bz\x97\x1a\x84\x1e|\xa4:\x1d\xf8a\x0b\xe9\x06\xd2\xed\xad\xa8v\x99\xa6'
    DB_HOST='localhost'
    DB_USER='postgres'
    DB_PASSWORD='postgres'
    DB_DATABASE='yapanit'

class DevelopmentConfig(Config):
    DEBUG=True

class DevelopmentConfig(Config):
    TESTING=True

class ProductionConfig(Config):
    DB_HOST='ec2-54-217-236-201.eu-west-1.compute.amazonaws.com'
    DB_USER='xnmnsceybattno'
    DB_PASSWORD='f9f5203832a95dddcdac98aff4e83ca33a7b4778f5b87ae89f72364ea08d0da4'    
    DB_DATABASE='d7mq3n8b6u3sfc'
