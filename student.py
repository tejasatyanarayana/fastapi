from fastapi import FastAPI,Request,HTTPException

app = FastAPI()

students = [
    {   "student_id" : 1,
        "name" : "Ankamma Rao",
        "marks" : 99,
        "status" : "pass"
    },

    {
            "student_id" : 2,
            "name" : "teja",
            "marks" : 98,
            "status" : "pass"
    },

    {
            "student_id" : 3,
            "name" : "Priya",
            "marks" : 25,
            "status" : "Fail"
    }
]

@app.get("/student/display_all")
def display_all():
    return {"students" : students}


@app.post("/student/add_student")
async def add_student(request:Request):
    data = await request.json()
    student_id = int(data["student_id"])
    if student_id not in students:
        try:
            name = data["name"]
            marks = int(data["marks"])
            status = data["status"]
        except:
            raise HTTPException(status_code=404, detail="Invalid input")
        new_student = {
            "student_id" : student_id,
            "name" : name,
            "marks" : marks,
            "status" : status
        }
        students.append(new_student)

    return {
        "message" : "Student record added successfully"
    }



@app.put("/student/update_student")
async def update_student(request:Request):
    data = await request.json()
    student_id = data["student_id"]

    for student in students:
        id = student["student_id"]
        
        if student_id == id:
                student["name"] = data["name"]
                student["marks"] = int(data["marks"])
                student["status"] = data["status"]
                break
    print(students)

        
    return {
        "message" : "Student record updated successfully"
    }



@app.delete("/student/delete_student")
async def delete_student(request:Request):
    data = await request.json()
    student_id = data["student_id"]
    for student in students:
        id = student["student_id"]

        if student_id == id:
            students.remove(student)
            break
    return {
        "message" : "Student record deleted successfully"
    }

    
        
        
