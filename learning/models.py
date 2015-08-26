from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from learning import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    fname = Column(String(255))
    lname = Column(String(255))
    userid = Column(String(10))
    password = Column(String(255))
    topics = relationship('Topic')
    votes = relationship('Vote')
    posts = relationship('Post')


class Topic(Base):
    __tablename__ = 'topic'
    id = Column(Integer, primary_key=True)
    topic = Column(String(255), unique=True)
    description = Column(String)
    createdby = Column(Integer, ForeignKey('user.id'))
    votes = relationship('Vote')
    posts = relationship('Post')
    complete = Column(Integer)


class Vote(Base):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True)
    topic = Column(Integer, ForeignKey('topic.id'))
    voteup = Column(Integer)
    votedown = Column(Integer)
    voter = Column(Integer, ForeignKey('user.id'))


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    slug = Column(String(255), unique=True)
    content = Column(String)
    timestamp = Column(DateTime)
    author = Column(Integer, ForeignKey('user.id'))
    parent = Column(Integer)
    topic = Column(Integer, ForeignKey('topic.id'))
