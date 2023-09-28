from pydantic import BaseModel

class User(BaseModel):
    id : int
    username : str
    password : str
    created_at : str
    updated_at : str

class Booking(BaseModel):
    id : int
    user_id : str
    start_time : str
    end_time : str