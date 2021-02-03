import os
import re
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean, DateTime
from lib.domain.base import Base
from datetime import datetime
from lib.utils.reg_exp import RegExp


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
    slug = Column(String, nullable=False, index=True, unique=True)

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

        self.slug = None

        self._compute_values()

    def _compute_values(self) -> None:
        self.predicted_spread = (
            self.underdog_predicted_score - self.favorite_predicted_score
        )
        self.actual_spread = self.underdog_actual_score - self.favorite_actual_score

        self.covered = self.actual_spread < self.predicted_spread
        self.winner_predicted = self.favorite_actual_score > self.underdog_actual_score

        self.slug = (
            RegExp.replace_special_characters(
                self.date.strftime("%Y-%m-%d %H:%M:%S.%f %z"), "-"
            )
            + "-"
            + RegExp.replace_special_characters(self.favorite, "-")
            + "-"
            + RegExp.replace_special_characters(self.underdog, "-")
        )
        self.slug = self.slug.replace("--", "-")

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

    def merge(self, p1):
        self.date = p1.date if p1.date is not None else self.date
        self.favorite = p1.favorite if p1.favorite is not None else self.favorite
        self.underdog = p1.underdog if p1.underdog is not None else self.underdog
        self.favorite_predicted_score = (
            p1.favorite_predicted_score
            if p1.favorite_predicted_score is not None
            else self.favorite_predicted_score
        )
        self.underdog_predicted_score = (
            p1.underdog_predicted_score
            if p1.underdog_predicted_score is not None
            else self.underdog_predicted_score
        )
        self.favorite_actual_score = (
            p1.favorite_actual_score
            if p1.favorite_actual_score is not None
            else self.favorite_actual_score
        )
        self.underdog_actual_score = (
            p1.underdog_actual_score
            if p1.underdog_actual_score is not None
            else self.underdog_actual_score
        )
        self.percentage = (
            p1.percentage if p1.percentage is not None else self.percentage
        )
        self.location = p1.location if p1.location is not None else self.location

        self._compute_values()
