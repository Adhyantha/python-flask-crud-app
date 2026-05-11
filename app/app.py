from flask import Flask, request, jsonify
import mysql.connector
import time

app=Flask(__name__)


def connect():
        for i in range(10):
            try:
                connection=mysql.connector.connect(
                host="mysql-service",
                user="appuser",
                password="apppass",
                database="studentdb")

                print("Database Connected Successfully")
                return connection
            except Exception as ex:
                print("Retrying to connect DB : ",ex)
                time.sleep(5)
        raise Exception("Database not ready after retries")

db=connect()
                

cursor=db.cursor()

cursor.execute("""
create table if not exists students(id int auto_increment primary key, name varchar(101),
                age int)
""")

cursor.execute("select count(*) from students")
count=cursor.fetchone()[0]

if count==0:
    sample_query="insert into students(name,age) values(%s,%s)"
    sample_data=("Pandiyan",30)
    cursor.execute(sample_query,sample_data)
    db.commit()


@app.route("/")
def home():
    return "Student API is Running, <br/> <h1>Welcome to Kubernetes Demo with Helm Charts</h1>"


@app.route("/students",methods=["POST"])
def create_student():
    data=request.json
    
    name=data["name"]
    age=data["age"]

    query= "insert into students(name,age) values(%s,%s)"
    cursor.execute(query,(name,age))
    db.commit()

    return jsonify({
        "message":"Student Data inserted successfully"
    })

@app.route("/students",methods=["GET"])
def get_students():
    cursor.execute("select * from students")
    rows=cursor.fetchall()
    students=[]
    for row in rows:
        students.append({
            "id":row[0],
            "name":row[1],
            "age":row[2]
        })
    
    return jsonify(students)

@app.route("/students/<int:id>",methods=["PUT"])
def update_student(id):
    data=request.json
    query="update students set name=%s,age=%s where id=%s"

    cursor.execute(query,(data["name"],data["age"],id))
    db.commit()

    return jsonify({
        "message":"Student Data updated successfully"
    }) 

@app.route("/students/<int:id>",methods=["DELETE"])
def delete_student(id):
    query="delete from students where id=%s"

    cursor.execute(query,(id,))
    db.commit()

    return jsonify({
        "message":"Student Data deleted successfully"
    })

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)