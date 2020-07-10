from fastapi import APIRouter

from . import bot

api_v1_router = APIRouter()
api_v1_router.include_router(bot.router, prefix='/bot')
