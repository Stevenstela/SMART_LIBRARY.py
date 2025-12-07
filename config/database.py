import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        dbname="smart_library",
        user="postgres",        # change if you set a different user
        password="STEVRINA", # change to whatever you set during install
        host="localhost",
        port="5432",
        cursor_factory=RealDictCursor
    )