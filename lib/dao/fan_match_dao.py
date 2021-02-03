import traceback
from typing import Optional

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker

from lib.dao.base_dao import BaseDAO
from lib.domain.fan_match_model import FanMatch


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
        except:
            traceback.print_exc()

        return self.save(prediction)

    def save_or_update(self, prediction: FanMatch) -> Optional[FanMatch]:
        try:
            from_db = (
                BaseDAO.query(self, FanMatch).filter_by(slug=prediction.slug).first()
            )

            if from_db is not None:
                FanMatch.merge(from_db, prediction)
                return from_db
        except:
            traceback.print_exc()

        return self.save(prediction)
