from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import os
from database import db, create_document

app = FastAPI(title="Portfolio API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactMessageModel(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    subject: Optional[str] = Field(None, max_length=150)
    message: str = Field(..., min_length=5, max_length=5000)


@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/test")
def test():
    database_url = os.getenv("DATABASE_URL", "not set")
    database_name = os.getenv("DATABASE_NAME", "not set")
    status = "connected" if db is not None else "not connected"
    collections = []
    try:
        if db is not None:
            collections = db.list_collection_names()
    except Exception:
        pass

    return {
        "backend": "FastAPI",
        "database": "MongoDB",
        "database_url": database_url,
        "database_name": database_name,
        "connection_status": status,
        "collections": collections,
    }


@app.post("/contact")
def submit_contact(msg: ContactMessageModel):
    try:
        doc_id = create_document("contactmessage", msg)
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
