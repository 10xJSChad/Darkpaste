from AnaDB import AnaDatabase
import Registration

darkpaste = AnaDatabase("Darkpaste")
darkpaste.load()
print("Enter username")
username = input()
print("Enter password")
password = input()

print(Registration.register(username, password)[1])
print("Ctrl+C to exit")
input()

darkpaste.enter("users", [username, password, "x", "x"])
darkpaste.save()