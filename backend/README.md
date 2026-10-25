# MySQL analysis history

1. Create the database and table by running `schema.sql` in MySQL Workbench or with the MySQL client.
2. Copy `.env.example` to `.env` in this folder and set the MySQL username and password. Keep any existing `GROQ_API_KEY` setting in `.env`.
3. Restart the FastAPI server.

Successful AI analyses are stored in `analysis_history`. The frontend's **Analysis History** page displays the latest 50 records. The API accepts a `limit` from 1 to 100 at `GET /api/history`.

## Public demo on Render

The repository includes a `render.yaml` blueprint for the frontend and API. To create a public demo:

1. Push this repository to GitHub and connect it to Render.
2. Create the services from the blueprint in `render.yaml`.
3. Enter `GROQ_API_KEY` and the connection settings for a remotely reachable MySQL database when Render prompts for them. The MySQL server must allow connections from the deployed API.
4. Wait for both services to finish deploying. The static site URL shown in Render is the demo link.

Keep API keys and database credentials in Render's environment settings, not in source control. The demo uses the configured Groq account and database.
