from fastapi import FastAPI, Path, status, Body, HTTPException
from pydantic import BaseModel
from typing import Annotated, List

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})

# users = {'1': 'Имя: Example, возраст: 18'}
users = []
class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get("/")
async def get_main():
    return "Главная страница"

@app.get("/user/admin")
async def get_admin():
    return "Вы вошли, как администратор"
#
# @app.get("/user/{user_id}")
# async def get_user_id(
#         user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example=32)]):
#     return f"Вы вошли как пользователь № {user_id}"
#
# @app.get('/user/{username}/{age}')
# async def get_user(
#         username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
#         age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]):
#     return f"Информация о пользователе. Имя: {username}, Возраст: {age}"

@app.get('/users')
async def get_all_users() -> List[User]:
    return users

@app.post('/user/{username}/{age}')
async def crate_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    user_id = str(len(users) + 1)
    user = User(id = user_id, username = username, age = age)
    users.append(user)
    return user

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        user_id: Annotated[int, Path(ge=1, le=100, description='Enter user id', example='1')],
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete( '/user/{user_id}')
async def delete_users(
        user_id: Annotated[int, Path(ge=1, le=100, description='Enter user id', example='1')]) -> User:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")