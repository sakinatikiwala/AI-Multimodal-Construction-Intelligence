import json
import os
from typing import Any

import mysql.connector
from mysql.connector import Error


def _connect():
    required_settings = ("MYSQL_DATABASE", "MYSQL_USER")
    missing_settings = [name for name in required_settings if not os.getenv(name)]
    if missing_settings:
        raise RuntimeError(
            f"Missing MySQL settings: {', '.join(missing_settings)}. "
            "Configure them in backend/.env."
        )

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=os.environ["MYSQL_DATABASE"],
        user=os.environ["MYSQL_USER"],
        password=os.getenv("MYSQL_PASSWORD", ""),
        connection_timeout=5,
    )


def _ensure_schema(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analysis_history (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            feature VARCHAR(150) NOT NULL,
            request_data JSON NOT NULL,
            response_data JSON NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_analysis_history_created_at (created_at)
        )
        """
    )


def save_analysis(feature: str, request_data: dict[str, Any], response_data: dict[str, Any]) -> None:
    connection = None
    try:
        connection = _connect()
        cursor = connection.cursor()
        _ensure_schema(cursor)
        cursor.execute(
            """
            INSERT INTO analysis_history (feature, request_data, response_data)
            VALUES (%s, %s, %s)
            """,
            (
                feature,
                json.dumps(request_data, ensure_ascii=False),
                json.dumps(response_data, ensure_ascii=False),
            ),
        )
        connection.commit()
        cursor.close()
    except (Error, RuntimeError, ValueError) as error:
        if connection:
            connection.rollback()
        raise RuntimeError(f"Could not save analysis history: {error}") from error
    finally:
        if connection and connection.is_connected():
            connection.close()


def get_analysis_history(limit: int = 50) -> list[dict[str, Any]]:
    connection = None
    try:
        connection = _connect()
        cursor = connection.cursor(dictionary=True)
        _ensure_schema(cursor)
        cursor.execute(
            """
            SELECT id, feature, request_data, response_data, created_at
            FROM analysis_history
            ORDER BY created_at DESC, id DESC
            LIMIT %s
            """,
            (limit,),
        )
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            for field in ("request_data", "response_data"):
                if isinstance(row[field], str):
                    row[field] = json.loads(row[field])
            row["created_at"] = row["created_at"].isoformat()
        return rows
    except (Error, RuntimeError, ValueError) as error:
        raise RuntimeError(f"Could not load analysis history: {error}") from error
    finally:
        if connection and connection.is_connected():
            connection.close()
