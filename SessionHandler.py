from sqlalchemy import create_engine, Column, Text, TIMESTAMP, BIGINT, func
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
Base = declarative_base()

class Request(Base):
    __tablename__ = 'requests'

    id = Column(BIGINT, primary_key=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    repo_url = Column(Text)
    prompt = Column(Text)
    output = Column(Text)

    def __repr__(self):
        return f"<Request(id={self.id}, created_at={self.created_at}, repo_url={self.repo_url}, prompt={self.prompt}, output={self.output})>"

class SessionHandler: # handling sessions for a Supabase DB
    def __init__(self):
        self.DATABASE_URI = os.getenv('DATABASE_URI')
        self.engine = create_engine(self.DATABASE_URI)
        self.session = sessionmaker(bind=self.engine)()

    def getAllRequests(self):
        return self.session.query(Request).all()

    def addRequest(self, repoUrl, prompt, output):
        request = Request(repo_url=repoUrl, prompt=prompt, output=output)
        self.session.add(request)
        self.session.commit()
    
    def disconnect(self):
        self.session.close()