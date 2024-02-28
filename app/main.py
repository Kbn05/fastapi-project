from fastapi import FastAPI
from .routers import posts, users, auth, location
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# my_posts = [{"title": "Hello World", "content": "This is my first post", "id": 1},
#             {"title": "Second Post", "content": "This is my second post", "id": 2},
#             {"title": "Third Post", "content": "This is my third post", "id": 3},
#             {"title": "Fourth Post", "content": "This is my fourth post", "id": 4}]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(location.router)


# Create a route to handle GET requests sent to the / path


@app.get("/")
async def root():
    return {"message": "Hello World"}
