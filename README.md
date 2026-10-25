# ConstructAI

ConstructAI is a multimodal construction intelligence demo with a React/Vite frontend and a FastAPI backend. It includes site safety monitoring, crack detection, property valuation, project planning, a construction knowledge assistant and chatbot, a daily site assistant, a weather advisor, and MySQL-backed analysis history.

## Requirements

- Python 3.10 or later
- Node.js 20.19+ or 22.12+
- MySQL 8.0+
- A Groq API key for AI-powered analysis

## Run locally on Windows

Open two PowerShell terminals at the project root.

### 1. Configure MySQL

Create the database and history table by running [`backend/schema.sql`](backend/schema.sql) in MySQL Workbench, or from PowerShell if the MySQL client is on `PATH`:

```powershell
mysql -u root -p < backend\schema.sql
```

Copy the backend environment template and edit the local `.env` file with your own values:

```powershell
Copy-Item backend\.env.example backend\.env
notepad backend\.env
```

Set `GROQ_API_KEY`, `MYSQL_DATABASE`, `MYSQL_USER`, and `MYSQL_PASSWORD`. The default database name in the template is `constructai`. Keep `.env` private; it is excluded from Git.

### 2. Start the backend

In the first PowerShell terminal:

```powershell
Set-Location backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirement.txt
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API runs at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

### 3. Start the frontend

In the second PowerShell terminal:

```powershell
Set-Location frontend
npm ci
npm run dev
```

Open the local URL printed by Vite, usually `http://localhost:5173`. During development the frontend sends API requests to `http://localhost:8000`. Set `VITE_API_BASE_URL` if the API uses a different address.

## Analysis history

Successful AI analyses are saved to MySQL. The **Analysis History** page shows the latest 50 entries. The API endpoint `GET /api/history` accepts an optional `limit` between 1 and 100.

The API database connection uses these settings from `backend/.env`:

| Variable | Purpose | Default |
| --- | --- | --- |
| `MYSQL_HOST` | MySQL server hostname | `127.0.0.1` |
| `MYSQL_PORT` | MySQL server port | `3306` |
| `MYSQL_DATABASE` | Database name | Required |
| `MYSQL_USER` | MySQL account | Required |
| `MYSQL_PASSWORD` | MySQL password | Empty |

## Build and lint the frontend

```powershell
Set-Location frontend
npm run build
npm run lint
```

## Deploy a public demo on Render

The root [`render.yaml`](render.yaml) defines a Render Blueprint with a static frontend and a FastAPI service.

1. Push this repository to GitHub and sign in to Render.
2. In Render, create a new Blueprint and select this GitHub repository.
3. Add the prompted environment variables securely in Render. Provide `GROQ_API_KEY` and the credentials for a MySQL database reachable from Render. Do not use a MySQL server bound only to your local computer.
4. Deploy the Blueprint and wait for both services to become healthy. Use the static site URL shown in Render as the public demo link.

The frontend's `VITE_API_BASE_URL` is connected to the deployed API by the Blueprint. Keep secrets in Render environment settings, not in this repository.

## Security notes

- Never commit `.env` files, API keys, database passwords, or other credentials.
- `.gitignore` excludes local environment files, Python caches, `node_modules`, and frontend build output.
- AI requests require a valid Groq API key. Analysis history requires a reachable MySQL database.
