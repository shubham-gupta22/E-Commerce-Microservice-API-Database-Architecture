from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import database
from database import Base

app = FastAPI()

# This is line 8 where it was crashing. It will find Base now!
Base.metadata.create_all(bind=database.engine)

@app.post("/products/")
def create_product(title: str, price: float, stock: int, db: Session = Depends(database.get_db)):
    new_product = models.Product(title=title, price=price, stock=stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product created successfully", "product_id": new_product.id}

@app.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product.id, "title": product.title, "price": product.price, "stock": product.stock}