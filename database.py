from sqlalchemy.orm import sessionmaker
from model import engine

Session = sessionmaker(bind=engine)

# new way
def get_db():
    with Session() as db:
        yield db