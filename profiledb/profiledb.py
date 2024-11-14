from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv(override=True)

class ProfileDatabase:
    _instance = None
    _engine = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProfileDatabase, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # Load database credentials from environment variables
        self.server = os.getenv('PROFILEDB_SERVER')
        self.database = os.getenv('PROFILEDB_DATABASE')
        self.username = os.getenv('PROFILEDB_USERNAME')
        self.password = os.getenv('PROFILEDB_PASSWORD')
        self.port = os.getenv('PROFILEDB_PORT')
        self.connect()

    def connect(self):
        try:
            connection_string = f"mysql+pymysql://{self.username}:{self.password}@{self.server}:{self.port}/{self.database}"
            ProfileDatabase._engine = create_engine(connection_string)
            print("ProfileDB connection successful!")
        except SQLAlchemyError as e:
            print(f"Error connecting to ProfileDB: {e}")
            exit(0)

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            cls()
        return cls._engine

    @classmethod
    def close_connection(cls):
        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None
            print("ProfileDB connection closed.")

class BaseProfileTable:
    def __init__(self):
        self.engine = ProfileDatabase.get_engine()

    def execute_query(self, query, params=None):
        try:
            with self.engine.begin() as conn:
                conn.execute(text(query), params or {})
        except SQLAlchemyError as e:
            print(f"Error executing query on ProfileDB: {e}")

    def fetch_query(self, query, params=None):
        try:
            with self.engine.begin() as conn:
                result = conn.execute(text(query), params or {})
                return result.fetchall()
        except SQLAlchemyError as e:
            print(f"Error fetching query on ProfileDB: {e}")
            return None
