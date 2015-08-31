from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from moderator import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    fname = Column(String(255))
    lname = Column(String(255))
    userid = Column(String(10))
    password = Column(String(255))
    isadmin = Column(Integer)
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
    complete = Column(Integer, default=0)


class Vote(Base):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True)
    topic = Column(Integer, ForeignKey('topic.id'))
    voteup = Column(Integer, default=0)
    votedown = Column(Integer, default=0)
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
