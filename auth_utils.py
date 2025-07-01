# auth_utils.py

import bcrypt
import mysql.connector
from dotenv import load_dotenv
import os
from sql_handler import get_db_connection  # Make sure this returns a working MySQL connection

load_dotenv()


# -------------------
# PASSWORD UTILITIES
# -------------------

def hash_password(password: str) -> bytes:
    """
    Hash a plain-text password and return the hashed bytes.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    """
    Verify a plain-text password against the hashed password.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)


# -------------------
# USER AUTH FUNCTIONS
# -------------------

def signup_user(username: str, password: str) -> str:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return "Username already exists."
        hashed = hash_password(password).decode('utf-8')
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed))
        conn.commit()
        cursor.close()
        conn.close()
        return "Signup successful. Please log in."
    except mysql.connector.Error as err:
        return f"MySQL Error: {err}"
    except Exception as e:
        return f"Error: {e}"



def login_user(username: str, password: str) -> tuple[str, str | None]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        return "Invalid username or password.", None

    hashed_from_db = result[0].encode('utf-8')
    print(f"Login attempt for user: {username}")
    print(f"Stored hash: {hashed_from_db}")
    print(f"Password entered: {password}")

    if verify_password(password, hashed_from_db):
        return "Login successful.", username
    else:
        print("Password verification failed.")
        return "Invalid username or password.", None



# -------------------
# OPTIONAL TEST BLOCK
# -------------------

if __name__ == "__main__":
    pw = "testpassword123"
    hashed_pw = hash_password(pw)
    print("Hashed password:", hashed_pw)

    print("Correct password:", verify_password("testpassword123", hashed_pw))  # True
    print("Wrong password:", verify_password("wrongpass", hashed_pw))  # False

