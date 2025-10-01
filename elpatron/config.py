class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'tu-clave-secreta'
    SERVER_NAME = 'localhost'
    PREFERRED_URL_SCHEME = 'https'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True