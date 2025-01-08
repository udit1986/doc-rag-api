from fastapi import APIRouter, Depends, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Document
from app.api import deps

router = APIRouter()

@router.post("/ingest")
async def ingest_document(document_data: dict, db: AsyncSession = Depends(deps.get_session)):
    return await document_service.ingest_document(document_data, db)

@router.post("/chat")
async def answer_question(question: str, db: AsyncSession = Depends(deps.get_session)):
    return await document_service.answer_question(question, db)

@router.post("/select")
async def select_documents(criteria: dict, db: AsyncSession = Depends(deps.get_session)):
    return await document_service.select_documents(criteria, db)