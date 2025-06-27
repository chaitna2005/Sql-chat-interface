import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define DB config
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

# Reusable DB connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Function to generate schema description
def get_schema_description():
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

# Import markdown table converter
from utils import to_markdown_table

# Function to run SQL and return result
def run_sql_query(query):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        if query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            if not rows:
                return "No results found."
            else:
                return to_markdown_table(rows)  # ✅ Shows as markdown table
        else:
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            conn.close()
            return f"Query OK. {affected} row(s) affected."
    except mysql.connector.Error as err:
        return f"MySQL Error: {err}"
    except Exception as e:
        return f"Error: {e}"

