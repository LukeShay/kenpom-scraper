from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, Session, Query


class BaseDAO:
    def __init__(self, engine: Engine):
        self._engine = engine
        self._session = None

    def save(self, obj):
        self.session.add(obj)
        return obj

    def commit(self) -> None:
        self.session.commit()

    def query(self, clazz) -> Query:
        return self.session.query(clazz)

    @property
    def session(self) -> Session:
        if self._session is None:
            DBSession = sessionmaker(bind=self._engine)
            self._session = DBSession()

        return self._session
