# Sql-chat-interface

A simple SQL-powered chat interface built with Python and OpenAI API.

## Features
- Send SQL queries via chat
- Get responses from your database
- Easy to use and extend

## 🚀 What You’ve Successfully Implemented

The project currently includes the following key features, each tested and confirmed working as expected:

| Feature                                  | ✅ Status     |
|------------------------------------------|--------------|
| Natural language to SQL via GPT          | Working      |
| MySQL live schema reader                 | Working      |
| PostgreSQL live schema reader            | Working      |
| Markdown tables in Gradio chat           | Clean & neat |
| Token logging to file (`token_log.txt`)  | Accurate     |
| Modular code (split into files)          | Organized    |
| Multi-database support (.env-based)      | ✅ Implemented|

## 🔄 Latest Additions: PostgreSQL Support & Improved Flexibility

- **PostgreSQL Integration**  
  The system now supports both MySQL and PostgreSQL. Just switch the `DB_TYPE` value in the `.env` file (`mysql` or `postgres`) and the app will connect accordingly.

- **Dynamic Schema Description**  
  Schema is read live from either MySQL or PostgreSQL and used to generate more accurate SQL queries based on the actual structure.

- **Database-Agnostic Query Execution**  
  All query execution logic now handles both PostgreSQL and MySQL backends using shared code paths with proper drivers (`psycopg2` and `mysql-connector-python`).

- **Improved Connection Management**  
  The app now connects through `password_db.py`, ensuring centralized and reusable logic for database access.

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
4. Create a `.env` file with your DB credentials and set `DB_TYPE` to either `mysql` or `postgres`  
5. Run `app.py`  

## License
This project is licensed under the MIT License.


