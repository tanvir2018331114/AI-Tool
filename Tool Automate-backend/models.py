
from sqlalchemy import Column, Integer, String, Text, Float, JSON, ARRAY
from database import Base

class Tool(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text)
    input_params = Column(JSON)
    output_type = Column(String)
    code = Column(Text)
    embedding = Column(ARRAY(Float))
