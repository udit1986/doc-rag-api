from fastapi import APIRouter, Depends, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Document

router = APIRouter()

@router.post("/ingest")
async def ingest_document(document_data: dict):
    return await document_service.ingest_document(document_data)

@router.post("/chat")
async def answer_question(question: str):
    return await document_service.answer_question(question)

@router.post("/select")
async def select_documents(criteria: dict):
    return await document_service.select_documents(criteria)