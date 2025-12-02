from fastapi import APIRouter, Request, Response
import controller.user as ctrlr
from pwdlib import PasswordHash
from db_connection import DbConnection
from models.user import User, InputUser, PartialUser
from pydantic import EmailStr
from typing import Dict

user_router = APIRouter(prefix="/user")

@user_router.post("/signup")
async def register(request: Request, payload: Dict[EmailStr]):
    db: DbConnection = request.app.state.db
    user = ctrlr.get_user_by_email()
    if user is not None:
        ...
        # TODO : Retourner une reponse http avec les bons code erreurs etc.
    return await ctrlr.register(db, payload)
