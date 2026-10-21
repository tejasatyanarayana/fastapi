# cloth_id = column Integer 
# name = column String 
# price = column Float
# stock = column Integer 


from sqlalchemy import Column,Integer,String,Float
from database import Base

class Clothes(Base):
    __tablename__ = "clothes"

    cloth_id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    price = Column(Float,nullable=False)
    stock = Column(Integer,nullable=False)



