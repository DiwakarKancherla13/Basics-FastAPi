from pydantic import BaseModel,Field
class Product(BaseModel):
    Id:int 
    Brand:str 
    Model:str 
    Category:str 
    Sub_Category:str
    Price:int 

