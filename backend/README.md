# MySQL analysis history

1. Create the database and table by running `schema.sql` in MySQL Workbench or with the MySQL client.
2. Copy `.env.example` to `.env` in this folder and set the MySQL username and password. Keep any existing `GROQ_API_KEY` setting in `.env`.
3. Restart the FastAPI server.

Successful AI analyses are stored in `analysis_history`. The frontend's **Analysis History** page displays the latest 50 records. The API accepts a `limit` from 1 to 100 at `GET /api/history`.
