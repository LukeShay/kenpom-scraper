import traceback
from typing import Optional

from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker

from lib.dao.base_dao import BaseDAO
from lib.domain.team_model import Team


class TeamDAO(BaseDAO):
    def __init__(self, engine: Engine):
        BaseDAO.__init__(self, engine)

    def save(self, name: Team) -> Team:
        return BaseDAO.save(self, name)

    def save_if_new(self, name: Team) -> Optional[Team]:
        try:
            BaseDAO.query(Team).filter_by(name=name.name).one()

            return None
        except:
            traceback.print_exc()

        return self.save(name)
