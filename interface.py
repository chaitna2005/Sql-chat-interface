import gradio as gr
from openai_handler import english_to_sql
from sql_handler import run_sql_query
from utils import to_markdown_table
from auth_utils import signup_user, login_user

def chatbot(message):
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
        user_state = gr.State(None)

        # --- AUTH UI ---
        with gr.Row(visible=True) as auth_row:
            with gr.Column():
                gr.Markdown("## Login")
                login_username = gr.Textbox(label="Username")
                login_password = gr.Textbox(label="Password", type="password")
                login_button = gr.Button("Login")
                login_status = gr.Textbox(label="Status", interactive=False)
            with gr.Column():
                gr.Markdown("## Signup")
                signup_username = gr.Textbox(label="New Username")
                signup_password = gr.Textbox(label="New Password", type="password")
                signup_button = gr.Button("Signup")
                signup_status = gr.Textbox(label="Status", interactive=False)

        # --- CHAT UI (hidden initially) ---
        with gr.Column(visible=False) as chat_container:
            gr.Markdown("## 🧠 Chat with Your Database")
            chatbot_ui = gr.Chatbot(height=450, show_label=False, type='messages')
            user_welcome = gr.Markdown("")
            txt = gr.Textbox(placeholder="Ask a question in plain English", show_label=False)
            send_btn = gr.Button("Send")
            logout_btn = gr.Button("Logout")

        # --- AUTH HANDLERS ---
        def handle_login(username, password):
            msg, user = login_user(username, password)
            if user:
                return (
                    msg,
                    gr.update(visible=False),
                    gr.update(visible=True),
                    user,
                    f"👋 Welcome, {user}!"
                )
            else:
                return msg, gr.update(visible=True), gr.update(visible=False), None, ""

        def handle_signup(username, password):
            return signup_user(username, password)

        # --- CHAT HANDLERS ---
        def handle_send(message, history=None, user=None):
            history = history or []

            if not user:
                return history, "Please log in first."

            history.append({"role": "user", "content": message})
            bot_reply = chatbot(message)
            history.append({"role": "assistant", "content": bot_reply})

            return history, ""

        def handle_logout():
            return None, gr.update(visible=True), gr.update(visible=False), ""

        # --- EVENTS ---
        login_button.click(
            handle_login,
            inputs=[login_username, login_password],
            outputs=[login_status, auth_row, chat_container, user_state, user_welcome]
        )

        signup_button.click(
            handle_signup,
            inputs=[signup_username, signup_password],
            outputs=[signup_status]
        )

        send_btn.click(
            handle_send,
            inputs=[txt, chatbot_ui, user_state],
            outputs=[chatbot_ui, txt]
        )

        txt.submit(
            handle_send,
            inputs=[txt, chatbot_ui, user_state],
            outputs=[chatbot_ui, txt]
        )

        logout_btn.click(
            handle_logout,
            outputs=[user_state, auth_row, chat_container, user_welcome]
        )

    return demo

# --- MAIN ---
if __name__ == "__main__":
    create_interface().launch(server_port=7861)

