from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
Base =declarative_base()
class Product(Base):

    __tablename__ ="copy_product"

    Id =Column(Integer,primary_key=True,index=True)
    Brand =Column(String)
    Model =Column(String)
    Category =Column(String)
    Sub_Category =Column(String)
    Price=Column(Integer)

