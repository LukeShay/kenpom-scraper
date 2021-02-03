import os
import re
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from lib.domain.base import Base
from datetime import datetime
from lib.utils.reg_exp import RegExp


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True, unique=True)
    location = Column(String, nullable=False, index=True)

    def __init__(
        self,
        name="",
        location="",
    ):
        self.name = name
        self.location = location
