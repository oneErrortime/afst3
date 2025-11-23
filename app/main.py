from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from .api import auth, books, readers, borrows, advanced

app = FastAPI(title="Library Management API", version="1.0.0")

# Add CORS middleware to handle frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins during development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(readers.router, prefix="/readers", tags=["readers"])
app.include_router(borrows.router, prefix="/borrows", tags=["borrows"])
app.include_router(advanced.router, prefix="/advanced", tags=["advanced"])

# Mount the templates directory to serve static files
app.mount("/static", StaticFiles(directory="templates"), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to Library Management API"}

@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    with open("templates/index.html", "r", encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content=content)