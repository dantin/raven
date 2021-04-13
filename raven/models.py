# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Room(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    jabber_id = Column(String(255), nullable=False)

    def __repr__(self):
        return self.name


class Device(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    serial_no = Column(String(255), nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'))
    room = relationship('Room')


class Stream(Model):
    id = Column(Integer, primary_key=True)
    push_url = Column(String(255), nullable=False)
    broadcast_url = Column(String(255), nullable=False)
    device_id = Column(Integer, ForeignKey('device.id'))
    device = relationship('Device')
