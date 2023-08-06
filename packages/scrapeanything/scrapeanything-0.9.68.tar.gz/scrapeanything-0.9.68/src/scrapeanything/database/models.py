'''SQLAlchemy Data Models.'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Numeric, Integer, Text, String, Date, DateTime, Time, Boolean, Enum, Float
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.sql import func
import enum

from scrapeanything.utils.types import Types

Base = declarative_base()

class Model(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())

class Run(Model):

    __tablename__ = 'runs'
    __keys__ = 'started_at, finished_at'

    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    error_message = Column(String(255))