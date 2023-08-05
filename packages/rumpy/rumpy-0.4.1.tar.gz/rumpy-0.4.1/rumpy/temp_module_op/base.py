import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from rumpy.modules.base import Base

logger = logging.getLogger(__name__)


class BaseDB:
    def __init__(self, db_name, echo, reset):
        # 创建数据库
        engine = create_engine(f"sqlite:///{db_name}.db", echo=echo, connect_args={"check_same_thread": False})
        if reset:
            Base.metadata.drop_all(engine)
        # 创建表
        Base.metadata.create_all(engine)
        # 创建会话
        self.Session = sessionmaker(bind=engine, autoflush=False)
        self.session = self.Session()
        logger.debug(f"init db, name: {db_name}, echo: {echo}, reset: {reset}")

    def __commit(self):
        """Commits the current db.session, does rollback on failure."""
        from sqlalchemy.exc import IntegrityError

        logger.debug("db commit")

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def add(self, obj):
        """Adds this model to the db (through db.session)"""
        self.session.add(obj)
        self.__commit()
        return self

    def commit(self):
        self.__commit()
        return self

    def delete(self, obj):
        """Deletes this model from the db (through db.session)"""
        self.session.delete(self)
        self.__commit()
