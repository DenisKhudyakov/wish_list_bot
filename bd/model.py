from sqlalchemy import Boolean, Column, Integer, String

from config.config import Base


class Gift(Base):
    __tablename__ = "gifts"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    reserved = Column(Boolean, default=False)
