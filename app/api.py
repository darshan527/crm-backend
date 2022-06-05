from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from pydantic import BaseModel
import sqlite3
from app.db import check_login, check_user


con = sqlite3.connect("crm_sql.db")
cur = con.cursor()


class Login(BaseModel):
    email: str
    password: str
    secret_que: str
    secret_ans: str


class Post(BaseModel):
    title: str
    body: str
    author: str
    status: str
    pubdate: str


class User(Login):
    name: str
    role: str


app = FastAPI()

origins = ["http://localhost:3000", "localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}


@app.post("/login", tags=["login"], status_code=(status.HTTP_200_OK))
async def login(user_details: Login):
    # print(user_details)
    user_details = user_details.dict()
    if check_login(con, user_details):
        print("user exist")
        return user_details
    else:
        print("User not exist")
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not exist"
        )


@app.post("/signup", tags=["signup"], status_code=status.HTTP_201_CREATED)
async def signup(user_details: User):
    user_details = user_details.dict()
    usr = check_user(con, user_details["email"])
    if usr:
        # print("Not inserted")
        return HTTPException(
            status.HTTP_406_NOT_ACCEPTABLE, detail="User already registered"
        )
    else:
        cur.execute(
            """INSERT INTO Users VALUES(:name,:email,:password,:role,:secret_que,:secret_ans)""",
            user_details,
        )
        con.commit()
        # ls = cur.execute("""SELECT * FROM USERS;""").fetchall()
        # print(ls)
        # print("Data Inserted")
    return user_details
