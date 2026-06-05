from sqlmodel import Session, select, delete
from models.user_model import User
from schemas.user_schema import UserCreateOrUpdate, UserExportResponse

from encrypt_manager import encrypt, decrypt

from events_bus import emit

def get_all_users(sesson:Session) -> list[User]:
    return sesson.exec(select(User)).all()
    
def create_user(session:Session, data:UserCreateOrUpdate):
    user = User(login=data.login, password=encrypt(data.password))

    session.add(user)
    session.commit()
    session.refresh(user)
    
    emit("user.changed", session=session)
    return user

def export_user(login: str, session: Session):
    user = session.exec(select(User).where(User.login == login)).first()

    if not user:
        return None

    emit("user.changed", session=session)
    return UserExportResponse(
        login=user.login,
        password=decrypt(user.password)
    )

def edit_password_by_login(session:Session, data:UserCreateOrUpdate):
    user = session.exec(select(User).where(User.login == data.login)).first()

    if not user:
        return None
    
    user.password = data.password

    session.add(user)
    session.commit()

    session.refresh(user)

    emit("user.changed", session=session)
    return user

def delete_user_by_login(session: Session, login: str) -> bool:
    user = session.exec(select(User).where(User.login == login)).first()
    if not user:
        return False
    session.delete(user)
    session.commit()
    emit("user.changed", session=session)
    return True