import os

from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
port = os.getenv('PORT')
database = os.getenv('DATABASE')

URL = f'mysql://{username}:{password}@localhost:{port}/{database}'
engine = create_engine(URL, echo=True)
