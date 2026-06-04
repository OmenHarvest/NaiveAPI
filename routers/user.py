from fastapi import APIRouter, Depends, Response, HTTPException
from sqlmodel import Session
from database import get_session
from schemas.user_schema import UserResponse, UserCreateOrUpdate, UserExportResponse
from services.user_service import get_all_users as get_all_users_from_service
from services.user_service import create_user as create_user_from_service
from services.user_service import export_user as export_user_from_service
from services.user_service import edit_password_by_login as edit_password_by_login_from_service
from services.user_service import delete_user_by_login as delete_user_by_login_from_service




role = APIRouter(prefix="/users", tags=["user"])
#Role editor

@role.get("/", response_model=list[UserResponse])
def get_all_users(response:Response, session: Session = Depends(get_session)):
    all_users = get_all_users_from_service(sesson=session)
    if not all_users:
        return Response(status_code=204)
    else:
        response.status_code=200
        return all_users

@role.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreateOrUpdate, response: Response, session: Session = Depends(get_session)):
    response.status_code=200
    return create_user_from_service(session, user)

@role.patch("/")
def edit_user_password_by_login(user: UserCreateOrUpdate, response: Response, session: Session = Depends(get_session)):
    response.status_code=200
    return edit_password_by_login_from_service(data=user, session=session)

    

@role.delete("/{login}")
def delete_user_by_login(login:str, session:Session = Depends(get_session)):
    deleted = delete_user_by_login_from_service(session=session, login=login)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return "success"

@role.get("/{login}/export", response_model=UserExportResponse)
def get_connection_data_by_login(login: str, session: Session = Depends(get_session)):
    result = export_user_from_service(login=login, session=session)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result
    