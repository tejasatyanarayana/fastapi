from fastapi import FastAPI,Request,HTTPException,Depends
from database import get_db,Base,engine
from sqlalchemy.orm import Session
from models import Clothes


Base.metadata.create_all(bind=engine)




app = FastAPI()


@app.get("/stock/total_stock")
def total_stock(db :Session = Depends(get_db)):
    return db.query(Clothes).all()

@app.post("/stock/add_stock")
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
        raise HTTPException(status_code=400, detail="clorth_id must be integers , price must be a number")

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



    



# @app.put("/stock/update_stock/{cloth_id}")
# async def update_stock(request:Request):
#     try:
#         data = await request.json()
#         cloth_id = int(data["cloth_id"])
#         fabric = data["fabric"]
#         price = int(data["price"])
#         quantity = int(data["quantity"])
#     except Exception :
#         raise HTTPException(status_code=404, detail="Cloth not found")
#     if cloth_id not in stock:
#         raise HTTPException(status_code=404 , detail="cloth not found")
#     stock[cloth_id]={
#         "fabric" : fabric,
#         "price" : price,
#         "quantity" : quantity
#     }
#     return {
#         "message" : "cloth modified successfully"
#     }

# @app.delete("/stock/delete_stock/{cloth_id}")
# async def delete_cloth(cloth_id:int):
#     print(cloth_id)
#     if int(cloth_id) not in stock:
#         raise HTTPException(status_code=404, detail="cloth not found")
#     del stock[cloth_id]
#     return{
#         "message" : "cloth deleted successfully"
#     }