from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator
import json
import uvicorn

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

# Initialize FastAPI app
app = FastAPI()

# API key and Gemini client setup
gemini_api_key = "your_api_key"
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Define all agents
web_development_expert: Agent = Agent(
    name="Web Development Agent",
    instructions="You are a Web Development Assistant. You only respond to queries related to web development.",
    model=model,
    handoff_description="Web development expert"
)

mobile_development_expert: Agent = Agent(
    name="Mobile Development Agent",
    instructions="You are a mobile Development Assistant. You only respond to queries related to mobile development.",
    model=model,
    handoff_description="Mobile development expert"
)

Devops_expert: Agent = Agent(
    name="DevOps Agent",
    instructions="You are a DevOps Assistant. You only respond to queries related to DevOps.",
    model=model,
    handoff_description="DevOps expert"
)

Openai_agent: Agent = Agent(
    name="OpenAI Agent",
    instructions="You are an OpenAI Assistant. You only respond to queries related to OpenAI.",
    model=model,
    handoff_description="OpenAI expert"
)

Agentic_AI_expert: Agent = Agent(
    name="AI Development Agent",
    instructions="""You are an AI Development Assistant. You only respond to queries related to AI development. Use tools like DevOps and OpenAI as needed.""",
    tools=[
        Devops_expert.as_tool(tool_name="DevOps", tool_description="Handle infrastructure-related AI deployment queries."),
        Openai_agent.as_tool(tool_name="OpenAI Expert", tool_description="Answer OpenAI-related AI system questions."),
    ],
    model=model,
    handoff_description="AI development expert"
)

triage_agent: Agent = Agent(
    name="Triage Agent",
    instructions="Redirect all questions related to web development, mobile development, or Agentic AI to their respective agents. For unrelated queries, inform the user your role is limited.",
    model=model,
    handoffs=[web_development_expert, mobile_development_expert, Agentic_AI_expert]
)

# Request model
class QueryRequest(BaseModel):
    query: str

# -------------------------
# 📌 NON-STREAMING ENDPOINT
# -------------------------
@app.post("/ask")
async def ask_agent(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        result = await Runner.run(triage_agent, request.query)
        return {"response": result.final_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------------------------
# 📌 STREAMING ENDPOINT (text/event-stream)
# --------------------------------------
async def stream_response(message: str) -> AsyncGenerator[str, None]:
    result = Runner.run_streamed(triage_agent, input=message, run_config=config)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            chunk = json.dumps({"chunk": event.data.delta})
            yield f"data: {chunk}\n\n"

@app.post("/ask/stream")
async def ask_agent_stream(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    return StreamingResponse(
        stream_response(request.query),
        media_type="text/event-stream"
    )


# Optional: To run this file directly
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


