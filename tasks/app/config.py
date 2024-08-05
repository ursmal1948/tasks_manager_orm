from os import getenv
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------
# DB CONFIGURATION
# ------------------------------------------------------------
DB_USERNAME = getenv('DB_USERNAME', 'user')
DB_PASSOWRD = getenv('DB_PASSWORD', 'user1234')
DB_PORT = getenv('DB_PORT', '3307')
DB_NAME = getenv('DB_NAME', 'db_1')
DB_HOST = getenv('DB_HOST', 'mysql')
DB_URL = f'mysql://{DB_USERNAME}:{DB_PASSOWRD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# ------------------------------------------------------------
# DB TEST CONFIGURATION
# ------------------------------------------------------------

DB_TEST_USERNAME = getenv('DB_TEST_USERNAME', 'user')
DB_TEST_PASSOWRD = getenv('DB_TEST_PASSWORD', 'user1234')
DB_TEST_PORT = getenv('DB_TEST_PORT', '3308')
DB_TEST_NAME = getenv('DB_TEST_NAME', 'db_1')
DB_TEST_HOST = getenv('DB_TEST_HOST', 'mysql')

DB_TEST_URL = f'mysql://{DB_TEST_USERNAME}:{DB_TEST_PASSOWRD}@{DB_TEST_HOST}:{DB_TEST_PORT}/{DB_TEST_NAME}'

# ------------------------------------------------------------
# MAIL CONFIGURATION
# ------------------------------------------------------------
MAIL_SETTINGS = {
    'MAIL_SERVER': getenv('MAIL_SERVER', 'smtp.gmail.com'),
    'MAIL_PORT': int(getenv('MAIL_PORT', 465)),
    'MAIL_USE_SSL': bool(getenv('MAIL_USE_SSL', True)),
    'MAIL_USERNAME': getenv('MAIL_USERNAME', 'ula.malin35@gmail.com'),
    'MAIL_PASSWORD': getenv('MAIL_PASSWORD', 'dmmzadtkkgjteysw'),
}
