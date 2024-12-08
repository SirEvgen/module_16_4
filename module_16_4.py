from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List

from typing_extensions import Annotated

users = []
app = FastAPI()


class Users(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users")
async def get_users() -> List[Users]:
    return users


@app.post("/user/{username}/{age}")
async def post_user(username: Annotated[str, Path(min_length=4, max_length=20, discriminator="Enter username",
                                                  example="UrbanUser")],
                    age: Annotated[int, Path(ge=18, le=120, description='Enter age',
                                             example='24')]):
    if not users:
        id = 1
    else:
        id = users[-1].id + 1
    new_user = Users(id=id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, discriminator="Enter your id",
                                                   example="12")],
                      username: Annotated[str, Path(min_length=4, max_length=20, discriminator="Enter username",
                                                    example="UrbanUser")],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age',
                                               example='24')]):
    try:
        new_user = users[user_id - 1]
        new_user.username = username
        new_user.age = age
        return new_user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, discriminator="Enter your id",
                                                   example="12")]):
    for count, user in enumerate(users):
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")
