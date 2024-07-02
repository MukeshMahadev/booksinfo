from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routes import book_routes
from routes import user_routes
from routes import review_routes

app = FastAPI()

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


@app.get("/api/healthcheck", tags=["Healthcheck"])
async def generate_music():
    return "Hi, Server is up and running"

app.include_router(user_routes.router, prefix='/api')
app.include_router(book_routes.router, prefix='/api')
app.include_router(review_routes.router, prefix='/api')


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=7777)
