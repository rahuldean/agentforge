# rahulmx_agent

A streaming AI assistant for [rahulmx.com](https://rahulmx.com). It answers visitor questions about my work, projects, and background using Google's Agent Development Kit and Gemini 2.5 Flash.

## What it does

The agent runs as a FastAPI server with a single `/chat` endpoint. Responses stream back as server-sent events so the frontend can start rendering immediately without waiting for the full reply.

## Stack

- [Google ADK](https://google.github.io/adk-docs/) for the agent runtime
- Gemini 2.5 Flash as the underlying model
- FastAPI + uvicorn for the HTTP layer
- Docker for deployment

## Setup

Copy the example env file and fill in your API key:

```bash
cp .env.example .env
```

Install dependencies:

```bash
make install
```

## Running locally

```bash
make dev
```

The server starts at `http://localhost:8000` with hot reload enabled.

To run without reload:

```bash
make run
```

## Docker

Build the image:

```bash
make build
```

Run the container (reads from your `.env` file):

```bash
make up
```

Stream logs from a running container:

```bash
make logs
```

Stop it:

```bash
make down
```

## API

### POST /chat

Send a message and get a streaming response.

**Request body:**

```json
{
  "message": "What projects have you worked on?",
  "session_id": "user-123"
}
```

`session_id` is optional and defaults to `"default"`. Use a unique value per user or browser session to maintain conversation history.

**Response:**

Server-sent events stream. Each event is a chunk of the agent's reply:

```
data: Here are some of the projects...

data: [DONE]
```

### GET /health

Returns `{ "status": "ok" }`. Use this for uptime checks.

## Code quality

Linting and formatting use [ruff](https://docs.astral.sh/ruff/):

```bash
make lint
make format
```

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `GOOGLE_API_KEY` | Yes | API key for Google Gemini |
