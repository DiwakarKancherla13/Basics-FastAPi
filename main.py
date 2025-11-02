from fastapi import FastAPI,Depends,Security,HTTPException
from fastapi.security.api_key import APIKeyHeader
from model_pydantic import Product
from databaseconfig import engine,session
import model_sqlalchemy
from sqlalchemy.orm import Session
app = FastAPI()

model_sqlalchemy.Base.metadata.create_all(bind=engine)

STATIC_BEARER_TOKEN = "diwakarecommerce"

api_key_header =APIKeyHeader(name="Authorization",auto_error=True)

def verify_token(api_key: str = Security(api_key_header)):
    if not api_key.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = api_key.split(" ")[1]
    if token != STATIC_BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

Products=[
    Product(
            Id=1,
            Brand="Apple",
            Model="Iphone 17",
            Category="Electronics",
            Sub_Category="Smartphones",
            Price=83000
            )   
]

def init_db():
    db=session()

    count = db.query(model_sqlalchemy.Product).count
    if count ==0 :
        for product in Products:
            db.add(model_sqlalchemy.Product(**product.model_dump()))
    
        db.commit()
        db.close()
    
init_db()

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def greet():
    return "Hello Server Up"

@app.get("/Products",dependencies=[Depends(verify_token)])
def get_Products(db:Session =Depends(get_db)):
    db_products=db.query(model_sqlalchemy.Product).all()
    return db_products

@app.get("/Products/{id}")
def get_Products(id:int,db:Session =Depends(get_db)):
    db_product=db.query(model_sqlalchemy.Product).filter(model_sqlalchemy.Product.Id == id).first()
    if db_product:
        return db_product
    return {"message":f"No Product Found With This Id :{id}"}


@app.post("/Products")
def add_Products(product:Product,db:Session =Depends(get_db)):
    db_product=db.query(model_sqlalchemy.Product).filter(model_sqlalchemy.Product.Id == product.Id).first()
    if db_product:
        return {"message":f"Duplicate We Cannot Add Product With Id {product.Id}"}
    db.add(model_sqlalchemy.Product(**product.model_dump()))
    db.commit()
    return "Product Added Successfully"

@app.put("/Products")
def update_Products(id:int,product:Product,db:Session =Depends(get_db)):
    db_product=db.query(model_sqlalchemy.Product).filter(model_sqlalchemy.Product.Id == id).first()
    if db_product:
        db_product.Brand =product.Brand
        db_product.Model =product.Model
        db_product.Category =product.Category
        db_product.Sub_Category =product.Sub_Category
        db_product.Price =product.Price
        db.commit()
        return "Product Updated Successfully"

    else:
        return "No Product Found"
    
@app.delete("/Products")
def delete_Products(id:int,product:Product,db:Session =Depends(get_db)):
    db_product=db.query(model_sqlalchemy.Product).filter(model_sqlalchemy.Product.Id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted Successfully"

    else:
        return "No Product Found"
