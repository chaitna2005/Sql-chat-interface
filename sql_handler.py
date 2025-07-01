import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "school_db"),  # default to school_db if not set
}
print(f"Connecting to DB: {db_config['database']}")

def get_db_connection():
    return mysql.connector.connect(**db_config)

def get_schema_description():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]

        schema_lines = [
            "You are a MySQL expert. You must generate only syntactically correct SQL queries that will run on the following database schema:\n",
            "Database schema:"
        ]

        for table in tables:
            cursor.execute(f"SHOW COLUMNS FROM {table};")
            columns = [row[0] for row in cursor.fetchall()]
            col_list = ", ".join(columns)
            schema_lines.append(f"- {table}({col_list})")

        instructions = """\nInstructions:
1. Use ONLY the tables and columns listed above.
2. Return a single valid SQL query only. No markdown, no explanations.
3. Use UPPER() for case-insensitive matching.
4. Use table aliases for joins.
5. Ensure it runs directly on MySQL.
6. Don't add extra columns or tables.
Convert this natural language input into SQL:"""

        return "\n".join(schema_lines) + instructions

    except mysql.connector.Error as err:
        return f"MySQL Error: {err}"

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def to_markdown_table(rows):
    if not rows:
        return "No data to display."
    headers = list(rows[0].keys())
    header_row = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    data_rows = []
    for row in rows:
        values = [str(row.get(col, "")).replace('\n', ' ') for col in headers]
        data_rows.append("| " + " | ".join(values) + " |")
    return "\n".join([header_row, separator] + data_rows)

def run_sql_query(query):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)

        if query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            if not rows:
                return "No results found."
            return to_markdown_table(rows)
        else:
            conn.commit()
            affected = cursor.rowcount
            return f"Query OK. {affected} row(s) affected."

    except mysql.connector.Error as err:
        return f"MySQL Error: {err}"

    except Exception as e:
        return f"Error: {e}"

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


