from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration Variables
database_name = os.getenv("DATABASE_NAME")
database_user = os.getenv("DATABASE_USER")
database_password = os.getenv("DATABASE_PASSWORD")
database_host = os.getenv("DATABASE_HOST", "localhost")
database_port = os.getenv("DATABASE_PORT", "5432")

# Create Database Connection URL
database_connection_url = f"postgresql+psycopg2://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"

# Initialize Database Engine
database_engine = create_engine(database_connection_url)

# Create a SessionMaker instance
DatabaseSession = sessionmaker(bind=database_engine)

# Initialize a Session
database_session = DatabaseSession()