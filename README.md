# ConstructAI — Multimodal Construction Intelligence

ConstructAI is a web application for AI-assisted construction planning, site safety, structural crack guidance, property valuation, and day-to-day construction questions. It combines a React/Vite frontend with a FastAPI backend and can save successful AI analyses to MySQL.

## Features

- Site safety monitor with optional image and document uploads
- Crack detection guidance with an optional image
- Real-estate valuation
- Construction project planning and material estimates
- Construction knowledge assistant
- Construction chatbot
- Daily site assistant
- Weather-aware activity advisor
- MySQL-backed analysis history

AI features use the Groq API. Their results are informational and should not replace review by qualified construction, structural, safety, or property professionals.

## Technology

- Frontend: React, Vite, React Router
- Backend: Python, FastAPI, Uvicorn
- AI: Groq API
- Persistence: MySQL

## Getting started

See [SETUP.md](./SETUP.md) for prerequisites, local installation, environment configuration, database setup, and deployment instructions.

Once configured, run the frontend and backend in separate terminals:

```powershell
# Terminal 1
Set-Location .\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

```powershell
# Terminal 2
Set-Location .\frontend
npm run dev
```

Open the local URL printed by Vite (normally http://localhost:5173). The API root is http://localhost:8000, and interactive API documentation is at http://localhost:8000/docs.

## Project layout

```text
backend/       FastAPI application, MySQL integration, and SQL schema
frontend/      React/Vite web application
render.yaml    Render Blueprint for the API and static frontend
SETUP.md       Detailed local and hosted setup instructions
```

## API routes

The backend exposes `GET /`, `GET /api/history`, and feature endpoints under `/api/`, including `/api/safety-monitor`, `/api/crack-detection`, `/api/real-estate-valuation`, `/api/project-planner`, `/api/knowledge-assistant`, `/api/chatbot`, `/api/site-assistant`, and `/api/weather-advisor`.

## Deployment

The Render deployment blueprint is in [`render.yaml`](./render.yaml). A public demo is **not deployed yet**. Deployment requires connecting the GitHub repository to Render and configuring a Groq API key and a MySQL database reachable by the hosted backend. See [SETUP.md](./SETUP.md#deploy-on-render).

## Security

- Never commit `.env` files, API keys, database passwords, or other credentials.
- Keep secrets in local environment files or the hosting provider's secret settings.
- Keep the MySQL database private and grant the application only the access it needs.
- The Git ignore rules exclude local environment files, dependencies, caches, and build output.