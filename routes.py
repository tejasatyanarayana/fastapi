from fastapi import HTTPException,Depends
from database import get_db
from sqlalchemy.orm import Session
from models import Clothes

from fastapi import APIRouter

router = APIRouter(prefix="/stock",
                   tags=["Clothes"])

@router.get("/total_stock")
def total_stock(db :Session = Depends(get_db)):
    return db.query(Clothes).all()

@router.post("/add_stock")
async def new_stock(data:dict,db :Session = Depends(get_db)):
    required = ["cloth_id","name","price","stock"]
    missing = []
    for f in required:
        if f not in data:
            missing.append(f)

            

    if missing:
        raise HTTPException(status_code=400, detail=f"{missing} are missing")


    try:
        cloth_id = int(data["cloth_id"])
        name = str(data['name'])
        price=float(data['price'])
        stock = int(data['stock'])
    except (ValueError,TypeError):
        raise HTTPException(status_code=400, detail="cloth_id must be integers , price must be a number")

    existing_cloth = db.query(Clothes).filter(Clothes.cloth_id == cloth_id).first()

    if existing_cloth:
        raise HTTPException(
            status_code = 409,
            detail = "CLOTH ID already exists"
        )

    cloth = Clothes(
        cloth_id = cloth_id,
        name = name,
        price = price,
        stock = stock
    )

    db.add(cloth)
    db.commit()
    db.refresh(cloth)

    return {
        "message": "Cloth added successfully",
        "cloth":cloth
    }



@router.put("/update_stock/{cloth_id}")
async def update_stock(data:dict,db : Session = Depends(get_db)):
    required = ["cloth_id","name","price","stock"]
    missing = []
    for f in required:
        if f not in data:
            missing.append(f)

    if missing:
        raise HTTPException(status_code=400, detail=f"{missing} are missing")

    try:
        cloth_id = int(data['cloth_id'])
        name = str(data['name'])
        price = float(data['price'])
        stock = int(data['stock'])
    except (ValueError,TypeError):
        raise HTTPException(status_code=400, detail = "cloth id must be integers, price must be a number")

    cloth = db.query(Clothes).filter(Clothes.cloth_id == cloth_id).first()

    if not cloth:
        raise HTTPException(
            status_code= 409,
            detail="Cloth id does not exist"
        )
    cloth.name = name
    cloth.price = price
    cloth.stock = stock
    
    
    db.commit()
    db.refresh(cloth)

    return{
        "message": "Cloth modified Successfully!!",
        "cloth" : cloth
    }

@router.delete("/delete_stock/{cloth_id}")
def delete_stock(cloth_id,db :Session = Depends(get_db)):
    cloth = db.query(Clothes).filter(Clothes.cloth_id == cloth_id).first()

    if not cloth:
        raise HTTPException(status_code=404, detail="cloth not found")
    db.delete(cloth)
    db.commit()
    return{
        "message" : "Cloth deleted Successfully" 
    }
