import uvicorn
import pymysql
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

conn = pymysql.connect(host='localhost',
                        user='root',
                        password='',
                        database='test')

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.get("/users")
def users():    
    cur = conn.cursor()
    sql = "select * from test.app1_teacher"
    cur.execute(sql)
    result = cur.fetchall()

    data_dict = {}
    datas_arr = []
    for i in result:
        data_dict['datas'] = {
            'id' : i[0],
            'name' : i[1],
            'age' : i[2],
            'gender' : i[3]
        }
        datas_arr.append(data_dict['datas'])
    return JSONResponse(datas_arr)


@app.get("/search_user/{user_id}")
def search_user(user_id):    
    cur = conn.cursor()
    sql = "select * from test.app1_teacher where id = %s"
    cur.execute(sql, user_id)
    result = cur.fetchone()
    if result:
        data_dict = {}
        data_dict['id'] = result[0]
        data_dict['name'] = result[1]
        data_dict['age'] = result[2]
        data_dict['gender'] = result[3]
        return JSONResponse(data_dict)
    else:
        return HTMLResponse(content="The user does not exist!", status_code=404)


@app.post('/create_user')
def create_user(name: str, age: int, gender: str):
    cur = conn.cursor()
    sql = """
            insert into test.app1_teacher (tname, tage, tgender)
            values(%s,%s,%s)
          """
    cur.execute(sql, (name, age, gender))
    conn.commit()
    return HTMLResponse(content="Create Success!", status_code=200)


@app.put('/update_user')
def update_user(user_id: int, name: str, age: int, gender: str):
    cur = conn.cursor()
    sql = "select * from test.app1_teacher where id = %s"
    cur.execute(sql, user_id)
    result = cur.fetchone()

    if result:
        sql = """
                update test.app1_teacher 
                set tname = %s, tage = %s, tgender = %s
                where id = %s
            """
        cur.execute(sql, (name, age, gender, user_id))
        conn.commit()
        return HTMLResponse(content="Update Success!", status_code=200)
    else:
        return HTMLResponse(content="The user does not exist!", status_code=404)


@app.delete('/delete_user')
def delete_user(user_id: int):    
    cur = conn.cursor()
    sql = "select * from test.app1_teacher where id = %s"
    cur.execute(sql, user_id)
    result = cur.fetchone()

    if result:
        sql = """
                delete from test.app1_teacher 
                where id = %s
            """
        cur.execute(sql, user_id)
        conn.commit()
        return HTMLResponse(content="Delete Success!", status_code=200)
    else:
        return HTMLResponse(content="The user does not exist!", status_code=404)


if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    
