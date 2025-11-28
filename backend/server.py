from fastapi import FastAPI

app = FastAPI(title="My Universe Doc")

@app.get("/")
async def root():
    return {"message": "Hello World"}

