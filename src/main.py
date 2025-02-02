from fastapi import FastAPI
from route import search, base


app = FastAPI()
app.include_router(search.search_router, prefix="/matcher")
app.include_router(base.base_route)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)