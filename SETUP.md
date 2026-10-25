# Setup instructions

This guide covers local development and the optional Render deployment. Keep API keys and database credentials private; never paste them into source files, screenshots, issues, or chat.

## Requirements

- Python 3.10 or newer
- Node.js 20.19+ (or a compatible current Node.js LTS release) and npm
- MySQL 8 or a compatible MySQL server
- A Groq API key for AI-powered endpoints
- Git (optional for local setup; required to deploy from GitHub)

## 1. Configure the backend

Open PowerShell in the project folder:

```powershell
Set-Location .\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirement.txt
Copy-Item .env.example .env
```

Edit `backend/.env` locally and set the MySQL connection values. Add your Groq key:

```dotenv
GROQ_API_KEY=your_private_groq_api_key
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=constructai
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_private_mysql_password
```

Use your own values; the text above is only a placeholder. The `.env` file is ignored by Git.

### Create the MySQL database

Start MySQL, then create the database and history table using MySQL Workbench by opening and running [`backend/schema.sql`](./backend/schema.sql). Alternatively, from PowerShell in the `backend` directory, run:

```powershell
Get-Content .\schema.sql | mysql -u root -p
```

Use a dedicated MySQL user for the application when possible. Grant it access to the `constructai` database and use the same username and password in `.env`.

Successful AI analyses are saved to `analysis_history`. The history API returns up to 100 records (`GET /api/history?limit=50`). The backend also creates the table if it does not already exist, but the database itself must exist and the configured user must have the required permissions.

## 2. Start the backend

With the virtual environment active in `backend`:

```powershell
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Check the API at:

- Health response: http://localhost:8000/
- Interactive API documentation: http://localhost:8000/docs

AI requests require a working Groq key. Analysis history also requires a reachable, configured MySQL database.

## 3. Install and start the frontend

Open a second PowerShell terminal in the project folder:

```powershell
Set-Location .\frontend
npm ci
npm run dev
```

Open the local URL Vite prints (normally http://localhost:5173). During local development, the frontend uses `http://localhost:8000` for the API by default.

To use a different backend URL locally, create `frontend/.env.local`:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Restart Vite after editing environment variables. For a production build, `VITE_API_BASE_URL` should be the HTTPS base URL of the deployed API; do not include `/api` at the end.

## 4. Verify the frontend

Run these commands in `frontend`:

```powershell
npm run build
npm run lint
```

The build command verifies the production bundle. The project currently has existing lint errors for unused `motion` imports in some feature components; these are separate from whether the app builds.

## Deploy on Render

[`render.yaml`](./render.yaml) defines the FastAPI service and static frontend. A public demo link is available only after the services are successfully created and deployed.

1. Push the project to a GitHub repository and sign in to Render.
2. In Render, create a new Blueprint and select the GitHub repository containing `render.yaml`.
3. Review the two services and start the Blueprint deployment.
4. Enter the requested backend environment variables in Render's secret/environment settings:
   - `GROQ_API_KEY`
   - `MYSQL_HOST`
   - `MYSQL_PORT`
   - `MYSQL_DATABASE`
   - `MYSQL_USER`
   - `MYSQL_PASSWORD`
5. Use a MySQL service/provider reachable from the deployed API. A MySQL server bound to `127.0.0.1` on your personal computer is not reachable by Render.
6. Create the `constructai` database and `analysis_history` table on the hosted MySQL server using `backend/schema.sql`. Set `MYSQL_DATABASE` to the database name you created.
7. Wait until both Render services are healthy. Open the static frontend service's URL to use the demo.

The frontend Blueprint obtains the API host from the `constructai-api` service. Do not put API keys or database credentials in `render.yaml`, GitHub, or frontend variables. Anything named `VITE_*` is included in the browser bundle and must not contain secrets.

## Troubleshooting

- **Backend reports missing `GROQ_API_KEY`:** Check that `backend/.env` exists, contains the key, and restart Uvicorn.
- **History endpoint returns a database error:** Check that MySQL is running, the database exists, and `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER`, and `MYSQL_PASSWORD` match the database setup.
- **Frontend cannot reach the backend:** Confirm Uvicorn is running on port 8000. For a remote backend, set `VITE_API_BASE_URL` to its HTTPS base URL and rebuild/redeploy the frontend.
- **A feature returns an AI error:** Confirm the Groq key is valid, the model is available to the account, and the backend can reach the Groq API.
- **Render does not show a public demo URL:** Check the build/deploy logs for both services and resolve missing environment variables or database network access.
