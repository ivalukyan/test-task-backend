from fastapi import FastAPI, HTTPException
from models import User, Booking
import psycopg2
from datetime import datetime
from passlib.hash import bcrypt
from const import MYDATABASE, USER_DB, PASSWORD_DB, LOCALHOSTING

def date_now():
    dt = datetime.now()
    return dt
def hashpassword(password):
    hashed_password = bcrypt.hash(password)
    return hashed_password

app = FastAPI(
    title="test-back-end"
)

conn = psycopg2.connect(
    host=LOCALHOSTING,
    database=MYDATABASE,
    user=USER_DB,
    password=PASSWORD_DB
)

@app.post("/users/")
async def create_users(user : User):
    with conn.cursor() as cur:
        password_user = hashpassword(user.password)
        cur.execute("INSERT INTO users(id, username, password, created_at, updated_at) VALUES(%s, %s, %s, %s, %s)", (user.id, user.username, password_user, date_now(), date_now()))
        conn.commit()
        return {"message": "User created successfully"}

@app.delete("/users/{user_id}")
async def delete_users(user_id : int):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM users WHERE id=%s", (user_id, ))
        conn.commit()
        cur.execute("SELECT * FROM booking WHERE user_id=%s", (user_id,))
        cur.execute(f"DELETE FROM booking WHERE {cur.fetchall()}")
        conn.commit()
        return {"message" : "User deleted successfully"}

@app.post("/booking/")
async def create_booking(booking : Booking, user : User):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO booking(id, user_id, start_time, end_time) VALUES(%s, %s, %s, %s)", (booking.id, user.id, date_now(), booking.end_time))
        conn.commit()
        return {"message": "Booking for user created successfully"}

@app.delete("/booking/{book_id}")
async def delete_booking(book_id : int):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM booking WHERE id=%s", (book_id,))
        conn.commit()
        return {"message" : "Booking deleted successfully"}

@app.get("/booking/{book_id}")
async def read_booking(book_id : int):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM booking WHERE id=%s", (book_id,))
        res = cur.fetchone()
        if res:
            return {"id": res[0], "user_id": res[1], "start_time" : res[2], "end_time" : res[3]}
        else:
            raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
async def update_user(user_id : int, user : User):
    with conn.cursor() as cur:
        password_user = hashpassword(user.password)
        cur.execute("UPDATE users SET username=%s, password=%s, update_at=%s WHERE id=%s", (user.username, password_user, date_now(), user_id))
        conn.commit()
        return {"message": "User updated successfully"}

@app.put("/booking/{book_id}")
async def update_booking(book_id : int, booking : Booking):
    with conn.cursor() as cur:
        cur.execute("UPDATE booking SET start_time=%s, end_time=%s WHERE id=%s", (date_now(), booking.end_time, book_id))
        conn.commit()
        return {"message": "Booking updated successfully"}

