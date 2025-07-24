from sqlalchemy import Column, Integer, String
from lib.db import Base

class Autocomplete(Base):
    __tablename__ = "autocomplete"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)