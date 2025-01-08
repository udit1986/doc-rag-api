from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Document
from app.schemas.requests import QuestionRequest
import openai
from app.core.config import get_settings 

openai.api_key = get_settings().openai_api_key

async def ingest_document(document_data: dict, db: AsyncSession):
    new_document = Document(**document_data)
    new_document.embedding = await generate_embeddings(new_document.content)
    db.add(new_document)
    await db.commit()
    await db.refresh(new_document)
    return new_document

async def answer_question(question: QuestionRequest, db: AsyncSession):
    result = await db.execute(select(Document).where(Document.id.in_(question.document_ids)))
    rows = result.fetchall()
    embeddings = [row['embedding'] for row in rows]
    retriever = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")
    question_embedding = retriever(question.question)[0]
    # Use OpenAI's API to get a response based on the embeddings
    response = openai.Embedding.create(
        input=question_embedding,
        model="text-embedding-ada-002"
    )
    
    # Implement retrieval logic here
    answer = response['data'][0]['embedding']

    return {"answer": "Generated answer based on retrieved content"}


async def select_documents(criteria: dict, db: AsyncSession):
    # Implement logic to select documents based on criteria
    pass

# Embedding generation
async def generate_embeddings(content: str):
    # Use OpenAI or Hugging Face to generate embeddings
    response = openai.Embedding.create(input=content, model="text-embedding-ada-002")
    return response['data'][0]['embedding']