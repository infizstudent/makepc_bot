from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from config import  DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

Base = declarative_base()
#DELETE FROM computers;

class Computer(Base):
    __tablename__ = 'computers'
    id = Column(Integer, primary_key=True)
    image_url = Column(String)
    description = Column(String)
    message_id = Column(Integer)  # <---- add this


engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
