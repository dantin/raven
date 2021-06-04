# -*- coding: utf-8 -*-
import enum

from flask_appbuilder import Model
from sqlalchemy import Column, Enum, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class VideoBoxTypes(str, enum.Enum):
    xgc_500 = 'XGC 500'


class VideoStreamTypes(str, enum.Enum):
    camera = 'Camera'
    device = 'Device'


class Room(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    jabber_id = Column(String(255), nullable=False)
    video_boxes = relationship('VideoBox')

    def __repr__(self):
        return self.name


class VideoBox(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    serial_no = Column(String(255), nullable=False)
    video_box_type = Column(Enum(VideoBoxTypes))
    room_id = Column(Integer, ForeignKey('room.id'))
    room = relationship('Room')
    video_streams = relationship('VideoStream')

    def __repr__(self):
        return self.serial_no


class VideoStream(Model):
    id = Column(Integer, primary_key=True)
    push_url = Column(String(255), nullable=False)
    broadcast_url = Column(String(255), nullable=False)
    stream_type = Column(Enum(VideoStreamTypes))
    video_box_id = Column(Integer, ForeignKey('video_box.id'))
    video_box = relationship('VideoBox')

    def __repr__(self):
        if self.video_box:
            return f'{self.video_box.serial_no}  {self.stream_type}'
        return f'Unknown {self.stream_type}'
