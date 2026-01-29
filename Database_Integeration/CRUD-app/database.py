from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# define the database URL
DATABASE_URL = "sqlite:///test.db"

# create the engine
engine = create_engine(DATABASE_URL, echo=True)
# echo=True logs generated SQL to the console for debugging

# create a session Factory
# this factory will create new session objects for each request/operation
sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)