# Backend setup

This folder contains the FastAPI API, Groq integration, and MySQL analysis-history storage.

For full project setup, see the root [README](../README.md) and [setup guide](../SETUP.md). The backend-specific steps are summarized below.

## Requirements

- Python 3.10 or newer
- MySQL 8 or compatible
- A Groq API key for AI-powered endpoints

## Install and configure

From the project root in PowerShell:

```powershell
Set-Location .\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirement.txt
Copy-Item .env.example .env
```

Set your private Groq and MySQL credentials in `backend/.env`:

```dotenv
GROQ_API_KEY=your_private_groq_api_key
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=constructai
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_private_mysql_password
```

These are example values only. Do not commit `.env` or share its contents.

## Create the database

Run [`schema.sql`](./schema.sql) in MySQL Workbench, or from PowerShell in this directory:

```powershell
Get-Content .\schema.sql | mysql -u root -p
```

The application creates the `analysis_history` table when needed, but the database must already exist and the configured MySQL user must have permission to create and use the table. Successful AI analyses are saved to the table.

## Run the API

With the virtual environment active in this directory:

```powershell
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API is available at http://localhost:8000. Interactive API documentation is at http://localhost:8000/docs.

## Deployment

For Render environment-variable and hosted MySQL instructions, see [Deploy on Render](../SETUP.md#deploy-on-render). Keep `GROQ_API_KEY` and MySQL credentials in local environment settings or the hosting provider's secret settings, never in source control.
