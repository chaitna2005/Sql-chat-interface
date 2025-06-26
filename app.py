import os
from dotenv import load_dotenv
from openai import OpenAI
import mysql.connector
import gradio as gr

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# MySQL config from .env
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

# Load live schema from database
def get_schema_description():
    try:
        conn = mysql.connector.connect(**db_config)
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
        instructions = """
Instructions:
1. Use ONLY the tables and columns listed above.
2. Return a single valid SQL query only. No markdown, no explanations.
3. Use UPPER() for case-insensitive matching.
4. Use table aliases for joins.
5. Ensure it runs directly on MySQL.
6. Don't add extra columns or tables.
Convert this natural language input into SQL:
"""
        return "\n".join(schema_lines) + instructions
    except mysql.connector.Error as err:
        return f"MySQL Error: {err}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Connect to DB
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Convert SQL results to markdown table
def to_markdown_table(data):
    if not data:
        return "No results found."
    headers = list(data[0].keys())
    header_row = "| " + " | ".join(headers) + " |"
    separator_row = "| " + " | ".join(["---"] * len(headers)) + " |"
    rows = []
    for row in data:
        rows.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    return "\n".join([header_row, separator_row] + rows)

# Translate English to SQL using GPT
def english_to_sql(user_input):
    schema_prompt = get_schema_description()
    full_prompt = f"{schema_prompt}\n{user_input}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response.choices[0].message.content.strip()

# Run SQL and return results
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
                return to_markdown_table(rows)
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

# Chatbot logic
def chatbot(message, history):
    sql_query = english_to_sql(message)
    sql_result = run_sql_query(sql_query)
    full_reply = (
        f"**🧠 SQL Query Generated:**\n"
        f"```sql\n{sql_query}\n```\n"
        f"**📊 Query Result:**\n{sql_result}"
    )
    return full_reply

# Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧠 Chat with Your Database")
    gr.Markdown("Ask any question about your SQL database using plain English.")

    chatbot_ui = gr.Chatbot(height=450, show_label=False)
    txt = gr.Textbox(placeholder="e.g. Show me all students in grade 10", show_label=False)

    def respond(message, history):
        bot_response = chatbot(message, history)
        history.append((message, bot_response))
        return history, ""

    txt.submit(respond, [txt, chatbot_ui], [chatbot_ui, txt])

demo.launch(share=True)








