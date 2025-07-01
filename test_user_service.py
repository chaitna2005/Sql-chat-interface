import time
from user_service import register_user, login_user, update_password

username = f"testuser{int(time.time())}"  # unique username each run

def test_register():
    print(register_user(username, "Password123!"))

def test_login(password):
    user = login_user(username, password)
    if user:
        print(f"Login successful with password '{password}':", user)
    else:
        print(f"Login failed with password '{password}'.")

def test_update_password():
    print(update_password(username, "Password123!", "NewPass456!"))

if __name__ == "__main__":
    test_register()
    test_login("Password123!")
    test_update_password()
    test_login("NewPass456!")

