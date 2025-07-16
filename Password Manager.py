from cryptography.fernet import Fernet


class PasswordManager:
    def __init__(self):
        self.key = self.loadKey()
        self.cipher = Fernet(self.key)
        self.data = self.readPasswordData()

    def saveKeys(self):
        with open('key.txt', 'wb') as file:
            file.write(self.key)

    @staticmethod
    def loadKey():
        try:
            with open('key.txt', 'rb') as file:
                return file.read()

        except FileNotFoundError:
            return Fernet.generate_key()

    def savePasswordData(self):
        name = input("Enter the User name: ")

        while name in self.data:
            name = input("User name exist enter a valid username: ")

            password = input("Enter the Password: ").encode()
            encryptedPassword = self.cipher.encrypt(password)
    
            self.data[name] = encryptedPassword
            self.data = dict(sorted(self.data.items()))
    
            print("New User Registered Successfully")

    def getUserName(self):
        username = input("Enter the Username: ")

        while username not in self.data:
            username = input("Username does not exist enter a valid username: ")

        return username

    def deletePassword(self):
        username = self.getUserName()

        password = input("Enter the Password: ")
        correctPass = self.decrypt(self.data[username])

        while password != correctPass:
            password = input("Passwords do not match. Try again: ")

        self.data.pop(username)
        print("User DELETED Successfully")

    def decrypt(self, password):
        encryptedPasswordBytes = password.decode().encode('ascii')
        decryptedPassword = self.cipher.decrypt(encryptedPasswordBytes)
        normalPass = decryptedPassword.decode('utf-8')

        return normalPass

    def getPasswordData(self):
        username = self.getUserName()
        normalPass = self.decrypt(self.data[username])

        print("The Password is: " + normalPass)

    def changePassword(self):
        username = self.getUserName()
        correctPassword = self.decrypt(self.data[username])
        password = input("Enter your Password: ")

        while password != correctPassword:
            password = input("Wrong Password! Enter your Password: ")

        password = input("Enter the new Password: ")
        encryptedPassword = self.cipher.encrypt(password.encode())

        self.data[username] = encryptedPassword
        self.data = dict(sorted(self.data.items()))

        print("Password Changed Successfully")

    def changeUsername(self):
        username = self.getUserName()

        password = input("Enter the password: ")
        correctPass = self.decrypt(self.data[username])

        while password != correctPass:
            password = input("Wrong Password! Enter your Password: ")

        oldPass = self.data[username]
        self.data.pop(username)
        username = input("Enter the new Username: ")
        self.data[username] = oldPass

        print("Username Changed Successfully")

    @staticmethod
    def readPasswordData():
        try:
            with open('passwords.txt', 'r') as file:
                data = file.read()

                if len(data) == 0:
                    return {}

                return eval(data)

        except FileNotFoundError:
            with open('passwords.txt', 'w') as file:
                return dict()

    def saveData(self):
        with open('passwords.txt', 'w') as file:
            file.write("{\n")

            for name, password in self.data.items():
                file.write(f"'{name}': {password},\n")

            file.write("}")

    def loop(self):
        stop = "yes".casefold()

        while stop != "No".casefold():
            choice = input("Whats your operation\n1: Add a password\n2: Change a Password\n3: Check your password\n4: Delete user\n5: Modify Username\nChoice:  ")

            if choice.lower() == "1":
                self.savePasswordData()

            elif choice.lower() == "2":
                self.changePassword()

            elif choice == "3":
                self.getPasswordData()

            elif choice == "4":
                self.deletePassword()

            elif choice == "5":
                self.changeUsername()

            stop = input("Would you like to continue? (Y/N): ").casefold()

        self.saveData()
        self.saveKeys()


mng = PasswordManager()
mng.loop()
