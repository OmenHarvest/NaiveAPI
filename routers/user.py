from fastapi import APIRouter

role = APIRouter(prefix="/users", tags=["user"])
#Role editor

@role.get("/")
def get_all_users():
    pass

@role.post("/")
def create_user():
    pass

@role.patch("/{login}")
def edit_user_password_by_login(login:str):
    pass

@role.delete("/{login}")
def delete_user_by_login(login:str):
    pass

@role.get("/{login}/export")
def get_connection_data_by_login(login:str):
    pass