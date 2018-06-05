# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Collect(Base):
    __tablename__ = 'collect'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'), index=True)
    img_id = Column(ForeignKey('image.id'), index=True)

    img = relationship('Image', primaryjoin='Collect.img_id == Image.id', backref='collects')
    user = relationship('User', primaryjoin='Collect.user_id == User.id', backref='collects')


class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    url = Column(String(200))


class Music(Base):
    __tablename__ = 'music'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    singer = Column(String(50))
    brand = Column(String(20))
    mp3_url = Column(String(100))
    user_id = Column(ForeignKey('user.id'), index=True)

    user = relationship('User', primaryjoin='Music.user_id == User.id', backref='musics')


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    phone = Column(String(12))

    @property
    def json(self):
        return {"id":self.id,
                "name":self.name,
                "phone":self.phone}