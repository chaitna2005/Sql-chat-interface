import mysql.connector
from auth_utils import hash_password, verify_password
from sql_handler import get_db_connection  # assuming your existing db connection here

def register_user(username: str, password: str) -> str:
    """
    Registers a new user with hashed password.
    Returns success or error message.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return "Error: Username already taken."

        # Hash the password and decode bytes to string before storing
        pw_hash = hash_password(password).decode('utf-8')

        # Insert new user
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, pw_hash)
        )
        conn.commit()
        return "User registered successfully."
    except mysql.connector.Error as err:
        return f"MySQL Error: {err}"
    finally:
        cursor.close()
        conn.close()

def login_user(username: str, password: str) -> dict:
    """
    Verifies user credentials.
    Returns user info dict if success, else None.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return None

        # Verify password (encode stored hash string back to bytes)
        if verify_password(password, user["password_hash"].encode('utf-8')):
            # Remove password_hash before returning user data
            user.pop("password_hash")
            return user
        else:
            return None
    except mysql.connector.Error:
        return None
    finally:
        cursor.close()
        conn.close()

def update_password(username: str, old_password: str, new_password: str) -> str:
    """
    Updates password if old_password matches.
    Returns success or error message.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch user
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return "User not found."

        if not verify_password(old_password, user["password_hash"].encode('utf-8')):
            return "Old password is incorrect."

        # Hash new password and decode bytes to string before storing
        new_pw_hash = hash_password(new_password).decode('utf-8')

        # Update password in DB
        cursor.execute(
            "UPDATE users SET password_hash = %s WHERE username = %s",
            (new_pw_hash, username)
        )
        conn.commit()
        return "Password updated successfully."
    except mysql.connector.Error as err:
        return f"MySQL Error: {err}"
    finally:
        cursor.close()
        conn.close()
