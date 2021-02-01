import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from lib.domain.base import Base
from datetime import datetime


class FanMatch(Base):
    __tablename__ = "fan_match"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    favorite = Column(String, nullable=False)
    underdog = Column(String, nullable=False)
    favorite_predicted_score = Column(Integer, nullable=False)
    underdog_predicted_score = Column(Integer, nullable=False)
    favorite_actual_score = Column(Integer, nullable=False)
    underdog_actual_score = Column(Integer, nullable=False)
    percentage = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    predicted_spread = Column(Float, nullable=False)
    actual_spread = Column(Integer, nullable=False)
    covered = Column(Boolean, nullable=False)
    winner_predicted = Column(Boolean, nullable=False)

    def __init__(
        self,
        date=datetime.now(),
        favorite="",
        underdog="",
        favorite_predicted_score=-1,
        underdog_predicted_score=-1,
        favorite_actual_score=-1,
        underdog_actual_score=-1,
        percentage=-1,
        location="",
    ):
        self.date = date
        self.favorite = favorite
        self.underdog = underdog
        self.favorite_predicted_score = favorite_predicted_score
        self.underdog_predicted_score = underdog_predicted_score
        self.favorite_actual_score = favorite_actual_score
        self.underdog_actual_score = underdog_actual_score
        self.percentage = percentage
        self.location = location

        self.predicted_spread = None
        self.actual_spread = None

        self.covered = None
        self.winner_predicted = None

        self._calculate_numbers()

    def _calculate_numbers(self) -> None:
        self.predicted_spread = (
            self.underdog_predicted_score - self.favorite_predicted_score
        )
        self.actual_spread = self.underdog_actual_score - self.favorite_actual_score

        self.covered = self.actual_spread < self.predicted_spread
        self.winner_predicted = self.favorite_actual_score > self.underdog_actual_score

    def __str__(self):
        return f"{self.date},{self.favorite},{self.underdog},{self.location},{self.favorite_predicted_score},{self.underdog_predicted_score},{self.predicted_spread},{self.percentage},{self.favorite_actual_score},{self.underdog_actual_score},{self.actual_spread},{self.covered},{self.winner_predicted}"

    @staticmethod
    def column_headers():
        return "date,favorite,underdog,location,favorite_predicted_score,underdog_predicted_score,predicted_spread,percentage,favorite_actual_score,underdog_actual_score,actual_spread,covered,winner_predicted"

    @classmethod
    def fromKenPomPrediction(cls, prediction):
        return cls(
            prediction.date,
            prediction.favorite,
            prediction.underdog,
            prediction.favorite_predicted_score,
            prediction.underdog_predicted_score,
            prediction.favorite_actual_score,
            prediction.underdog_actual_score,
            prediction.percentage,
            prediction.location,
        )

    @classmethod
    def merge(cls, p1, p2):
        new = cls.fromKenPomPrediction(p1)

        new.date = p2.date if p2.date is not None else p1.date
        new.favorite = p2.favorite if p2.favorite is not None else p1.favorite
        new.underdog = p2.underdog if p2.underdog is not None else p1.underdog
        new.favorite_predicted_score = (
            p2.favorite_predicted_score
            if p2.favorite_predicted_score is not None
            else p1.favorite_predicted_score
        )
        new.underdog_predicted_score = (
            p2.underdog_predicted_score
            if p2.underdog_predicted_score is not None
            else p1.underdog_predicted_score
        )
        new.favorite_actual_score = (
            p2.favorite_actual_score
            if p2.favorite_actual_score is not None
            else p1.favorite_actual_score
        )
        new.underdog_actual_score = (
            p2.underdog_actual_score
            if p2.underdog_actual_score is not None
            else p1.underdog_actual_score
        )
        new.percentage = p2.percentage if p2.percentage is not None else p1.percentage
        new.location = p2.location if p2.location is not None else p1.location

        new._calculate_numbers()

        return new
