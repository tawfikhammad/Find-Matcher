from fastapi import APIRouter

base_route = APIRouter()

@base_route.get("/welcome")
async def welcome():
    return {"message": "Welcome to the Vector Search API!"}