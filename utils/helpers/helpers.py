def take_confirmation():
    # Define the correct password
    correct_password = "fortunealpha13"

    # Prompt the user to enter the password
    user_password = input("Please check the stocks before continuing. Enter the confirmation code to proceed: ")

    # Check if the entered password is correct
    if user_password == correct_password:
        print("Confirmation Code confirmed. Proceeding with the process...")
        return True
    else:
        print("Access denied. Incorrect password.")
        return False