from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents.run_config import RunConfig, StreamingMode

from dotenv import load_dotenv
from google.genai import types

from agent import root_agent

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://rahulmx.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

session_service = InMemorySessionService()

APP_NAME = "rahulmx_agent_api"

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

async def get_or_create(app_name, user_id, session_id):
    # 1. Try to get the existing session
    session = await session_service.get_session(
        app_name=app_name, 
        user_id=user_id, 
        session_id=session_id
    )
    
    # 2. If it doesn't exist, create it
    if session is None:
        session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
    return session

@app.post("/chat")
async def chat(req: ChatRequest):
    session = await get_or_create(
        app_name= APP_NAME,
        user_id= req.session_id,
        session_id=req.session_id
    )

    async def stream_response():
        content = types.Content(
            role="user",
            parts=[types.Part(text=req.message)]
        )

        async for event in runner.run_async(
            user_id=req.session_id,
            session_id=req.session_id,
            new_message=content,
            run_config=RunConfig(streaming_mode=StreamingMode.SSE),
        ):
            if event.content and event.content.parts:
                  for part in event.content.parts:
                      if part.text:
                          yield f"data: {part.text}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

@app.get('/health')
async def health():
    return { 'status': 'ok'}