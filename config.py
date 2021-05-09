import os
basedir = os.path.abspath(os.path.dirname(__file__))


PASSWORD ="meow"
PUBLIC_IP_ADDRESS ="34.94.90.49"
DBNAME ="nlrt_db"
PROJECT_ID ="nlrt-311223"
INSTANCE_NAME ="nlrt"
REGION="us-west2"

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'meowmeow'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{REGION}:{INSTANCE_NAME}"
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{REGION}:{INSTANCE_NAME}"