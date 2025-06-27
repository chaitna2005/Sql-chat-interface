import gradio as gr
from openai_handler import english_to_sql
from sql_handler import run_sql_query
from utils import to_markdown_table


def chatbot(message, history):
    sql_query, token_info = english_to_sql(message)
    sql_result = run_sql_query(sql_query)

    full_reply = (
        f"**🧠 SQL Query Generated:**\n"
        f"```sql\n{sql_query}\n```\n\n"
        f"**📊 Query Result:**\n"
        f"{sql_result}\n\n"
        f"**🧾 Token Usage:**\n{token_info}"
    )
    return full_reply




def create_interface():
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
    return demo
