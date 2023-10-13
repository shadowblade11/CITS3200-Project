from app.models import User

def getCredentials(user, passwd):
    u = User(username=user)
    u.set_passwd(passwd)
    u.is_admin = True
    User.write_to(u)
    
    
if __name__ == "__main__":
    username = input("Please enter a username.\nUsername: ")
    password = input("\nPlease enter a password.\nPassword: ")
    password_retype = input("\nPlease enter your password again.\nRe-type Password: ")

    if (password == password_retype):
        getCredentials(username, password)
        print("\nYour account has been created!\n")
        exit(0)
    else:
        print("Your passwords do not match. Please try again.")
        exit(1)

