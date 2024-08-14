# Import necessary libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
class DatabaseConfig:
    """Class to hold database configuration."""
    def __init__(self):
        self.name = os.getenv("DATABASE_NAME")
        self.user = os.getenv("DATABASE_USER")
        self.password = os.getenv("DATABASE_PASSWORD")
        self.host = os.getenv("DATABASE_HOST", "localhost")
        self.port = os.getenv("DATABASE_PORT", "5432")
        
    @property
    def connection_url(self):
        """Returns the database connection URL."""
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

# Initialize Database Configuration
db_config = DatabaseConfig()

# Initialize Database Engine
database_engine = create_engine(db_config.connection_url)

# Initialize a SessionMaker instance
DatabaseSession = sessionmaker(bind=database_engine)

# Function to initialize a new database session
def create_database_session():
    """Creates and returns a new database session."""
    return DatabaseSession()

# Initialize a database session using the function
database_session = create_database_session()