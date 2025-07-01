# Sql-chat-interface

A simple SQL-powered chat interface built with Python and OpenAI API.

## Features
- Send SQL queries via chat
- Get responses from your database
- Easy to use and extend

## 🚀 What You’ve Successfully Implemented

The project currently includes the following key features, each tested and confirmed working as expected:

| Feature                          | ✅ Status    |
|---------------------------------|-------------|
| Natural language to SQL via GPT  | Working     |
| MySQL live schema reader         | Working     |
| Markdown tables in Gradio chat   | Clean & neat|
| Token logging to file (`token_log.txt`) | Accurate |
| Modular code (split into files)  | Organized   |

## 🔒 Recent Improvements: Enhanced User Authentication & UI

- **Secure Password Hashing**  
  Passwords are now securely hashed before storing in the database, protecting user credentials from exposure.

- **Improved Login Flow**  
  Users are automatically redirected to the chat interface upon successful login for a smoother experience.

- **Logout Feature Added**  
  A logout button has been integrated within the chat UI to allow users to safely sign out.

- **Frontend & Backend Integration**  
  Signup, login, password change, and logout functionalities are fully connected between frontend (Gradio) and backend.  
  Clear success and error messages provide immediate user feedback.

- **Dynamic UI Based on User Status**  
  The interface dynamically updates visible elements depending on whether the user is logged in, improving usability and clarity.

- **Chat AI System Fully Maintained**  
  The core functionality where natural language queries are converted into SQL and executed remains fully intact and operational.

## How to run
1. Clone this repo  
2. Create and activate your virtual environment  
3. Install dependencies from `requirements.txt`  
4. Run `app.py`  

## License
This project is licensed under the MIT License.

