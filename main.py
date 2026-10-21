from fastapi import FastAPI,Request,HTTPException

app = FastAPI()

stock = {
    101 :{
        "fabric" : "Lenin",
        "price" : 1099,
        "quantity" : 20
    },
    102 : {
        "fabric" : "cotton",
        "price" : 850,
        "quantity" : 25
    }
}
@app.get("/stock/total_stock")
def total_stock():
    return stock

@app.post("/stock/add_stock")
async def new_stock(request:Request):
    data =await request.json()
    cloth_id = int(data["cloth_id"])
    if cloth_id not in stock:
        try:
            
            Fabric = data["fabric"]
            price = int(data["price"])
            Quantity = int(data["quantity"])
        except:
            raise  HTTPException(status_code = 404 , detail = "item already exists or is invalid format")
        
        stock[cloth_id] = {
            "fabric" : Fabric,
            "price" : price,
            "quantity" : Quantity   
        }

        
        return{
            "message" : "Successfully added"

        }

@app.put("/stock/update_stock/{cloth_id}")
async def update_stock(request:Request):
    try:
        data = await request.json()
        cloth_id = int(data["cloth_id"])
        fabric = data["fabric"]
        price = int(data["price"])
        quantity = int(data["quantity"])
    except Exception :
        raise HTTPException(status_code=404, detail="Cloth not found")
    if cloth_id not in stock:
        raise HTTPException(status_code=404 , detail="cloth not found")
    stock[cloth_id]={
        "fabric" : fabric,
        "price" : price,
        "quantity" : quantity
    }
    return {
        "message" : "cloth modified successfully"
    }

@app.delete("/stock/delete_stock/{cloth_id}")
async def delete_cloth(cloth_id:int):
    print(cloth_id)
    if int(cloth_id) not in stock:
        raise HTTPException(status_code=404, detail="cloth not found")
    del stock[cloth_id]
    return{
        "message" : "cloth deleted successfully"
    }