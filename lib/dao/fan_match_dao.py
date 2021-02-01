from lib.domain.fan_match_model import FanMatch
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional

from lib.dao.base_dao import BaseDAO


class FanMatchDAO(BaseDAO):
    def __init__(self, engine: Engine):
        BaseDAO.__init__(self, engine)

    def save(self, prediction: FanMatch) -> FanMatch:
        return BaseDAO.save(self, prediction)

    def save_if_new(self, prediction: FanMatch) -> Optional[FanMatch]:
        try:
            BaseDAO.query(FanMatch).filter_by(
                date=prediction.date,
                favorite=prediction.favorite,
                underdog=prediction.underdog,
                location=prediction.location,
            ).one()

            return None
        except Exception:
            print(Exception)

        return self.save(prediction)

    def save_or_update(
        self, prediction: FanMatch
    ) -> Optional[FanMatch]:
        try:
            from_db = (
                BaseDAO.query(FanMatch)
                .filter_by(
                    date=prediction.date,
                    favorite=prediction.favorite,
                    underdog=prediction.underdog,
                    location=prediction.location,
                )
                .one()
            )

            prediction = FanMatch.merge(from_db, prediction)
        except Exception:
            print(Exception)

        return self.save(prediction)
