import gradio as gr
from user_service import register_user, login_user, update_password

current_user = None  # Global session variable

def signup(username, password):
    result = register_user(username, password)
    return result

def login(username, password):
    global current_user
    user = login_user(username, password)
    if user:
        current_user = user
        return f"✅ Logged in as {user['username']}", f"User ID: {user['id']}\nCreated at: {user['created_at']}"
    else:
        return "❌ Login failed. Check username/password.", ""

def change_password(old_password, new_password):
    global current_user
    if not current_user:
        return "⚠️ You must be logged in to change password."
    if not old_password or not new_password:
        return "⚠️ Please enter both old and new passwords."
    result = update_password(current_user['username'], old_password, new_password)
    return result

def logout():
    global current_user
    current_user = None
    return "✅ Logged out successfully.", ""

with gr.Blocks() as demo:
    gr.Markdown("# User Authentication System")

    with gr.Tab("Signup"):
        su_username = gr.Textbox(label="Username")
        su_password = gr.Textbox(label="Password", type="password")
        su_btn = gr.Button("Sign Up")
        su_output = gr.Textbox(label="Signup Result")
        su_btn.click(signup, inputs=[su_username, su_password], outputs=su_output)

    with gr.Tab("Login"):
        li_username = gr.Textbox(label="Username")
        li_password = gr.Textbox(label="Password", type="password")
        li_btn = gr.Button("Login")
        li_output = gr.Textbox(label="Login Result")
        li_userinfo = gr.Textbox(label="User Info")
        li_btn.click(login, inputs=[li_username, li_password], outputs=[li_output, li_userinfo])

    with gr.Tab("Change Password"):
        cp_old = gr.Textbox(label="Old Password", type="password")
        cp_new = gr.Textbox(label="New Password", type="password")
        cp_btn = gr.Button("Change Password")
        cp_output = gr.Textbox(label="Change Password Result")
        cp_btn.click(change_password, inputs=[cp_old, cp_new], outputs=cp_output)

    with gr.Tab("Logout"):
        lo_btn = gr.Button("Logout")
        lo_output = gr.Textbox(label="Logout Result")
        lo_userinfo = gr.Textbox(label="User Info")
        lo_btn.click(logout, inputs=None, outputs=[lo_output, lo_userinfo])

demo.launch()


